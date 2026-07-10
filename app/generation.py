"""Build answer payloads from retrieved chunks."""

def build_answer_stub(question: str, matches: list[dict]) -> dict:
    if not matches:
        return {
            "question": question,
            "answer": "No relevant context was retrieved.",
            "sources": [],
            "confidence_notes": "No chunks were retrieved, so the stub cannot answer.",
        }

    context_lines = []
    sources = []
    for match in matches:
        context_lines.append(str(match["text"]))
        sources.append(
            {
                "chunk_id": match["chunk_id"],
                "chunk_index": match["chunk_index"],
                "score": match["score"],
                "text_preview": match["text"][:120],
            }
        )

    answer = " ".join(context_lines)
    return {
        "question": question,
        "answer": answer,
        "sources": sources,
        "confidence_notes": "This is a deterministic answer stub based only on retrieved chunks.",
    }
