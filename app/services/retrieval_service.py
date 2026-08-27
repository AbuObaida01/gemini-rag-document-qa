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

            chunk = {
                "text": document,
                "document": metadata["document"],
                "chunk": metadata["chunk"],
                "distance": distance,
            }

            # Page exists for page-based documents
            # such as PDFs.
            if "page" in metadata:
                chunk["page"] = metadata["page"]

            # Preserve additional metadata such as
            # file type and OCR extraction method.
            if "file_type" in metadata:
                chunk["file_type"] = metadata[
                    "file_type"
                ]

            if "extraction_method" in metadata:
                chunk["extraction_method"] = metadata[
                    "extraction_method"
                ]

            retrieved_chunks.append(chunk)

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
            source_info = (
                f"[Source {index}]\n"
                f"Document: {chunk['document']}\n"
            )

            if "page" in chunk:
                source_info += (
                    f"Page: {chunk['page']}\n"
                )

            source_info += (
                f"Chunk: {chunk['chunk']}\n"
            )

            context_parts.append(
                (
                    source_info
                    + "\n"
                    + chunk["text"]
                ).strip()
            )

        return "\n\n".join(context_parts)