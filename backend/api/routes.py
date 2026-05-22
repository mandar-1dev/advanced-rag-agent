from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
import google.generativeai as genai
import asyncio
import logging
from backend.api.models import QueryRequest, QueryResponse
from backend.config import settings

logger = logging.getLogger(__name__)

# Configure Gemini API
genai.configure(api_key=settings.gemini_api_key)
model = genai.GenerativeModel('gemini-2.0-flash')

router = APIRouter()

QUERY_TIMEOUT = 60  # 60 seconds timeout

@router.post("/query", response_model=QueryResponse)
async def handle_query(payload: QueryRequest):
    try:
        # Prepare context from documents
        context = "\n".join(payload.documents) if payload.documents else ""
        
        # Build prompt
        prompt = f"""You are an AI assistant answering questions based on provided documents.
        
Documents:
{context}

Question: {payload.query}

Please provide a helpful and accurate answer based on the documents provided."""
        
        # Call Gemini API with timeout using asyncio.wait_for
        loop = asyncio.get_event_loop()
        
        response = await asyncio.wait_for(
            loop.run_in_executor(None, lambda: model.generate_content(prompt)),
            timeout=QUERY_TIMEOUT
        )
        
        return QueryResponse(
            query=payload.query,
            results=[{"answer": response.text, "source": "Gemini 2.0 Flash"}],
            metadata={"source": "Gemini API", "model": "gemini-2.0-flash"},
        )
    except asyncio.TimeoutError:
        logger.error(f"Query timeout for: {payload.query}")
        raise HTTPException(status_code=504, detail="Query processing timed out. Please try again.")
    except Exception as e:
        logger.error(f"Query error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")
