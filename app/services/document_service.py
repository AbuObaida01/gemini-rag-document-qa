from pathlib import Path

import pymupdf
from fastapi import UploadFile

from app.config.settings import UPLOAD_DIR
from app.services.chunk_service import ChunkService
from app.services.embedding_service import EmbeddingService
from app.services.vector_service import VectorService

ALLOWED_CONTENT_TYPES = {
    "application/pdf",
}


class DocumentService:
    def __init__(self) -> None:
        self.upload_dir = Path(UPLOAD_DIR)
        self.upload_dir.mkdir(parents=True, exist_ok=True)
        self.chunk_service = ChunkService()
        self.embedding_service = EmbeddingService()
        self.vector_service = VectorService()

    def validate_file(self, file: UploadFile) -> None:
        if not file.filename:
            raise ValueError(
                "Filename is missing."
            )

        if not file.filename.lower().endswith(".pdf"):
            raise ValueError(
                "Only PDF files are supported."
            )

        if file.content_type != "application/pdf":
            raise ValueError(
                "Only PDF files are supported."
            )

    def check_duplicate(self, filename: str) -> None:
        file_path = self.upload_dir / filename

        if file_path.exists():
            raise FileExistsError(
                f"Document '{filename}' already exists."
            )

    async def save_file(self, file: UploadFile) -> Path:
        file_path = self.upload_dir / file.filename

        content = await file.read()

        if not content:
            raise ValueError("Uploaded file is empty.")

        file_path.write_bytes(content)

        return file_path

    def extract_text(self, file_path: Path) -> list[dict]:
        pages = []

        try:
            document = pymupdf.open(file_path)
        except Exception as exc:
            raise ValueError(
                "The uploaded file is not a valid PDF."
            ) from exc

        try:
            if len(document) == 0:
                raise ValueError(
                    "The uploaded PDF contains no pages."
                )

            for page_number, page in enumerate(document, start=1):
                text = page.get_text("text").strip()

                if text:
                    pages.append(
                        {
                            "page": page_number,
                            "text": text,
                        }
                    )

        finally:
            document.close()

        if not pages:
            raise ValueError(
                "The uploaded PDF contains no extractable text."
            )

        return pages

    async def process_upload(self, file: UploadFile) -> dict:
        self.validate_file(file)

        filename = file.filename

        self.check_duplicate(filename)

        file_path = await self.save_file(file)

        try:
            pages = self.extract_text(file_path)

            chunks = self.chunk_service.chunk_pages(pages)

            for chunk in chunks:
                chunk["embedding"] = (
                    self.embedding_service.generate_embedding(
                        chunk["text"]
                    )
                )

            chunks_stored = self.vector_service.add_chunks(
                document_name=filename,
                chunks=chunks,
            )

        except Exception:
            file_path.unlink(missing_ok=True)
            raise

        return {
            "file_path": file_path,
            "pages": pages,
            "chunks": chunks,
            "chunks_stored": chunks_stored,
        }

    def list_documents(self) -> list[str]:
        documents = []

        for file_path in self.upload_dir.glob("*.pdf"):
            documents.append(file_path.name)

        return sorted(documents)

    def delete_document(
        self,
        document_name: str,
    ) -> None:
        file_path = self._get_safe_path(
            document_name
        )

        if not file_path.exists():
            raise FileNotFoundError(
                f"Document '{document_name}' not found."
            )

        self.vector_service.delete_document(
            document_name
        )

        try:
            file_path.unlink()
        except Exception as exc:
            raise RuntimeError(
                "Document vectors were deleted, "
                "but the PDF file could not be removed."
            ) from exc

    def _get_safe_path(
        self,
        filename: str,
    ) -> Path:
        upload_dir = self.upload_dir.resolve()
        file_path = (upload_dir / filename).resolve()

        if upload_dir not in file_path.parents:
            raise ValueError(
                "Invalid document path."
            )

        return file_path