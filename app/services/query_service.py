import logging

from app.config.settings import TOP_K
from app.services.generation_service import GenerationService
from app.services.retrieval_service import RetrievalService


logger = logging.getLogger(__name__)


class QueryService:
    def __init__(self) -> None:
        self.retrieval_service = RetrievalService()
        self.generation_service = GenerationService()

    def query(
        self,
        question: str,
        top_k: int = TOP_K,
    ) -> dict:
        if not question.strip():
            raise ValueError(
                "Question cannot be empty."
            )

        logger.info(
            "Processing query: %s",
            question,
        )

        chunks = self.retrieval_service.retrieve(
            question=question,
            top_k=top_k,
        )

        logger.info(
            "Retrieved %s chunks for query",
            len(chunks),
        )

        context = self.retrieval_service.build_context(
            chunks
        )

        if not context:
            logger.info(
                "No relevant context found for query"
            )

            return {
                "answer": (
                    "I could not find the answer "
                    "in the provided documents."
                ),
                "sources": [],
            }

        logger.info(
            "Generating answer using %s chunks",
            len(chunks),
        )

        answer = self.generation_service.generate_answer(
            question=question,
            context=context,
        )

        logger.info(
            "Answer generated successfully"
        )

        sources = []

        for chunk in chunks:
            source = {
                "document": chunk["document"],
                "chunk": chunk["chunk"],
                "distance": chunk["distance"],
            }

            if "page" in chunk:
                source["page"] = chunk["page"]

            if "file_type" in chunk:
                source["file_type"] = chunk["file_type"]

            if "extraction_method" in chunk:
                source["extraction_method"] = (
                    chunk["extraction_method"]
                )

            sources.append(source)

        return {
            "answer": answer,
            "sources": sources,
        }