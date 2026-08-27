from pathlib import Path
from typing import Any

from app.services.extraction.base import BaseExtractor
from app.services.extraction.ocr_service import OCRService


class ImageExtractor(BaseExtractor):
    """
    Extract text from image files using OCR.
    """

    SUPPORTED_EXTENSIONS = {
        ".png",
        ".jpg",
        ".jpeg",
        ".webp",
        ".tif",
        ".tiff",
    }

    def __init__(
        self,
        ocr_service: OCRService | None = None,
    ) -> None:
        self.ocr_service = ocr_service or OCRService()

    def extract(self, file_path: Path) -> dict[str, Any]:
        if not file_path.exists():
            raise FileNotFoundError(
                f"File not found: {file_path}"
            )

        extension = file_path.suffix.lower()

        if extension not in self.SUPPORTED_EXTENSIONS:
            raise ValueError(
                f"ImageExtractor does not support {extension} files."
            )

        text = self.ocr_service.extract_text(
            file_path
        )

        return {
            "text": text,
            "metadata": {
                "filename": file_path.name,
                "file_type": extension.lstrip("."),
                "extraction_method": "ocr",
            },
        }