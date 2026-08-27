import chromadb

from app.config.settings import CHROMA_DB_PATH, TOP_K


COLLECTION_NAME = "document_chunks"


class VectorService:

    def __init__(self) -> None:
        self.client = chromadb.PersistentClient(
            path=CHROMA_DB_PATH
        )

        self.collection = (
            self.client.get_or_create_collection(
                name=COLLECTION_NAME
            )
        )

    def add_chunks(
        self,
        document_name: str,
        chunks: list[dict],
    ) -> int:
        if not chunks:
            return 0

        ids = []
        documents = []
        embeddings = []
        metadatas = []

        for chunk in chunks:
            chunk_id = (
                f"{document_name}"
                f"_chunk_{chunk['chunk']}"
            )

            ids.append(chunk_id)
            documents.append(chunk["text"])
            embeddings.append(chunk["embedding"])

            metadata = {
                "document": document_name,
                "chunk": chunk["chunk"],
            }

            # Preserve extractor metadata.
            chunk_metadata = chunk.get(
                "metadata",
                {},
            )

            if chunk_metadata:
                metadata.update(
                    chunk_metadata
                )

            # Preserve PDF page information
            # when it exists.
            if "page" in chunk:
                metadata["page"] = chunk["page"]

            metadatas.append(metadata)

        self.collection.add(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
        )

        return len(chunks)

    def delete_document(
        self,
        document_name: str,
    ) -> None:
        self.collection.delete(
            where={
                "document": document_name
            }
        )

    def count(self) -> int:
        return self.collection.count()

    def get_document_chunks(
        self,
        document_name: str,
    ) -> dict:
        return self.collection.get(
            where={
                "document": document_name
            },
            include=[
                "documents",
                "metadatas",
            ],
        )

    def list_documents(self) -> list[str]:
        result = self.collection.get(
            include=["metadatas"]
        )

        documents = set()

        for metadata in result["metadatas"]:
            if metadata and metadata.get("document"):
                documents.add(
                    metadata["document"]
                )

        return sorted(documents)

    def search(
        self,
        query_embedding: list[float],
        top_k: int = TOP_K,
    ) -> dict:
        if not query_embedding:
            raise ValueError(
                "Query embedding cannot be empty."
            )

        if top_k <= 0:
            raise ValueError(
                "top_k must be greater than zero."
            )

        return self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            include=[
                "documents",
                "metadatas",
                "distances",
            ],
        )