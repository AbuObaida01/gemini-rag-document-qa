import json
from pathlib import Path

from app.services.query_service import QueryService


BASE_DIR = Path(__file__).resolve().parent
QUESTIONS_FILE = BASE_DIR / "evaluation_questions.json"


def load_questions() -> list[dict]:
    with QUESTIONS_FILE.open(
        "r",
        encoding="utf-8",
    ) as file:
        return json.load(file)


def evaluate_answers() -> None:
    questions = load_questions()

    query_service = QueryService()

    print("=" * 60)
    print("RAG ANSWER EVALUATION")
    print("=" * 60)

    for item in questions:
        question = item["question"]

        result = query_service.query(
            question=question
        )

        print()
        print("-" * 60)
        print(f"Question: {question}")
        print()
        print("Answer:")
        print(result["answer"])
        print()
        print(
            f"Sources: {len(result['sources'])}"
        )

        for source in result["sources"]:
            print(
                f"  - "
                f"{source['document']} | "
                f"page={source['page']} | "
                f"chunk={source['chunk']} | "
                f"distance={source['distance']:.4f}"
            )


if __name__ == "__main__":
    evaluate_answers()