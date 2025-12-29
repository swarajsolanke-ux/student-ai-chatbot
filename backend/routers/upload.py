# upload.py - Part of routers module
from fastapi import APIRouter, UploadFile
from config import Settings
import shutil, os

router = APIRouter(prefix="/upload")

@router.post("/")
def upload(file: UploadFile):
    path = os.path.join(Settings.UPLOAD_DIR, file.filename)
    with open(path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    return {"file": file.filename}
