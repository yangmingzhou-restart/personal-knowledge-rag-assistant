from app.prompts import build_grounded_prompt

def test_build_grounded_prompt_includes_question_and_context():
    matches = [
        {
            "chunk_id": "chunk_1",
            "chunk_index": 0,
            "text": "RAG uses retrieved context.",
            "score": 0.91,
        }
    ]

    prompt = build_grounded_prompt(
        question="What does RAG use?",
        matches=matches,
    )

    assert "What does RAG use?" in prompt
    assert "RAG uses retrieved context." in prompt
    assert "chunk_1" in prompt
    assert "0.91" in prompt

def test_build_grounded_prompt_requires_context_only_answer():
    prompt = build_grounded_prompt(
        question="unknown?",
        matches=[],
    )

    assert "No context was retrieved." in prompt
    assert "If the context is insufficient" in prompt