from pathlib import Path

from eval.run_retrieval_evaluation import (
    UNKNOWN_ANCHOR,
    extract_anchor_groups,
    extract_anchors_from_text,
    judge,
    parse_evaluation_questions,
    render_results_markdown,
)


def test_parse_evaluation_questions_reads_id_question_and_anchor(tmp_path):
    path = tmp_path / "evaluation-questions.md"
    path.write_text(
        """
### Q1 - Project purpose

- Question: What is the main purpose?
- Expected anchor: `[ANCHOR-PROJECT-PURPOSE]`
- Expected evidence:
  - grounded answers

### Q2 - Upload pipeline

- Question: What happens after upload?
- Expected anchor: [ANCHOR-UPLOAD-PIPELINE]
""",
        encoding="utf-8",
    )

    questions = parse_evaluation_questions(path)

    assert questions == [
        {
            "id": "Q1",
            "question": "What is the main purpose?",
            "expected_anchor": "[ANCHOR-PROJECT-PURPOSE]",
        },
        {
            "id": "Q2",
            "question": "What happens after upload?",
            "expected_anchor": "[ANCHOR-UPLOAD-PIPELINE]",
        },
    ]


def test_extract_anchors_from_text_returns_all_anchors():
    text = "Section text [ANCHOR-VECTOR-STORE] more text [ANCHOR-QDRANT-PLAN]"

    assert extract_anchors_from_text(text) == [
        "[ANCHOR-VECTOR-STORE]",
        "[ANCHOR-QDRANT-PLAN]",
    ]


def test_extract_anchors_from_text_returns_unknown_when_no_anchor_exists():
    assert extract_anchors_from_text("plain chunk text") == [UNKNOWN_ANCHOR]


def test_extract_anchor_groups_keeps_retrieval_order_and_chunk_groups():
    matches = [
        {
            "text": (
                "first [ANCHOR-UPLOAD-PIPELINE] "
                "same chunk [ANCHOR-VECTOR-STORE]"
            )
        },
        {"text": "second [ANCHOR-CHUNKING-POLICY]"},
        {"text": "third without anchor"},
    ]

    assert extract_anchor_groups(matches) == [
        ["[ANCHOR-UPLOAD-PIPELINE]", "[ANCHOR-VECTOR-STORE]"],
        ["[ANCHOR-CHUNKING-POLICY]"],
        [UNKNOWN_ANCHOR],
    ]


def test_judge_returns_pass_for_top_1_match():
    assert judge("[ANCHOR-A]", [["[ANCHOR-B]", "[ANCHOR-A]"]]) == "pass"


def test_judge_returns_partial_for_top_3_match_not_top_1():
    assert judge("[ANCHOR-A]", [["[ANCHOR-B]"], ["[ANCHOR-A]"]]) == "partial"


def test_judge_returns_fail_when_expected_anchor_missing():
    assert judge("[ANCHOR-A]", [["[ANCHOR-B]"], ["[ANCHOR-C]"]]) == "fail"


def test_render_results_markdown_includes_summary_and_rows():
    result = {
        "document_id": "doc_123",
        "sample_path": "eval/sample-personal-knowledge.md",
        "top_k": 3,
        "rows": [
            {
                "id": "Q1",
                "question": "What is the main purpose?",
                "expected_anchor": "[ANCHOR-PROJECT-PURPOSE]",
                "top_1_anchor": "[ANCHOR-PROJECT-PURPOSE]",
                "top_1_evidence": "uploads notes and generates grounded answers",
                "top_3_anchors": "[ANCHOR-PROJECT-PURPOSE], [ANCHOR-UPLOAD-PIPELINE]",
                "status": "pass",
                "notes": "",
            },
            {
                "id": "Q2",
                "question": "What happens after upload?",
                "expected_anchor": "[ANCHOR-UPLOAD-PIPELINE]",
                "top_1_anchor": "[ANCHOR-CHUNKING-POLICY]",
                "top_1_evidence": "describes chunking",
                "top_3_anchors": "[ANCHOR-CHUNKING-POLICY], [ANCHOR-UPLOAD-PIPELINE]",
                "status": "partial",
                "notes": "",
            },
        ],
    }

    markdown = render_results_markdown(result)

    assert "| Total questions | 2 |" in markdown
    assert "| Pass | 1 |" in markdown
    assert "| Partial | 1 |" in markdown
    assert "What is the main purpose?" in markdown
    assert "`[ANCHOR-PROJECT-PURPOSE]`" in markdown
    assert "### Pass Cases" in markdown
    assert "- Q1: top-1 hit [ANCHOR-PROJECT-PURPOSE]" in markdown
    assert "### Partial Cases" in markdown
    assert (
        "- Q2: expected anchor appears in top-3, but top-1 is [ANCHOR-CHUNKING-POLICY]"
        in markdown
    )
    assert "### What Rerank Should Improve" in markdown
    assert (
        "- Q2: move expected anchor [ANCHOR-UPLOAD-PIPELINE] above current top-1 [ANCHOR-CHUNKING-POLICY]"
        in markdown
    )


def test_render_results_markdown_keeps_top_3_anchors_inside_one_table_cell():
    result = {
        "document_id": "doc_123",
        "sample_path": "eval/sample-personal-knowledge.md",
        "top_k": 3,
        "rows": [
            {
                "id": "Q1",
                "question": "What is the main purpose?",
                "expected_anchor": "[ANCHOR-PROJECT-PURPOSE]",
                "top_1_anchor": "unknown / no anchor",
                "top_1_evidence": "general project text",
                "top_3_anchors": (
                    "unknown / no anchor ; "
                    "[ANCHOR-PROJECT-PURPOSE] ; "
                    "[ANCHOR-UPLOAD-PIPELINE]"
                ),
                "status": "partial",
                "notes": "",
            },
        ],
    }

    markdown = render_results_markdown(result)
    row = next(line for line in markdown.splitlines() if line.startswith("| Q1 |"))

    assert " ; " in row
    assert "unknown / no anchor ; [ANCHOR-PROJECT-PURPOSE]" in row
