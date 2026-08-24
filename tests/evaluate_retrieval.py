import json
from pathlib import Path

from app.services.retrieval_service import RetrievalService


BASE_DIR = Path(__file__).resolve().parent
QUESTIONS_FILE = BASE_DIR / "evaluation_questions.json"


def load_questions() -> list[dict]:
    with QUESTIONS_FILE.open(
        "r",
        encoding="utf-8",
    ) as file:
        return json.load(file)


def evaluate_retrieval() -> None:
    questions = load_questions()

    retrieval_service = RetrievalService()

    total = len(questions)

    relevant_questions = [
        item
        for item in questions
        if item["relevant"]
    ]

    irrelevant_questions = [
        item
        for item in questions
        if not item["relevant"]
    ]

    relevant_success = 0
    irrelevant_success = 0

    print("=" * 60)
    print("RAG RETRIEVAL EVALUATION")
    print("=" * 60)

    for item in questions:
        question = item["question"]
        expected_relevant = item["relevant"]

        results = retrieval_service.retrieve(
            question=question
        )

        distances = [
            result["distance"]
            for result in results
        ]

        retrieved = len(results) > 0

        if expected_relevant and retrieved:
            relevant_success += 1

        if not expected_relevant and not retrieved:
            irrelevant_success += 1

        print()
        print("-" * 60)
        print(f"Question: {question}")
        print(
            f"Expected relevant: "
            f"{expected_relevant}"
        )
        print(
            f"Retrieved chunks: "
            f"{len(results)}"
        )
        print(
            f"Distances: "
            f"{[round(d, 4) for d in distances]}"
        )

        for index, result in enumerate(
            results,
            start=1,
        ):
            print()
            print(
                f"Source {index}: "
                f"{result['document']} | "
                f"page={result['page']} | "
                f"chunk={result['chunk']}"
            )

            print(
                f"Distance: "
                f"{result['distance']:.4f}"
            )

            print("Text:")
            print(result["text"][:1000])

    relevant_recall = (
        relevant_success / len(relevant_questions)
        if relevant_questions
        else 0
    )

    irrelevant_rejection = (
        irrelevant_success / len(irrelevant_questions)
        if irrelevant_questions
        else 0
    )

    print()
    print("=" * 60)
    print("RESULTS")
    print("=" * 60)

    print(
        f"Total questions: "
        f"{total}"
    )

    print(
        f"Relevant questions: "
        f"{len(relevant_questions)}"
    )

    print(
        f"Relevant questions retrieved: "
        f"{relevant_success}"
    )

    print(
        f"Retrieval recall: "
        f"{relevant_recall:.2%}"
    )

    print(
        f"Irrelevant questions: "
        f"{len(irrelevant_questions)}"
    )

    print(
        f"Irrelevant questions rejected: "
        f"{irrelevant_success}"
    )

    print(
        f"Irrelevant rejection rate: "
        f"{irrelevant_rejection:.2%}"
    )


if __name__ == "__main__":
    evaluate_retrieval()