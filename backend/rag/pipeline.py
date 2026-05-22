import json
import asyncio
from typing import List, Dict, Any, AsyncGenerator
from google import genai
from google.genai import types
from rag.retriever import HybridRetriever
from rag.reranker import Reranker
from rag.chunker import AdvancedChunker
from utils.pdf_processor import PDFProcessor
from config import GEMINI_API_KEY, LLM_MODEL, TOP_K_RETRIEVAL, TOP_K_RERANK
import os

SYSTEM_PROMPT = """You are an elite research assistant with access to specific documents. Your task is to provide comprehensive, accurate, and insightful answers based EXCLUSIVELY on the retrieved document context provided.

INSTRUCTIONS:
1. Answer thoroughly and in depth — do NOT give short answers. Expand on every relevant point.
2. Always cite your sources by referencing the page number and document name like [Source 1, Page 3].
3. If multiple chunks support a point, synthesize them cohesively.
4. Structure your response with clear sections using markdown headers.
5. If the context is insufficient, explicitly say so.
6. Never hallucinate or add information not present in the context.
7. Use markdown formatting for clarity (headers, bullets, bold key terms).
8. At the end, always list all source pages you referenced.
"""

class RAGPipeline:
    def __init__(self):
        self.retriever = HybridRetriever()
        self.chunker   = AdvancedChunker()
        self.pdf_proc  = PDFProcessor()
        self.client    = genai.Client(api_key=GEMINI_API_KEY)
        self._reranker = None

    @property
    def reranker(self):
        if self._reranker is None:
            self._reranker = Reranker.get_instance()
        return self._reranker

    def ingest_pdf(self, file_path: str) -> Dict[str, Any]:
        print(f"[Pipeline] Ingesting: {file_path}")
        pages = self.pdf_proc.extract(file_path)
        if not pages:
            raise ValueError("No text could be extracted from the PDF.")
        chunks = self.chunker.chunk(pages)
        count  = self.retriever.add_documents(chunks)
        title  = pages[0]["metadata"].get("title", os.path.basename(file_path))
        return {
            "pages":  len(pages),
            "chunks": count,
            "title":  title,
            "source": os.path.basename(file_path),
        }

    def query(self, question: str, use_reranker: bool = True) -> Dict[str, Any]:
        candidates = self.retriever.retrieve(question, top_k=TOP_K_RETRIEVAL)
        if not candidates:
            return {
                "answer": "No relevant documents found. Please upload a PDF first.",
                "sources": [],
                "chunks_retrieved": 0,
            }
        final_docs = (
            self.reranker.rerank(question, candidates, top_k=TOP_K_RERANK)
            if use_reranker and len(candidates) > 1
            else candidates[:TOP_K_RERANK]
        )
        context = self._build_context(final_docs)
        prompt  = f"SYSTEM: {SYSTEM_PROMPT}\n\nRETRIEVED CONTEXT:\n{context}\n\n---\n\nQUESTION: {question}"
        response = self.client.models.generate_content(
            model=LLM_MODEL,
            contents=prompt,
        )
        return {
            "answer": response.text,
            "sources": self._format_sources(final_docs),
            "chunks_retrieved": len(final_docs),
        }

    async def query_stream(
        self,
        question: str,
        use_reranker: bool = True,
    ) -> AsyncGenerator[str, None]:
        candidates = self.retriever.retrieve(question, top_k=TOP_K_RETRIEVAL)
        if not candidates:
            yield json.dumps({
                "type": "error",
                "message": "No relevant documents found. Please upload a PDF first.",
            })
            return

        final_docs = (
            self.reranker.rerank(question, candidates, top_k=TOP_K_RERANK)
            if use_reranker and len(candidates) > 1
            else candidates[:TOP_K_RERANK]
        )

        # Send sources first
        yield json.dumps({"type": "sources", "sources": self._format_sources(final_docs)}) + "\n"

        context = self._build_context(final_docs)
        prompt  = f"SYSTEM: {SYSTEM_PROMPT}\n\nRETRIEVED CONTEXT:\n{context}\n\n---\n\nQUESTION: {question}"

        # Run blocking Gemini stream in thread pool to avoid blocking event loop
        loop = asyncio.get_event_loop()

        def run_stream():
            chunks = []
            for chunk in self.client.models.generate_content_stream(
                model=LLM_MODEL,
                contents=prompt,
            ):
                try:
                    if chunk.text:
                        chunks.append(chunk.text)
                except Exception:
                    pass
            return chunks

        tokens = await loop.run_in_executor(None, run_stream)
        for token in tokens:
            yield json.dumps({"type": "token", "token": token}) + "\n"

        yield json.dumps({"type": "done"}) + "\n"

    def _build_context(self, docs: List[Dict[str, Any]]) -> str:
        parts = []
        for i, doc in enumerate(docs):
            meta  = doc.get("metadata", {})
            score = doc.get("rerank_score", doc.get("rrf_score", 0))
            parts.append(
                f"[Source {i+1}] (File: {meta.get('source','Unknown')} | "
                f"Page: {meta.get('page_number','?')} | Relevance: {score:.3f})\n{doc['text']}"
            )
        return ("\n\n" + "-" * 60 + "\n\n").join(parts)

    def _format_sources(self, docs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        seen, sources = set(), []
        for i, doc in enumerate(docs):
            meta = doc.get("metadata", {})
            key  = (meta.get("source", ""), meta.get("page_number", 0))
            if key in seen:
                continue
            seen.add(key)
            sources.append({
                "index":           i + 1,
                "source":          meta.get("source", "Unknown"),
                "page":            meta.get("page_number", "?"),
                "total_pages":     meta.get("total_pages", "?"),
                "title":           meta.get("title", ""),
                "snippet":         doc["text"][:300] + "..." if len(doc["text"]) > 300 else doc["text"],
                "relevance_score": round(doc.get("rerank_score", doc.get("rrf_score", 0)), 4),
            })
        return sources

    def get_stats(self) -> Dict[str, Any]:
        return {
            "total_chunks": self.retriever.get_document_count(),
            "sources":      self.retriever.get_all_sources(),
        }

    def clear_knowledge_base(self):
        self.retriever.clear()
