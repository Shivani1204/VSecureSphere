from fastapi import APIRouter, HTTPException
from database import user_collection
from models import UserRegister, UserLogin, ForgotPasswordRequest, ResetPasswordRequest
from utils import hash_password, verify_password, send_reset_email
from bson.objectid import ObjectId

router = APIRouter()

@router.post("/register")
def register(user: UserRegister):
    if user_collection.find_one({"username": user.username}) or user_collection.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="Username or Email already exists.")
    
    user_dict = user.dict()
    user_dict["password"] = hash_password(user.password)
    user_collection.insert_one(user_dict)
    return {"message": "User registered successfully"}

@router.post("/login")
def login(data: UserLogin):
    user = user_collection.find_one({"username": data.username})
    if not user or not verify_password(data.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    return {
        "message": "Login successful",
        "username": user["username"],
        "email": user["email"]
    }

@router.post("/forgot-password")
def forgot_password(request: ForgotPasswordRequest):
    user = user_collection.find_one({"email": request.email})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    reset_link = f"http://localhost:8000/reset-password/{str(user['_id'])}"
    send_reset_email(request.email, reset_link)
    return {"message": "Reset email sent"}

@router.post("/reset-password/{user_id}")
def reset_password(user_id: str, request: ResetPasswordRequest):
    hashed = hash_password(request.new_password)
    result = user_collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {"password": hashed}}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=400, detail="Password reset failed")
    return {"message": "Password updated successfully"}
