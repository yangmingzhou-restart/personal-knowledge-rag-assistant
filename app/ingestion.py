import csv
from io import StringIO, BytesIO
from pathlib import Path
from docx import Document
from pypdf import PdfReader

SUPPORTED_EXTENSIONS = {".txt", ".md", ".csv", ".docx", ".pdf"}

class UnsupportedFileTypeError(ValueError):
    """
    UnsupportedFileTypeError: when the file type is not supported
    """
    pass


def extract_text(filename: str, content: bytes) -> str:
    """
    filename: str, the filename of the file
    content: bytes, the content of the file
    return: str, the text extracted from the file
            it will be used to chunk_text()
    """
    extension = Path(filename).suffix.lower()

    if extension in {".txt", ".md"}:
        return content.decode("utf-8")

    if extension == ".csv":
        return _extract_csv_text(content)
    
    if extension == ".docx":
        return _extract_docx_text(content)
    
    if extension == ".pdf":
        return _extract_pdf_text(content)

    raise UnsupportedFileTypeError(f"Unsupported file type: {extension}")


def _extract_csv_text(content: bytes) -> str:
    """
    content: bytes, the content of the csv file
    return: str, the text extracted from the csv file
            it will be used to chunk_text()
    """
    decoded = content.decode("utf-8")
    reader = csv.DictReader(StringIO(decoded))

    lines = []
    for row in reader:
        parts = []
        for key, value in row.items():
            parts.append(f"{key}={value}")
        lines.append(", ".join(parts))

    return "\n".join(lines)

def _extract_docx_text(content: bytes) -> str:
    """
    content: bytes, the content of the docx file
    return: str, the text extracted from the docx file
            it will be used to chunk_text()
    """
    doc = Document(BytesIO(content))
    paragraphs = [p.text.strip() for p in doc.paragraphs if p.text.strip()]

    text = "\n\n".join(paragraphs).strip()
    if not text:
        raise ValueError("No readable text found in DOCX.")
    return text

def _extract_pdf_text(content: bytes) -> str:
    """
    content: bytes, the content of the pdf file
    return: str, the text extracted from the pdf file
            it will be used to chunk_text()
    """
    reader = PdfReader(BytesIO(content))
    page_texts = []

    for page in reader.pages:
        # extract_text() may return None for scanned or image-only pages.
        text = page.extract_text() or "" # maybe: None or ""
        if text.strip():
            page_texts.append(text.strip())

    text = "\n\n".join(page_texts).strip()
    if not text:
        raise ValueError("No readable text found in PDF. Scanned PDFs are not supported yet.")
    return text
