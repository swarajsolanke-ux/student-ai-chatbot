
from langchain_ollama import OllamaEmbeddings
import chromadb
from config import CHROMA_DIR

client = chromadb.Client()
collection = client.get_or_create_collection("students")

embedder = OllamaEmbeddings(model="nomic-embed-text:latest")
