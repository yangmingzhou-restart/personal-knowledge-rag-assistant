import re
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from fastapi.testclient import TestClient

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.main import app


ANCHOR_PATTERN = re.compile(r"\[ANCHOR-[A-Z0-9-]+\]")
UNKNOWN_ANCHOR = "unknown / no anchor"


def parse_evaluation_questions(path: Path) -> list[dict[str, str]]:
    """
    path: Path, evaluation-questions.md path.

    return: list[dict[str, str]], parsed question rows with id, question, and expected_anchor.
            [
                {
                    "id": "Q1",
                    "question": "What is the main purpose of the Personal Knowledge RAG Assistant?",
                    "expected_anchor": "[ANCHOR-PROJECT-PURPOSE]",
                },
                ...
            ]

    RAG process position:
        Turns the human-readable evaluation plan into structured input for the
        automated retrieval evaluation runner.
    """
    questions: list[dict[str, str]] = []
    current: dict[str, str] | None = None

    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()

        if stripped.startswith("### Q"):
            if current is not None:
                questions.append(current)

            question_id = stripped.split(" - ", maxsplit=1)[0].replace("### ", "") # Q1,Q2...
            current = {"id": question_id}
            continue

        if current is None:
            continue

        if stripped.startswith("- Question:"):
            current["question"] = stripped.removeprefix("- Question:").strip()
        elif stripped.startswith("- Expected anchor:"):
            current["expected_anchor"] = (
                stripped.removeprefix("- Expected anchor:")
                .strip()
                .strip("`")
            )

    if current is not None:
        questions.append(current)

    return [
        item
        for item in questions
        if item.get("id") and item.get("question") and item.get("expected_anchor")
    ]


def extract_anchors_from_text(text: str) -> list[str]:
    """
    text: str, returned chunk text.

    return: list[str], all anchor labels in the chunk.
            If the chunk has no anchor, return [UNKNOWN_ANCHOR].
    """
    matches = ANCHOR_PATTERN.findall(text)
    return matches if matches else [UNKNOWN_ANCHOR]


def extract_anchor_groups(matches: list[dict[str, Any]]) -> list[list[str]]:
    """
    matches: list[dict[str, Any]], /retrieve matches.

    return: list[list[str]], anchors grouped by returned chunk in ranking order.
    """
    return [
        extract_anchors_from_text(str(match.get("text", "")))
        for match in matches
    ]


def summarize_evidence(match: dict[str, Any], max_length: int = 140) -> str:
    """
    match: dict[str, Any], one retrieved chunk row.

    return: str, short evidence phrase for evaluation-results.md.
    """
    text = " ".join(str(match.get("text", "")).split())
    return text[:max_length]


def judge(expected_anchor: str, anchor_groups: list[list[str]]) -> str:
    """
    expected_anchor: str, target anchor from evaluation-questions.md.
    anchor_groups: list[list[str]], anchors returned by /retrieve in ranking order.

    return: str, pass / partial / fail.
    """
    if not anchor_groups:
        return "fail"
    
    # pass: the first returned chunk contains the expected anchor
    if expected_anchor in anchor_groups[0]:
        return "pass"
    
    # partial: the expected anchor appears in any of the returned chunks
    if any(expected_anchor in anchors for anchors in anchor_groups[1:]):
        return "partial"
    
    return "fail"


def run_retrieval_evaluation(
    client: TestClient,
    sample_path: Path,
    questions_path: Path,
    top_k: int = 3,
) -> dict[str, Any]:
    """
    client: TestClient, FastAPI test client used to call upload and retrieve.
    sample_path: Path, markdown sample document to upload.
    questions_path: Path, structured markdown question file.
    top_k: int, number of matches requested from /retrieve.

    return: dict[str, Any], evaluation result payload ready for Markdown rendering.
            {
                "document_id": "1234567890",
                "sample_path": "sample.md",
                "top_k": 3,
                "rows": [
                    {
                        "id": "Q1",
                        "question": "What is the main purpose of the Personal Knowledge RAG Assistant?",
                        "expected_anchor": "[ANCHOR-PROJECT-PURPOSE]",
                        "top_1_anchor": "[ANCHOR-PROJECT-PURPOSE]",
                        "top_1_evidence": "upload personal notes",
                        "top_3_anchors": "[ANCHOR-PROJECT-PURPOSE], [ANCHOR-PROJECT-UPLOAD], [ANCHOR-PROJECT-SPLIT]",
                        "status": "pass",
                        "notes": "",
                    },
                    ...
                ],
            }
    """
    questions = parse_evaluation_questions(questions_path)

    upload_response = client.post(
        "/upload",
        files={
            "file": (
                sample_path.name,
                sample_path.read_bytes(),
                "text/markdown",
            )
        },
    )
    upload_response.raise_for_status()
    document_id = upload_response.json()["document_id"]

    rows = []
    for item in questions:
        response = client.post(
            "/retrieve",
            json={
                "document_id": document_id,
                "question": item["question"],
                "top_k": top_k,
            },
        )
        response.raise_for_status()

        matches = response.json()["matches"]
        anchor_groups = extract_anchor_groups(matches)
        top_1 = matches[0] if matches else {}
        status = judge(item["expected_anchor"], anchor_groups)

        rows.append(
            {
                "id": item["id"],
                "question": item["question"],
                "expected_anchor": item["expected_anchor"],
                "top_1_anchor": (
                    ", ".join(anchor_groups[0])
                    if anchor_groups
                    else UNKNOWN_ANCHOR
                ),
                "top_1_evidence": summarize_evidence(top_1),
                "top_3_anchors": " ; ".join(
                    ", ".join(group) for group in anchor_groups
                ),
                "status": status,
                "notes": "",
            }
        )

    return {
        "document_id": document_id,
        "sample_path": str(sample_path),
        "top_k": top_k,
        "rows": rows,
    }


def render_results_markdown(result: dict[str, Any]) -> str:
    """
    result: dict[str, Any], output from run_retrieval_evaluation().

    return: str, markdown content for eval/evaluation-results.md.
    """
    rows = result["rows"]
    pass_count = sum(1 for row in rows if row["status"] == "pass")
    partial_count = sum(1 for row in rows if row["status"] == "partial")
    fail_count = sum(1 for row in rows if row["status"] == "fail")

    lines = [
        "# Retrieval Evaluation Results",
        "",
        f"Date: {datetime.now(UTC).isoformat()}",
        f"Sample document: `{result['sample_path']}`",
        f"Document ID: {result['document_id']}",
        "Chunk size: 500",
        "Overlap: 50",
        f"Top k: {result['top_k']}",
        "",
        "## Summary",
        "",
        "| Metric | Result |",
        "| --- | --- |",
        f"| Total questions | {len(rows)} |",
        f"| Pass | {pass_count} |",
        f"| Partial | {partial_count} |",
        f"| Fail | {fail_count} |",
        "",
        "## Detailed Results",
        "",
        "| ID | Question | Expected anchor | Top-1 anchor | Top-1 evidence | Top-3 anchors | Status | Notes |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]

    for row in rows:
        lines.append(
            "| {id} | {question} | `{expected_anchor}` | `{top_1_anchor}` | {top_1_evidence} | {top_3_anchors} | {status} | {notes} |".format(
                **row
            )
        )

    lines.extend(render_final_analysis(rows))
    return "\n".join(lines) + "\n"


def describe_row(row: dict[str, Any]) -> str:
    """
    row: dict[str, Any], one evaluated question row.

    return: str, concise markdown bullet for the final analysis section.
    """
    if row["status"] == "pass":
        reason = f"top-1 hit {row['expected_anchor']}"
    elif row["status"] == "partial":
        reason = (
            f"expected anchor appears in top-3, but top-1 is {row['top_1_anchor']}"
        )
    else:
        reason = (
            f"expected {row['expected_anchor']} missing from top-3: "
            f"{row['top_3_anchors']}"
        )

    return f"- {row['id']}: {reason}"


def render_case_lines(rows: list[dict[str, Any]], status: str) -> list[str]:
    """
    rows: list[dict[str, Any]], all evaluated question rows.
    status: str, pass / partial / fail.

    return: list[str], markdown bullets for that status.
    """
    selected = [row for row in rows if row["status"] == status]
    if not selected:
        return ["- None"]
    return [describe_row(row) for row in selected]


def render_final_analysis(rows: list[dict[str, Any]]) -> list[str]:
    """
    rows: list[dict[str, Any]], all evaluated question rows.

    return: list[str], generated final analysis markdown lines.
    """
    partial_rows = [row for row in rows if row["status"] == "partial"]
    fail_rows = [row for row in rows if row["status"] == "fail"]

    lines = [
        "",
        "## Final Analysis",
        "",
        "### Pass Cases",
        "",
        *render_case_lines(rows, "pass"),
        "",
        "### Partial Cases",
        "",
        *render_case_lines(rows, "partial"),
        "",
        "### Fail Cases",
        "",
        *render_case_lines(rows, "fail"),
        "",
        "### What Rerank Should Improve",
        "",
    ]

    if partial_rows:
        lines.extend(
            [
                f"- {row['id']}: move expected anchor {row['expected_anchor']} above current top-1 {row['top_1_anchor']}"
                for row in partial_rows
            ]
        )
    else:
        lines.append("- None")

    lines.extend(["", "### What Retrieval Or Content Should Improve", ""])

    if fail_rows:
        lines.extend(
            [
                f"- {row['id']}: expected anchor {row['expected_anchor']} did not appear in top-3"
                for row in fail_rows
            ]
        )
    else:
        lines.append("- None")

    lines.extend(
        [
            "",
            "### Next Experiment",
            "",
            "- Use this baseline to compare the rerank results. Focus first on partial cases, because the correct evidence is already retrieved but ranked too low.",
        ]
    )
    return lines


def main() -> None:
    client = TestClient(app)
    sample_path = PROJECT_ROOT / "eval" / "sample-personal-knowledge.md"
    questions_path = PROJECT_ROOT / "eval" / "evaluation-questions.md"
    results_path = PROJECT_ROOT / "eval" / "evaluation-results.md"

    result = run_retrieval_evaluation(
        client=client,
        sample_path=sample_path,
        questions_path=questions_path,
        top_k=3,
    )
    results_path.write_text(
        render_results_markdown(result),
        encoding="utf-8",
    )
    pass_count = sum(1 for row in result["rows"] if row["status"] == "pass")
    partial_count = sum(1 for row in result["rows"] if row["status"] == "partial")
    fail_count = sum(1 for row in result["rows"] if row["status"] == "fail")
    print(f"Wrote: {results_path}")
    print(
        f"Summary: total={len(result['rows'])}, "
        f"pass={pass_count}, partial={partial_count}, fail={fail_count}"
    )


if __name__ == "__main__":
    main()
