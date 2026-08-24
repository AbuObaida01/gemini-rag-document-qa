from app.config.settings import (
    DISTANCE_THRESHOLD,
    TOP_K,
)
from app.services.embedding_service import EmbeddingService
from app.services.vector_service import VectorService


class RetrievalService:
    def __init__(self) -> None:
        self.embedding_service = EmbeddingService()
        self.vector_service = VectorService()

    def retrieve(
        self,
        question: str,
        top_k: int = TOP_K,
    ) -> list[dict]:
        if not question.strip():
            raise ValueError(
                "Question cannot be empty."
            )

        query_embedding = (
            self.embedding_service.generate_embedding(
                question
            )
        )

        results = self.vector_service.search(
            query_embedding=query_embedding,
            top_k=top_k,
        )

        retrieved_chunks = []

        for document, metadata, distance in zip(
            results["documents"][0],
            results["metadatas"][0],
            results["distances"][0],
        ):
            if distance > DISTANCE_THRESHOLD:
                continue

            retrieved_chunks.append(
                {
                    "text": document,
                    "document": metadata["document"],
                    "page": metadata["page"],
                    "chunk": metadata["chunk"],
                    "distance": distance,
                }
            )

        return retrieved_chunks

    def build_context(
        self,
        chunks: list[dict],
    ) -> str:
        if not chunks:
            return ""

        context_parts = []

        for index, chunk in enumerate(
            chunks,
            start=1,
        ):
            context_parts.append(
                f"""
    [Source {index}]
    Document: {chunk['document']}
    Page: {chunk['page']}
    Chunk: {chunk['chunk']}

    {chunk['text']}
    """.strip()
            )

        return "\n\n".join(context_parts)