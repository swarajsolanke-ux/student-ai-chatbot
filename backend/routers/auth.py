
from fastapi import APIRouter, HTTPException, Depends, status
from models.user import (
    OTPRequest, OTPVerify, UserRegister, UserLogin,
    TokenResponse, UserWithProfile, StudentProfileCreate
)
from services import auth_service, otp_service, notification_service
from sqlite import get_db
from middleware.auth_middleware import get_current_active_user
import sqlite3

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/send-otp", status_code=status.HTTP_200_OK)
def send_otp(request: OTPRequest, db: sqlite3.Connection = Depends(get_db)):
    """Send OTP to phone number"""
    otp_code, success = otp_service.create_otp(db, request.phone)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to send OTP"
        )
    
    return {
        "message": "OTP sent successfully",
        "phone": request.phone,
        "expires_in_minutes": 10
    }

@router.post("/verify-otp", response_model=TokenResponse)
def verify_otp(request: OTPVerify, db: sqlite3.Connection = Depends(get_db)):
    """Verify OTP and login/register user"""
    # Verify OTP
    is_valid = otp_service.verify_otp(db, request.phone, request.otp_code)
    
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired OTP"
        )
    
    # Check if user exists
    user = auth_service.get_user_by_phone(db, request.phone)
    
    if not user:
        # Create new user
        user_id = auth_service.create_user(db, request.phone, None, None, "phone")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create user"
            )
    else:
        user_id = user["id"]
    
    # Generate tokens
    tokens = auth_service.create_tokens_for_user(user_id, None)
    
    return TokenResponse(**tokens)

@router.post("/register", response_model=TokenResponse)
def register(request: UserRegister, db: sqlite3.Connection = Depends(get_db)):
    """Register new user with email/password"""
    if request.auth_provider == "email" and (not request.email or not request.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email and password required for email registration"
        )
    
    # Create user
    user_id = auth_service.create_user(
        db, request.phone, request.email, request.password, request.auth_provider
    )
    
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email or phone already exists"
        )
    
    # Create profile if full_name provided
    if request.full_name:
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO student_profiles (user_id, full_name) VALUES (?, ?)",
            (user_id, request.full_name)
        )
        db.commit()
    # Send welcome notification
    notification_service.create_notification(
        db, user_id,
        "Welcome to University Recommendation Platform!",
        "Complete your profile and take the assessment to get personalized university recommendations.",
        "success",
        "/profile"
    )
    
    # Generate tokens
    tokens = auth_service.create_tokens_for_user(user_id, request.email)
    
    return TokenResponse(**tokens)

@router.post("/login", response_model=TokenResponse)
def login(request: UserLogin, db: sqlite3.Connection = Depends(get_db)):
    """Login with email/password"""
    if not request.email or not request.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email and password required"
        )
    
    user = auth_service.authenticate_user(db, request.email, request.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    tokens = auth_service.create_tokens_for_user(user["id"], user["email"])
    
    return TokenResponse(**tokens)

@router.get("/me")
def get_current_user_info(
    current_user: dict = Depends(get_current_active_user),
    db: sqlite3.Connection = Depends(get_db)
):
    """Get current user information with profile"""
    user_id = current_user["user_id"]
    
    # Get user info
    cursor = db.cursor()
    cursor.execute(
        "SELECT id, email, phone, auth_provider, is_active, is_premium, created_at FROM users WHERE id = ?",
        (user_id,)
    )
    user_row = cursor.fetchone()
    
    if not user_row:
        raise HTTPException(status_code=404, detail="User not found")
    
    user_data = {
        "id": user_row[0],
        "email": user_row[1],
        "phone": user_row[2],
        "auth_provider": user_row[3],
        "is_active": bool(user_row[4]),
        "is_premium": bool(user_row[5]),
        "created_at": user_row[6]
    }
    
    # Get profile
    cursor.execute(
        """SELECT id, user_id, full_name, nationality, date_of_birth, gpa, budget,
                  preferred_country, preferred_major, learning_style, career_goal, bio, profile_image
           FROM student_profiles WHERE user_id = ?""",
        (user_id,)
    )
    profile_row = cursor.fetchone()
    
    profile_data = None
    if profile_row:
        profile_data = {
            "id": profile_row[0],
            "user_id": profile_row[1],
            "full_name": profile_row[2],
            "nationality": profile_row[3],
            "date_of_birth": profile_row[4],
            "gpa": profile_row[5],
            "budget": profile_row[6],
            "preferred_country": profile_row[7],
            "preferred_major": profile_row[8],
            "learning_style": profile_row[9],
            "career_goal": profile_row[10],
            "bio": profile_row[11],
            "profile_image": profile_row[12]
        }
    
    return {
        "user": user_data,
        "profile": profile_data
    }

@router.post("/profile/create")
def create_profile(
    profile: StudentProfileCreate,
    current_user: dict = Depends(get_current_active_user),
    db: sqlite3.Connection = Depends(get_db)
):
    """Create or update student profile"""
    user_id = current_user["user_id"]
    cursor = db.cursor()
    
    # Check if profile exists
    cursor.execute("SELECT id FROM student_profiles WHERE user_id = ?", (user_id,))
    existing = cursor.fetchone()
    
    if existing:
        # Update
        cursor.execute(
            """UPDATE student_profiles 
               SET full_name = ?, nationality = ?, date_of_birth = ?, gpa = ?, budget = ?,
                   preferred_country = ?, preferred_major = ?, learning_style = ?, career_goal = ?, bio = ?
               WHERE user_id = ?""",
            (profile.full_name, profile.nationality, profile.date_of_birth, profile.gpa, profile.budget,
             profile.preferred_country, profile.preferred_major, profile.learning_style, profile.career_goal,
             profile.bio, user_id)
        )
    else:
        # Create
        cursor.execute(
            """INSERT INTO student_profiles 
               (user_id, full_name, nationality, date_of_birth, gpa, budget, preferred_country,
                preferred_major, learning_style, career_goal, bio)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (user_id, profile.full_name, profile.nationality, profile.date_of_birth, profile.gpa, profile.budget,
             profile.preferred_country, profile.preferred_major, profile.learning_style, profile.career_goal, profile.bio)
        )
    
    db.commit()
    
    return {"message": "Profile updated successfully"}

@router.post("/logout")
def logout(current_user: dict = Depends(get_current_active_user)):
    """Logout user (client should discard tokens)"""
    return {"message": "Logged out successfully"}
