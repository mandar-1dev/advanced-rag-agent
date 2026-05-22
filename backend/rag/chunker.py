from typing import List

def chunk_text(documents: List[str], chunk_size: int = 500, overlap: int = 50) -> List[str]:
    chunks = []
    for doc in documents:
        start = 0
        while start < len(doc):
            end = min(start + chunk_size, len(doc))
            chunks.append(doc[start:end])
            if end == len(doc):
                break
            start = end - overlap
    return chunks
