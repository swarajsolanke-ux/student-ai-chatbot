# services/auth_service.py - Authentication and JWT service
from jose import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from config import settings
from typing import Optional
import sqlite3

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hash a password"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create JWT access token"""
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire, "type": "access"})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: dict):
    """Create JWT refresh token"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def create_tokens_for_user(user_id: int, email: Optional[str] = None):
    """Create both access and refresh tokens for a user"""
    token_data = {"sub": str(user_id)}
    if email:
        token_data["email"] = email
    
    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    }

def authenticate_user(db: sqlite3.Connection, email: str, password: str):
    """Authenticate a user by email and password"""
    cursor = db.cursor()
    cursor.execute(
        "SELECT id, email, password_hash, is_active FROM users WHERE email = ?",
        (email,)
    )
    user = cursor.fetchone()
    
    if not user:
        return None
    
    user_id, user_email, password_hash, is_active = user
    
    if not is_active:
        return None
    
    if password_hash and verify_password(password, password_hash):
        return {"id": user_id, "email": user_email}
    
    return None

def create_user(db: sqlite3.Connection, phone: Optional[str], email: Optional[str], 
                password: Optional[str], auth_provider: str = "email"):
    """Create a new user"""
    cursor = db.cursor()
    
    # Hash password if provided
    password_hash = hash_password(password) if password else None
    
    try:
        cursor.execute(
            """INSERT INTO users (phone, email, password_hash, auth_provider, is_active, is_premium)
               VALUES (?, ?, ?, ?, 1, 0)""",
            (phone, email, password_hash, auth_provider)
        )
        db.commit()
        user_id = cursor.lastrowid
        return user_id
    except sqlite3.IntegrityError:
        # User already exists
        return None

def get_user_by_email(db: sqlite3.Connection, email: str):
    """Get user by email"""
    cursor = db.cursor()
    cursor.execute(
        "SELECT id, email, phone, auth_provider, is_active, is_premium FROM users WHERE email = ?",
        (email,)
    )
    user = cursor.fetchone()
    
    if user:
        return {
            "id": user[0],
            "email": user[1],
            "phone": user[2],
            "auth_provider": user[3],
            "is_active": user[4],
            "is_premium": user[5]
        }
    return None

def get_user_by_phone(db: sqlite3.Connection, phone: str):
    """Get user by phone"""
    cursor = db.cursor()
    cursor.execute(
        "SELECT id, email, phone, auth_provider, is_active, is_premium FROM users WHERE phone = ?",
        (phone,)
    )
    user = cursor.fetchone()
    
    if user:
        return {
            "id": user[0],
            "email": user[1],
            "phone": user[2],
            "auth_provider": user[3],
            "is_active": user[4],
            "is_premium": user[5]
        }
    return None

def handle_social_auth(db: sqlite3.Connection, provider: str, email: str, user_info: dict):
    """Handle Google/Apple sign-in"""
    # Check if user exists
    user = get_user_by_email(db, email)
    
    if user:
        # Update auth provider if different
        if user["auth_provider"] != provider:
            cursor = db.cursor()
            cursor.execute(
                "UPDATE users SET auth_provider = ? WHERE id = ?",
                (provider, user["id"])
            )
            db.commit()
        return user["id"]
    else:
        # Create new user
        user_id = create_user(db, None, email, None, provider)
        return user_id
