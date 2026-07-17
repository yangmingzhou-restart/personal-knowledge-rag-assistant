import pytest
from io import BytesIO

from docx import Document
from pypdf import PdfReader, PdfWriter

from app.ingestion import UnsupportedFileTypeError, extract_text


def test_extract_text_from_txt():
    text = extract_text("note.txt", "hello rag".encode("utf-8"))

    assert text == "hello rag"


def test_extract_text_from_markdown():
    text = extract_text("readme.md", "# Title\n\ncontent".encode("utf-8"))

    assert "Title" in text
    assert "content" in text


def test_extract_text_from_csv():
    content = "name,score\nAlice,95\nBob,88\n".encode("utf-8")
    text = extract_text("scores.csv", content)

    assert "name=Alice, score=95" in text
    assert "name=Bob, score=88" in text


def test_extract_text_rejects_unsupported_file_type():
    with pytest.raises(UnsupportedFileTypeError):
        extract_text("image.png", b"fake")

def build_sample_docx_bytes(text: str) -> bytes:
    buffer = BytesIO()
    document = Document()
    document.add_paragraph(text)
    document.save(buffer)
    return buffer.getvalue()

def build_empty_pdf_bytes() -> bytes:
    buffer = BytesIO()
    writer = PdfWriter()
    writer.add_blank_page(width=72, height=72)
    writer.write(buffer)
    return buffer.getvalue()

def test_extract_text_from_docx_returns_text():
    content = build_sample_docx_bytes("RAG upload supported Word files.")

    text = extract_text("sample.docx", content)

    assert "RAG upload supported Word files." in text

def test_extract_text_from_empty_pdf_raises_clear_error():
    content = build_empty_pdf_bytes()

    with pytest.raises(ValueError, match="No readable text"):
        extract_text("empty.pdf", content)

