import os
import aiofiles
from fastapi import UploadFile
from config import settings
from typing import Optional
import hashlib
from datetime import datetime

async def save_upload_file(file: UploadFile, user_id: int, category: str = "general") -> dict:
    """
    Save an uploaded file to storage
    Returns dict with file info
    """
    # Validate file extension
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in settings.ALLOWED_EXTENSIONS:
        raise ValueError(f"File type {file_ext} not allowed. Allowed types: {settings.ALLOWED_EXTENSIONS}")
    
    # Create user directory
    user_dir = os.path.join(settings.UPLOAD_DIR, str(user_id), category)
    os.makedirs(user_dir, exist_ok=True)
    
    # Generate unique filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_filename = file.filename.replace(" ", "_")
    filename = f"{timestamp}_{safe_filename}"
    file_path = os.path.join(user_dir, filename)
    
    # Save file
    try:
        # Read file content
        contents = await file.read()
        file_size = len(contents)
        
        # Check file size
        if file_size > settings.MAX_FILE_SIZE:
            raise ValueError(f"File size exceeds maximum allowed size of {settings.MAX_FILE_SIZE / (1024*1024)}MB")
        
        # Write file
        async with aiofiles.open(file_path, 'wb') as f:
            await f.write(contents)
        
        # Calculate file hash for integrity
        file_hash = hashlib.md5(contents).hexdigest()
        
        return {
            "file_path": file_path,
            "file_name": safe_filename,
            "file_size": file_size,
            "file_hash": file_hash,
            "file_ext": file_ext
        }
        
    except Exception as e:
        # Clean up if error
        if os.path.exists(file_path):
            os.remove(file_path)
        raise e

async def delete_file(file_path: str) -> bool:
    """Delete a file from storage"""
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
        return False
    except Exception as e:
        print(f"Error deleting file {file_path}: {e}")
        return False

def get_file_url(file_path: str) -> str:
    """Convert file path to accessible URL"""
    # In production, this would return a CDN or signed URL
    # For now, return relative path from upload directory
    relative_path = file_path.replace(settings.UPLOAD_DIR, "/uploads")
    return relative_path

def validate_file_type(filename: str, allowed_types: Optional[set] = None) -> bool:
    """Validate file type"""
    if allowed_types is None:
        allowed_types = settings.ALLOWED_EXTENSIONS
    
    file_ext = os.path.splitext(filename)[1].lower()
    return file_ext in allowed_types

def get_file_size_mb(file_size_bytes: int) -> float:
    """Convert bytes to MB"""
    return round(file_size_bytes / (1024 * 1024), 2)

# Document-specific helpers
async def save_document(file: UploadFile, user_id: int, doc_type: str) -> dict:
    """Save a user document"""
    return await save_upload_file(file, user_id, f"documents/{doc_type}")

async def save_profile_image(file: UploadFile, user_id: int) -> dict:
    """Save a profile image"""
    # Only allow image types
    allowed_images = {'.jpg', '.jpeg', '.png'}
    if not validate_file_type(file.filename, allowed_images):
        raise ValueError("Only JPG and PNG images are allowed for profile pictures")
    
    return await save_upload_file(file, user_id, "profile")

async def save_university_media(file: UploadFile, university_id: int, media_type: str) -> dict:
    """Save university image or video"""
    allowed_media = {'.jpg', '.jpeg', '.png', '.mp4', '.webm'}
    if not validate_file_type(file.filename, allowed_media):
        raise ValueError(f"Only image and video files are allowed. Got: {file.filename}")
    
    category = f"universities/{university_id}/{media_type}"
    return await save_upload_file(file, 0, category)  # User ID 0 for admin uploads
