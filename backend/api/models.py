from pydantic import BaseModel, Field
from typing import List, Optional, Any


class QueryRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=2000)
    documents: list = Field(default_factory=list)
    use_reranker: bool = True
    stream: bool = False


class SourceDoc(BaseModel):
    index: int
    source: str
    page: Any
    total_pages: Any
    title: str
    snippet: str
    relevance_score: float


class QueryResponse(BaseModel):
    query: str
    results: list
    metadata: dict


class IngestResponse(BaseModel):
    success: bool
    message: str
    pages: Optional[int] = None
    chunks: Optional[int] = None
    title: Optional[str] = None
    source: Optional[str] = None


class StatsResponse(BaseModel):
    total_chunks: int
    sources: List[str]


class ClearResponse(BaseModel):
    success: bool
    message: str