from passlib.context import CryptContext
import smtplib
from email.message import EmailMessage
import os

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def send_reset_email(email_to: str, reset_link: str):
    msg = EmailMessage()
    msg["Subject"] = "Reset Your VSecureSphere Password"
    msg["From"] = os.getenv("EMAIL_USER")
    msg["To"] = email_to
    msg.set_content(f"Click this link to reset your password: {reset_link}")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(os.getenv("EMAIL_USER"), os.getenv("EMAIL_PASS"))
        smtp.send_message(msg)
