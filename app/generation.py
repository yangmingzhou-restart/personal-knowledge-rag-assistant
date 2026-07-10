"""Build answer payloads from retrieved chunks and an LLM client."""
from app.llm import LLMClient, get_llm_client
from app.prompts import build_grounded_prompt

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

def build_sources(matches: list[dict]) -> list[dict]:
    return [
        {
            "chunk_id": match["chunk_id"],
            "chunk_index": match["chunk_index"],
            "score": match["score"],
            "text_preview": match["text"][:120],
        }
        for match in matches
    ]


def build_llm_answer(
        question: str, 
        matches: list[dict], 
        llm_client: LLMClient | None = None,
    ) -> dict:
    client = llm_client or get_llm_client()
    prompt = build_grounded_prompt(question=question, matches=matches)
    llm_result = client.generate(prompt)
    
    return {
        "question": question,
        "answer": llm_result["answer"],
        "provider": llm_result["provider"],
        "sources": build_sources(matches),
        "confidence_notes": "Answer generated from a grounded prompt built from retrieved chunks.",
    }
    
    