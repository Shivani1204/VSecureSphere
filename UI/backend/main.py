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

from zoneinfo import ZoneInfo

IST = ZoneInfo("Asia/Kolkata")

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
    username: str
    experiment_id: str
    score: int
    passed: bool

class LabCompletion(BaseModel):
    username: str
    experiment_id: str


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
        "username": attempt.username,
        "experiment_id": attempt.experiment_id
    })

    await attempts_collection.insert_one({
        "username": attempt.username,
        "experiment_id": attempt.experiment_id,
        "attempt_number": previous_attempts + 1,
        "score": attempt.score,
        "passed": attempt.passed,
        "timestamp": datetime.utcnow()
    })

    return {"message": "Attempt recorded", "attempt_number": previous_attempts + 1}


@app.get("/get-knowledge-check-attempts/{username}/{experiment_id}")
async def get_attempts(username: str, experiment_id: str):
    attempts = await attempts_collection.find({
        "username": username,
        "experiment_id": experiment_id
    }).to_list(length=None)

    return {"attempts": attempts}

@app.post("/complete-lab")
async def complete_lab(data: LabCompletion):
    # 1️⃣ Find latest quiz attempt
    latest_attempt = await attempts_collection.find(
        {
            "username": data.username,
            "experiment_id": data.experiment_id
        }
    ).sort("timestamp", -1).limit(1).to_list(1)

    # 2️⃣ No quiz attempted
    if not latest_attempt:
        raise HTTPException(
            status_code=400,
            detail="Please complete the quiz before finishing the lab."
        )

    # 3️⃣ Quiz attempted but not passed
    if not latest_attempt[0]["passed"]:
        raise HTTPException(
            status_code=403,
            detail="You must pass the quiz before completing the lab."
        )

    # 4️⃣ Check if lab already completed
    existing = await completed_labs_collection.find_one({
        "username": data.username,
        "experiment_id": data.experiment_id
    })

    if existing:
        return {"message": "Lab already completed."}

    # 5️⃣ Mark lab as completed
    await completed_labs_collection.insert_one({
        "username": data.username,
        "experiment_id": data.experiment_id,
        "completed_at": datetime.utcnow()
    })

    return {"message": "Lab completed successfully ✅"}


# =========================
# USER PROFILE (NEW)
# =========================


@app.get("/profile/{username}")
async def get_profile(username: str):
    user = await users_collection.find_one(
        {"username": username},
        {"_id": 0, "password": 0}
    )

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    attempts = await attempts_collection.find({
        "username": username
    }).sort("timestamp", -1).to_list(None)

    formatted_attempts = []
    for a in attempts:
        ts = a["timestamp"]

        # Ensure timestamp is timezone-aware (Mongo usually stores UTC)
        if ts.tzinfo is None:
            ts = ts.replace(tzinfo=ZoneInfo("UTC"))

        ist_time = ts.astimezone(IST)

        formatted_attempts.append({
            "experiment": a["experiment_id"],
            "attempt": a["attempt_number"],
            "score": a["score"],
            "passed": a["passed"],
            "timestamp": ist_time.strftime("%Y-%m-%d %H:%M")
        })

    completed_labs = await db.completed_labs.find({
        "username": username
    }).to_list(length=None)

    total_score = sum(a["score"] for a in attempts)

    return {
        "name": user["name"],
        "email": user["email"],
        "attempts": formatted_attempts,
        "labsCompleted": [lab["experiment_id"] for lab in completed_labs]
    }
