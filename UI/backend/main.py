from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.concurrency import run_in_threadpool
from pydantic import BaseModel, EmailStr
import smtplib
from email.message import EmailMessage
from motor.motor_asyncio import AsyncIOMotorClient
import bcrypt
from datetime import datetime, timedelta
import secrets
import os

# Initialize FastAPI app
app = FastAPI()

# Allow frontend to talk to backend (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Email sending credentials (Use environment variables instead of hardcoding)
EMAIL_ADDRESS = os.getenv("EMAIL_USER", "mrunalshardul234@gmail.com")
EMAIL_PASSWORD = os.getenv("EMAIL_PASS", "oatb gtic zpjr yqae")

# Connect to MongoDB
MONGO_DETAILS = "mongodb://localhost:27017"
client = AsyncIOMotorClient(MONGO_DETAILS)
db = client.vsecuresphere
users_collection = db.users
attempts_collection = db.knowledge_check_attempts
password_reset_tokens_collection = db.password_reset_tokens

# Pydantic models
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

# Helper: Hash password
async def hash_password(password: str) -> str:
    hashed = await run_in_threadpool(bcrypt.hashpw, password.encode('utf-8'), bcrypt.gensalt())
    return hashed.decode('utf-8')

# Helper: Verify password
async def verify_password(plain_password: str, hashed_password: str) -> bool:
    return await run_in_threadpool(bcrypt.checkpw, plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

# Register route
@app.post("/register")
async def register_user(user: RegisterUser):
    existing_user = await users_collection.find_one({"username": user.username})
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    hashed_password = await hash_password(user.password)

    new_user = {
        "name": user.name,
        "email": user.email,
        "username": user.username,
        "password": hashed_password
    }
    await users_collection.insert_one(new_user)

    return {"message": f"User {user.username} registered successfully!"}

# Login route
@app.post("/login")
async def login_user(user: LoginUser):
    existing_user = await users_collection.find_one({"username": user.username})

    # Check if the user exists
    if not existing_user:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    # Now we compare the provided password with the stored hash
    is_password_correct = bcrypt.checkpw(user.password.encode('utf-8'), existing_user["password"].encode('utf-8'))

    if not is_password_correct:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    return {"message": f"Welcome back, {user.username}!"}

# Forgot password route
@app.post("/forgot-password")
async def forgot_password(request: ForgotPasswordRequest):
    user = await users_collection.find_one({"email": request.email})

    if not user:
        raise HTTPException(status_code=404, detail="Email not found")

    # Generate a secure token for password reset
    token = secrets.token_urlsafe(32)  # Generate a random token
    expires_at = datetime.utcnow() + timedelta(hours=1)  # Token expiration time

    # Store the token in the database with an expiration time
    await password_reset_tokens_collection.insert_one({
        "email": request.email,
        "token": token,
        "expires_at": expires_at
    })

    reset_link = f"http://localhost:5500/reset-password.html?token={token}"

    # Construct the email
    msg = EmailMessage()
    msg["Subject"] = "VSecureSphere Password Reset"
    msg["From"] = f"VSecureSphere Support <{EMAIL_ADDRESS}>"
    msg["To"] = request.email
    msg["Reply-To"] = "no-reply@vsecuresphere.com"
    msg.set_content(f"""
    Hello {user['name']},

    You requested a password reset. Please click the link below to reset your password:
    {reset_link}

    This link will expire in 1 hour.

    If you did not request this, please ignore this email.
    """)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
        return {"message": "Reset link sent to your email"}
    except smtplib.SMTPException as e:
        raise HTTPException(status_code=500, detail=f"SMTP error: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")

# Reset password route
@app.post("/reset-password")
async def reset_password(payload: ResetPasswordRequest):
    # Retrieve the reset token record from the database
    record = await password_reset_tokens_collection.find_one({"token": payload.token})

    if not record:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    # Check if the token has expired
    if record["expires_at"] < datetime.utcnow():
        # Delete expired token
        await password_reset_tokens_collection.delete_one({"token": payload.token})
        raise HTTPException(status_code=400, detail="Token expired")

    # Hash the new password
    hashed_password = await hash_password(payload.new_password)

    # Update the user's password
    await users_collection.update_one(
        {"email": record["email"]},
        {"$set": {"password": hashed_password}}
    )

    # Delete the token after successful password reset
    await password_reset_tokens_collection.delete_one({"token": payload.token})

    return {"message": "Password reset successfully!"}

# Submit knowledge check attempt
@app.post("/submit-knowledge-check")
async def submit_knowledge_check(attempt: KnowledgeCheckAttempt):
    user_id = attempt.user_id
    experiment_id = attempt.experiment_id
    score = attempt.score
    passed = attempt.passed

    previous_attempts = await attempts_collection.count_documents({
        "user_id": user_id,
        "experiment_id": experiment_id
    })

    attempt_number = previous_attempts + 1

    new_attempt = {
        "user_id": user_id,
        "experiment_id": experiment_id,
        "attempt_number": attempt_number,
        "score": score,
        "passed": passed,
        "timestamp": datetime.utcnow()
    }
    await attempts_collection.insert_one(new_attempt)

    return {"message": "Attempt recorded", "attempt_number": attempt_number}

# Get knowledge check attempts
@app.get("/get-knowledge-check-attempts/{user_id}/{experiment_id}")
async def get_attempts(user_id: str, experiment_id: str):
    attempts = await attempts_collection.find({
        "user_id": user_id,
        "experiment_id": experiment_id
    }).to_list(length=None)

    return {"attempts": attempts}
