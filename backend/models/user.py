# user.py - Enhanced user models
from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
from datetime import datetime

# ============= Authentication Models =============

class OTPRequest(BaseModel):
    phone: str = Field(..., min_length=10, max_length=15)
    
    @validator('phone')
    def validate_phone(cls, v):
        # Remove spaces and special characters
        cleaned = ''.join(filter(str.isdigit, v))
        if len(cleaned) < 10:
            raise ValueError('Phone number must be at least 10 digits')
        return v

class OTPVerify(BaseModel):
    phone: str
    otp_code: str = Field(..., min_length=6, max_length=6)

class UserRegister(BaseModel):
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=8)
    auth_provider: Optional[str] = 'email'  # email, phone, google, apple
    full_name: Optional[str] = None

class UserLogin(BaseModel):
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    password: Optional[str] = None

class SocialAuthRequest(BaseModel):
    provider: str = Field(..., pattern='^(google|apple)$')
    token: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int

class TokenRefresh(BaseModel):
    refresh_token: str

# ============= User Profile Models =============

class User(BaseModel):
    id: int
    email: Optional[str] = None
    phone: Optional[str] = None
    auth_provider: Optional[str] = None
    is_active: bool = True
    is_premium: bool = False
    created_at: datetime

    class Config:
        from_attributes = True

class StudentProfileCreate(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=100)
    nationality: Optional[str] = None
    date_of_birth: Optional[str] = None  # YYYY-MM-DD format
    gpa: Optional[float] = Field(None, ge=0.0, le=4.0)
    budget: Optional[int] = Field(None, ge=0)
    preferred_country: Optional[str] = None
    preferred_major: Optional[str] = None
    learning_style: Optional[str] = None
    career_goal: Optional[str] = None
    bio: Optional[str] = Field(None, max_length=500)

class StudentProfileUpdate(BaseModel):
    full_name: Optional[str] = Field(None, min_length=2, max_length=100)
    nationality: Optional[str] = None
    date_of_birth: Optional[str] = None
    gpa: Optional[float] = Field(None, ge=0.0, le=4.0)
    budget: Optional[int] = Field(None, ge=0)
    preferred_country: Optional[str] = None
    preferred_major: Optional[str] = None
    learning_style: Optional[str] = None
    career_goal: Optional[str] = None
    bio: Optional[str] = Field(None, max_length=500)

class StudentProfile(BaseModel):
    id: int
    user_id: int
    full_name: Optional[str] = None
    nationality: Optional[str] = None
    date_of_birth: Optional[str] = None
    gpa: Optional[float] = None
    budget: Optional[int] = None
    preferred_country: Optional[str] = None
    preferred_major: Optional[str] = None
    learning_style: Optional[str] = None
    career_goal: Optional[str] = None
    bio: Optional[str] = None
    profile_image: Optional[str] = None

    class Config:
        from_attributes = True

class UserWithProfile(BaseModel):
    user: User
    profile: Optional[StudentProfile] = None

# ============= Document Models =============

class DocumentUpload(BaseModel):
    doc_type: str
    file_name: str
    file_size: int

class Document(BaseModel):
    id: int
    user_id: int
    doc_type: str
    file_path: str
    file_name: str
    file_size: int
    uploaded_at: datetime

    class Config:
        from_attributes = True

# ============= Password Management =============

class PasswordChange(BaseModel):
    current_password: str
    new_password: str = Field(..., min_length=8)

class PasswordReset(BaseModel):
    email: EmailStr

class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str = Field(..., min_length=8)
