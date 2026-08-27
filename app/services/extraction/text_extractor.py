from pathlib import Path
from typing import Any

from app.services.extraction.base import BaseExtractor


class TextExtractor(BaseExtractor):
    """
    Extract text from plain-text and Markdown files.
    """

    SUPPORTED_EXTENSIONS = {
        ".txt",
        ".md",
    }

    def extract(self, file_path: Path) -> dict[str, Any]:
        if not file_path.exists():
            raise FileNotFoundError(
                f"File not found: {file_path}"
            )

        extension = file_path.suffix.lower()

        if extension not in self.SUPPORTED_EXTENSIONS:
            raise ValueError(
                f"TextExtractor does not support {extension} files."
            )

        text = file_path.read_text(
            encoding="utf-8"
        ).strip()

        if not text:
            raise ValueError(
                "The file contains no extractable text."
            )

        return {
            "text": text,
            "metadata": {
                "filename": file_path.name,
                "file_type": extension.lstrip("."),
            },
        }