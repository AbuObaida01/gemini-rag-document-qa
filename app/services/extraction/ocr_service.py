from pathlib import Path
import os

import pytesseract
from PIL import Image


class OCRService:
    """
    Extract text from images using Tesseract OCR.
    """

    def __init__(
        self,
        tesseract_cmd: str | None = None,
    ) -> None:

        if tesseract_cmd:
            pytesseract.pytesseract.tesseract_cmd = (
                tesseract_cmd
            )
            return

        # Windows default installation path.
        windows_path = Path(
            r"C:\Program Files\Tesseract-OCR\tesseract.exe"
        )

        if windows_path.exists():
            pytesseract.pytesseract.tesseract_cmd = (
                str(windows_path)
            )

    def extract_text(
        self,
        file_path: Path,
    ) -> str:

        if not file_path.exists():
            raise FileNotFoundError(
                f"File not found: {file_path}"
            )

        try:
            with Image.open(file_path) as image:
                text = pytesseract.image_to_string(
                    image
                )

        except Exception as exc:
            raise RuntimeError(
                f"Failed to process image with OCR: "
                f"{file_path.name}"
            ) from exc

        text = text.strip()

        if not text:
            raise ValueError(
                "OCR could not extract any text from "
                "the image."
            )

        return text