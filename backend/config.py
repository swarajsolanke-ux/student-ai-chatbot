
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

print(f"BASE_DIR:{BASE_DIR}")
DB_PATH = os.path.join(BASE_DIR, "chatbot.db")
UPLOAD_DIR = os.path.join(BASE_DIR, "storage/uploads")
CHROMA_DIR = os.path.join(BASE_DIR, "../chroma_db")

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(CHROMA_DIR, exist_ok=True)
