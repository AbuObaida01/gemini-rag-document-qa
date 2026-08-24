import chromadb

from app.config.settings import CHROMA_DB_PATH


COLLECTION_NAME = "document_chunks"


class VectorService:
    def __init__(self) -> None:
        self.client = chromadb.PersistentClient(
            path=CHROMA_DB_PATH
        )

        self.collection = self.client.get_or_create_collection(
            name=COLLECTION_NAME
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

            metadatas.append(
                {
                    "document": document_name,
                    "page": chunk["page"],
                    "chunk": chunk["chunk"],
                }
            )

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