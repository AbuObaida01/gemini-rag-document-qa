from pathlib import Path

import pymupdf
from fastapi import UploadFile

from app.config.settings import UPLOAD_DIR


ALLOWED_CONTENT_TYPES = {
    "application/pdf",
}


class DocumentService:
    def __init__(self) -> None:
        self.upload_dir = Path(UPLOAD_DIR)
        self.upload_dir.mkdir(parents=True, exist_ok=True)

    def validate_file(self, file: UploadFile) -> None:
        if not file.filename:
            raise ValueError("Filename is missing.")

        if file.content_type not in ALLOWED_CONTENT_TYPES:
            raise ValueError("Only PDF files are supported.")

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

        pages = self.extract_text(file_path)

        return {
            "file_path": file_path,
            "pages": pages,
        }