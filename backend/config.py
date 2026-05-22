import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

LLM_MODEL = "gemini-1.5-flash"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
RERANKER_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"

CHUNK_SIZE = 512
CHUNK_OVERLAP = 64
TOP_K_RETRIEVAL = 10
TOP_K_RERANK = 5
SIMILARITY_THRESHOLD = 0.3

VECTORSTORE_DIR = "./vectorstore"
COLLECTION_NAME = "rag_documents"

HOST = "0.0.0.0"
PORT = 8000
ALLOWED_ORIGINS = ["http://localhost:5173", "http://localhost:3000"]

UPLOAD_DIR = "./uploads"
MAX_FILE_SIZE_MB = 50
ALLOWED_EXTENSIONS = {".pdf"}
