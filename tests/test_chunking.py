from app.chunking import chunk_text

def test_short_text_returns_one_chunk():
    chunks = chunk_text("hello rag", chunk_size=50, overlap=10)
    
    assert len(chunks) == 1
    assert chunks[0]["chunk_index"] == 0
    assert chunks[0]["text"] == "hello rag"
    assert chunks[0]["start_char"] == 0
    assert chunks[0]["end_char"] == len("hello rag")

def test_long_text_returns_multiple_chunks_with_overlap():
    text = "abcdefghijklmnopqrstuvwxyz"

    chunks = chunk_text(text, chunk_size=10, overlap=2)
    
    assert len(chunks) == 3
    assert chunks[0]["text"] == "abcdefghij"
    assert chunks[1]["text"] == "ijklmnopqr"
    assert chunks[2]["text"] == "qrstuvwxyz"

def test_empty_text_returns_empty_list():
    assert chunk_text("") == []

def test_invalid_chunk_size_raises_value_error():
    try:
        chunk_text("hello", chunk_size=0, overlap=0)
    except ValueError as exc:
        assert "chunk_size" in str(exc)
    else:
        raise AssertionError("Expected ValueError")
    
def test_overalp_must_be_smaller_than_chunk_size():
    try:
        chunk_text("hello", chunk_size=10, overlap=10)
    except ValueError as exc:
        assert "overlap" in str(exc)
    else:
        raise AssertionError("Expected ValueError")
