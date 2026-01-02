
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # Database
    DATABASE_NAME = os.getenv("DATABASE_NAME", "University.db")

    # JWT Settings
    SECRET_KEY = os.getenv("SECRET_KEY", "bcbe7c26cb50d2ebe7e5e7b6f7a58464316791a568c46a053b6803852a07eaee")
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  
    REFRESH_TOKEN_EXPIRE_DAYS = 30
    
    # File Upload
    UPLOAD_DIR = os.getenv("UPLOAD_DIR", "./backend/storage/uploads")
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS = {'.pdf', '.jpg', '.jpeg', '.png', '.doc', '.docx'}
    
    # Ollama Settings
    OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "gemma2:2b")
    
    # ChromaDB Settings
    CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH", "./chroma_db")
    CHROMA_COLLECTION = "university_embeddings"
    
    # OTP Settings (Simulated - replace with real SMS service in production)
    OTP_EXPIRY_MINUTES = 10
    OTP_LENGTH = 6
    SMS_PROVIDER = os.getenv("SMS_PROVIDER", "simulated")# twilio, nexmo, simulated
    # TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", "")
    # TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "")
    # TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER", "")
    
    # # Social Auth
    # GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "")
    # GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET", "")
    # APPLE_CLIENT_ID = os.getenv("APPLE_CLIENT_ID", "")
    # APPLE_TEAM_ID = os.getenv("APPLE_TEAM_ID", "")
    # APPLE_KEY_ID = os.getenv("APPLE_KEY_ID", "")
    
    # # Payment Gateways (Simulated)
    # KNET_MERCHANT_ID = os.getenv("KNET_MERCHANT_ID", "")
    # KNET_API_KEY = os.getenv("KNET_API_KEY", "")
    # PAYMENT_MODE = os.getenv("PAYMENT_MODE", "simulated")  # live, simulated
    
    # # Email Settings
    # SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    # SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
    # SMTP_USERNAME = os.getenv("SMTP_USERNAME", "")
    # SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
    # FROM_EMAIL = os.getenv("FROM_EMAIL", "noreply@university-platform.com")
    
    # Frontend URL
    FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:8000")
    
    # Admin
    ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "swarajolanke02@gmail.com")
    
    # Features
    ENABLE_PREMIUM_FEATURES = os.getenv("ENABLE_PREMIUM_FEATURES", "true").lower() == "true"
    ENABLE_SOCIAL_AUTH = os.getenv("ENABLE_SOCIAL_AUTH", "true").lower() == "true"
    
    # Pagination
    DEFAULT_PAGE_SIZE = 20
    MAX_PAGE_SIZE = 100
    
    # AI Assessment
    PERSONALITY_QUESTIONS_COUNT = 15
    ACADEMIC_QUESTIONS_COUNT = 10
    INTERESTS_QUESTIONS_COUNT = 10
    
    # Recommendation Limits
    MIN_MAJOR_RECOMMENDATIONS = 3
    MAX_MAJOR_RECOMMENDATIONS = 7
    MAX_UNIVERSITY_RECOMMENDATIONS = 10
    MAX_COMPARISON_COUNT = 3

settings = Settings()


os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
