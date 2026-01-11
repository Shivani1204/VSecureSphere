from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.concurrency import run_in_threadpool
from pydantic import BaseModel, EmailStr
from motor.motor_asyncio import AsyncIOMotorClient
from email.message import EmailMessage
import smtplib
import bcrypt
from datetime import datetime, timedelta
import secrets
import os

# =========================
# FastAPI app
# =========================
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# Environment variables (REQUIRED)
# =========================
EMAIL_ADDRESS = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASS")
MONGO_DETAILS = os.getenv("MONGO_URI")

if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
    raise RuntimeError("EMAIL_USER or EMAIL_PASS environment variables are not set")

if not MONGO_DETAILS:
    raise RuntimeError("MONGO_URI environment variable is not set")

# =========================
# MongoDB connection
# =========================
client = AsyncIOMotorClient(MONGO_DETAILS)
db = client.vsecuresphere

users_collection = db.users
attempts_collection = db.knowledge_check_attempts
password_reset_tokens_collection = db.password_reset_tokens

# =========================
# Models
# =========================
class RegisterUser(BaseModel):
    name: str
    email: EmailStr
    username: str
    password: str

class LoginUser(BaseModel):
    username: str
    password: str

class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str

class KnowledgeCheckAttempt(BaseModel):
    user_id: str
    experiment_id: str
    score: int
    passed: bool

# =========================
# Helpers
# =========================
async def hash_password(password: str) -> str:
    hashed = await run_in_threadpool(
        bcrypt.hashpw,
        password.encode("utf-8"),
        bcrypt.gensalt()
    )
    return hashed.decode("utf-8")

async def verify_password(plain_password: str, hashed_password: str) -> bool:
    return await run_in_threadpool(
        bcrypt.checkpw,
        plain_password.encode("utf-8"),
        hashed_password.encode("utf-8")
    )

# =========================
# Routes
# =========================
@app.post("/register")
async def register_user(user: RegisterUser):
    if await users_collection.find_one({"username": user.username}):
        raise HTTPException(status_code=400, detail="Username already exists")

    hashed_password = await hash_password(user.password)

    await users_collection.insert_one({
        "name": user.name,
        "email": user.email,
        "username": user.username,
        "password": hashed_password
    })

    return {"message": f"User {user.username} registered successfully!"}


@app.post("/login")
async def login_user(user: LoginUser):
    existing_user = await users_collection.find_one({"username": user.username})

    if not existing_user:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    if not await verify_password(user.password, existing_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    return {"message": f"Welcome back, {user.username}!"}


@app.post("/forgot-password")
async def forgot_password(request: ForgotPasswordRequest):
    user = await users_collection.find_one({"email": request.email})

    if not user:
        raise HTTPException(status_code=404, detail="Email not found")

    token = secrets.token_urlsafe(32)
    expires_at = datetime.utcnow() + timedelta(hours=1)

    await password_reset_tokens_collection.insert_one({
        "email": request.email,
        "token": token,
        "expires_at": expires_at
    })

    reset_link = f"http://localhost:5500/reset-password.html?token={token}"

    msg = EmailMessage()
    msg["Subject"] = "VSecureSphere Password Reset"
    msg["From"] = f"VSecureSphere Support <{EMAIL_ADDRESS}>"
    msg["To"] = request.email
    msg.set_content(
        f"Click this link to reset your password:\n\n{reset_link}\n\n"
        "This link expires in 1 hour."
    )

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Email error: {e}")

    return {"message": "Reset link sent to your email"}


@app.post("/reset-password")
async def reset_password(payload: ResetPasswordRequest):
    record = await password_reset_tokens_collection.find_one({"token": payload.token})

    if not record or record["expires_at"] < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    hashed_password = await hash_password(payload.new_password)

    await users_collection.update_one(
        {"email": record["email"]},
        {"$set": {"password": hashed_password}}
    )

    await password_reset_tokens_collection.delete_one({"token": payload.token})

    return {"message": "Password reset successfully!"}


@app.post("/submit-knowledge-check")
async def submit_knowledge_check(attempt: KnowledgeCheckAttempt):
    previous_attempts = await attempts_collection.count_documents({
        "user_id": attempt.user_id,
        "experiment_id": attempt.experiment_id
    })

    await attempts_collection.insert_one({
        "user_id": attempt.user_id,
        "experiment_id": attempt.experiment_id,
        "attempt_number": previous_attempts + 1,
        "score": attempt.score,
        "passed": attempt.passed,
        "timestamp": datetime.utcnow()
    })

    return {"message": "Attempt recorded", "attempt_number": previous_attempts + 1}


@app.get("/get-knowledge-check-attempts/{user_id}/{experiment_id}")
async def get_attempts(user_id: str, experiment_id: str):
    attempts = await attempts_collection.find({
        "user_id": user_id,
        "experiment_id": experiment_id
    }).to_list(length=None)

    return {"attempts": attempts}
