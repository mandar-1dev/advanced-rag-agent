from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from backend.api.routes import router
from backend.config import settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Advanced RAG Agent")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins in development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api")

@app.get("/")
async def root():
    return {
        "message": "Advanced RAG Agent is running",
        "environment": settings.environment,
    }

@app.on_event("startup")
async def startup_event():
    logger.info(f"Application starting in {settings.environment} environment")
