from typing import List
from PyPDF2 import PdfReader


def extract_text_from_pdf(path: str) -> List[str]:
    reader = PdfReader(path)
    pages = []
    for page in reader.pages:
        pages.append(page.extract_text() or "")
    return pages
