from pathlib import Path
from fastapi import UploadFile
from app.config.settings import UPLOAD_DIR

ALLOWED_CONTENT_TYPES={
    "application/pdf",
}

class DocumentService:
    def __init__(self)->None:
        self.upload_dir=Path(UPLOAD_DIR)
        self.upload_dir.mkdir(parents=True, exist_ok=True)

    def validate_file(self, file: UploadFile)->None:
        if not file.filename:
            raise ValueError("Filename is missing")
        if file.content_type not in ALLOWED_CONTENT_TYPES:
            raise ValueError("Only PDF files are supported")

    def check_duplicate(self, filename:str)->None:
        file_path=self.upload_dir / filename

        if file_path.exists():
            raise FileExistsError(
                f"Document {filename} already exists"
            )

    async def save_file(self, file:UploadFile)->Path:
        file_path=self.upload_dir / file.filename
        content=await file.read()

        if not content:
            raise ValueError("Uploaded file empty")

        file_path.write_bytes(content)
        return file_path

    async def process_upload(self, file:UploadFile)->Path:
        self.validate_file(file)
        filename=file.filename
        self.check_duplicate(filename)
        return await self.save_file(file)