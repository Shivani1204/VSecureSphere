from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from email.message import EmailMessage
import smtplib

# Initialize FastAPI app
app = FastAPI()

# Allow frontend to talk to backend (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or ["http://localhost:5500"] if running frontend locally
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Email sending credentials
EMAIL_ADDRESS = "mrunalshardul234@gmail.com"         # Your Gmail
EMAIL_PASSWORD = "oatb gtic zpjr yqae"                # Your Gmail App Password

# Pydantic model for forgot password request
class ForgotPasswordRequest(BaseModel):
    email: EmailStr

@app.post("/forgot-password")
async def forgot_password(request: ForgotPasswordRequest):
    # Construct the email message
    msg = EmailMessage()
    msg["Subject"] = "VSecureSphere Password Reset"
    msg["From"] = "VSecureSphere Support <{}>".format(EMAIL_ADDRESS)  # ✅ Set nicely
    msg["To"] = request.email
    msg["Reply-To"] = "no-reply@vsecuresphere.com"  # ✅ Optional but good
    msg.set_content(f"""
    Hello,

    Click the link below to reset your password:
    http://localhost:8000/reset-password?email={request.email}

    If you did not request this, please ignore this email.
    """)

    try:
        # Sending email through Gmail's SMTP server
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
        return {"message": "Reset link sent to your email"}
    except Exception as e:
        print("Email error:", e)
        raise HTTPException(status_code=500, detail="Error sending email")
