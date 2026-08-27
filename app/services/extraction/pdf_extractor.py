from pathlib import Path
from typing import Any

import pymupdf

from app.services.extraction.base import BaseExtractor


class PDFExtractor(BaseExtractor):
    """
    Extract text from PDF files while preserving page information.
    """

    def extract(self, file_path: Path) -> dict[str, Any]:
        if not file_path.exists():
            raise FileNotFoundError(
                f"File not found: {file_path}"
            )

        if file_path.suffix.lower() != ".pdf":
            raise ValueError(
                "PDFExtractor can only process PDF files."
            )

        pages = []

        with pymupdf.open(file_path) as document:
            for page_number, page in enumerate(document, start=1):
                text = page.get_text("text").strip()

                if not text:
                    continue

                pages.append(
                    {
                        "text": text,
                        "metadata": {
                            "page": page_number,
                        },
                    }
                )

        if not pages:
            raise ValueError(
                "No extractable text was found in the PDF."
            )

        full_text = "\n\n".join(
            page["text"]
            for page in pages
        )

        return {
            "text": full_text,
            "pages": pages,
            "metadata": {
                "filename": file_path.name,
                "file_type": "pdf",
                "extraction_method": "text",
                "page_count": len(pages),
            },
        }