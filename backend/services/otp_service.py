# services/otp_service.py - OTP generation and verification (Simulated)
import random
import string
from datetime import datetime, timedelta
from config import settings
import sqlite3

def generate_otp(length: int = 6) -> str:
    """Generate a random OTP code"""
    return ''.join(random.choices(string.digits, k=length))

def send_otp(phone: str, otp_code: str) -> bool:
    """
    Send OTP via SMS
    In production, integrate with Twilio or similar service
    For now, just print to console (simulated)
    """
    if settings.SMS_PROVIDER == "simulated":
        print(f"📱 [SIMULATED SMS] Sending OTP to {phone}: {otp_code}")
        print(f"   (In production, this would use {settings.SMS_PROVIDER})")
        return True
    elif settings.SMS_PROVIDER == "twilio":
        # TODO: Integrate Twilio
        # from twilio.rest import Client
        # client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        # message = client.messages.create(
        #     body=f"Your verification code is: {otp_code}",
        #     from_=settings.TWILIO_PHONE_NUMBER,
        #     to=phone
        # )
        # return message.sid is not None
        print(f"Twilio integration not yet configured. OTP: {otp_code}")
        return True
    else:
        print(f"Unknown SMS provider: {settings.SMS_PROVIDER}")
        return False

def create_otp(db: sqlite3.Connection, phone: str) -> tuple[str, bool]:
    """
    Create and store OTP for a phone number
    Returns (otp_code, success)
    """
    cursor = db.cursor()
    
    # Generate OTP
    otp_code = generate_otp(settings.OTP_LENGTH)
    
    # Calculate expiry time
    expires_at = datetime.now() + timedelta(minutes=settings.OTP_EXPIRY_MINUTES)
    
    try:
        # Delete any existing OTPs for this phone
        cursor.execute(
            "DELETE FROM otp_verification WHERE phone = ? AND is_verified = 0",
            (phone,)
        )
        
        # Insert new OTP
        cursor.execute(
            """INSERT INTO otp_verification (phone, otp_code, expires_at, is_verified)
               VALUES (?, ?, ?, 0)""",
            (phone, otp_code, expires_at)
        )
        db.commit()
        
        # Send OTP
        send_result = send_otp(phone, otp_code)
        
        return otp_code, send_result
        
    except Exception as e:
        print(f"Error creating OTP: {e}")
        return None, False

def verify_otp(db: sqlite3.Connection, phone: str, otp_code: str) -> bool:
    """
    Verify OTP code for a phone number
    Returns True if valid, False otherwise
    """
    cursor = db.cursor()
    
    # Get latest OTP for this phone
    cursor.execute(
        """SELECT id, otp_code, expires_at, is_verified 
           FROM otp_verification 
           WHERE phone = ? 
           ORDER BY created_at DESC 
           LIMIT 1""",
        (phone,)
    )
    result = cursor.fetchone()
    
    if not result:
        print(f"No OTP found for phone: {phone}")
        return False
    
    otp_id, stored_otp, expires_at, is_verified = result
    
    # Check if already verified
    if is_verified:
        print(f"OTP already used for phone: {phone}")
        return False
    
    # Check if expired
    expires_at_dt = datetime.fromisoformat(expires_at)
    if datetime.now() > expires_at_dt:
        print(f"OTP expired for phone: {phone}")
        return False
    
    # Verify code
    if stored_otp != otp_code:
        print(f"Invalid OTP code for phone: {phone}")
        return False
    
    # Mark as verified
    cursor.execute(
        "UPDATE otp_verification SET is_verified = 1 WHERE id = ?",
        (otp_id,)
    )
    db.commit()
    
    print(f"✅ OTP verified successfully for phone: {phone}")
    return True

def cleanup_expired_otps(db: sqlite3.Connection):
    """Remove expired OTPs from database"""
    cursor = db.cursor()
    cursor.execute(
        "DELETE FROM otp_verification WHERE expires_at < ? OR is_verified = 1",
        (datetime.now(),)
    )
    deleted = cursor.rowcount
    db.commit()
    print(f"Cleaned up {deleted} expired/used OTPs")
    return deleted
