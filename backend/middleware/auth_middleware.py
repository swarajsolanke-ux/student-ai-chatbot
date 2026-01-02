from fastapi.responses import HTMLResponse
from fastapi import HTTPException, Security, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from config import settings
from datetime import datetime
import sqlite3

security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Security(security)):
    """
    Validates JWT token and returns current user
    """
    token = credentials.credentials
    
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        
        user_id: int = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Check if token is expired
        exp = payload.get("exp")
        if exp and datetime.fromtimestamp(exp) < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        return {"user_id": user_id, "email": payload.get("email")}
        
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

def get_current_active_user(current_user: dict = Depends(get_current_user)):
    """
    Validates that the current user is active
    """
    from sqlite import get_db
    
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT is_active FROM users WHERE id = ?", (current_user["user_id"],))
    result = cursor.fetchone()
    
    if not result or not result[0]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user account"
        )
    
    return current_user

def require_premium(current_user: dict = Depends(get_current_active_user)):
    """
    Requires user to have premium access
    """
    from sqlite import get_db
    
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT is_premium FROM users WHERE id = ?", (current_user["user_id"],))
    result = cursor.fetchone()
    
    if not result or not result[0]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Premium subscription required for this feature"
        )
    
    return current_user

# Optional authentication (doesn't fail if no token)
def get_optional_user(credentials: HTTPAuthorizationCredentials = Security(security)):
    """
    Returns user if authenticated, None otherwise
    """
    if credentials is None:
        return None
    
    try:
        return get_current_user(credentials)
    except HTTPException:
        return None
