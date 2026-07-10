

def build_grounded_prompt(question: str, matches: list[dict]) -> str:
    context_blocks = []

    # 构建上下文块，每个块包含chunk_id、index、score和text
    for match in matches:
        context_blocks.append(
            "\n".join(
                [
                    f"Source chunk_id: {match.get('chunk_id')}",
                    f"Chunk index: {match.get('chunk_index')}",
                    f"Retrieval score: {match.get('score')}",
                    "Text:",
                    str(match.get("text", ""))
                ]
            )
        )
    
    context = "\n\n---\n\n".join(context_blocks) if context_blocks else "No context was retrieved."

    return f"""You are a source-grounded RAG assistant

Rules:
- Answer the question using only the provided context.
- If the context is insufficient, say that the context is insufficient.
- Do not use outside knowledge.
- Keep the answer concise.
- Mention the source chunk_id when useful.

Question:
{question}

Context:
{context}
"""
