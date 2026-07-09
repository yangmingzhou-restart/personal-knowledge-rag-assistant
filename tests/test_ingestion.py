import pytest

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
