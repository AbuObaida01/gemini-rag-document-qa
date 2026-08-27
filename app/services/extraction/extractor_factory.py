from pathlib import Path

from app.services.extraction.base import BaseExtractor
from app.services.extraction.pdf_extractor import PDFExtractor
from app.services.extraction.text_extractor import TextExtractor
from app.services.extraction.docx_extractor import DOCXExtractor
from app.services.extraction.spreadsheet_extractor import SpreadsheetExtractor
from app.services.extraction.pptx_extractor import PPTXExtractor
from app.services.extraction.web_extractor import WebExtractor
from app.services.extraction.image_extractor import ImageExtractor


class ExtractorFactory:
    """
    Selects the appropriate document extractor
    based on the uploaded file extension.
    """

    def __init__(self) -> None:
        self._extractors: dict[str, BaseExtractor] = {
            ".pdf": PDFExtractor(),

            ".txt": TextExtractor(),
            ".md": TextExtractor(),

            ".docx": DOCXExtractor(),

            ".csv": SpreadsheetExtractor(),
            ".xlsx": SpreadsheetExtractor(),

            ".pptx": PPTXExtractor(),

            ".html": WebExtractor(),
            ".htm": WebExtractor(),
            ".json": WebExtractor(),

            ".png": ImageExtractor(),
            ".jpg": ImageExtractor(),
            ".jpeg": ImageExtractor(),
            ".webp": ImageExtractor(),
            ".tif": ImageExtractor(),
            ".tiff": ImageExtractor(),
        }

    def get_extractor(
        self,
        file_path: Path,
    ) -> BaseExtractor:
        extension = file_path.suffix.lower()

        extractor = self._extractors.get(extension)

        if extractor is None:
            raise ValueError(
                f"Unsupported file format: {extension}"
            )

        return extractor

    def extract(
        self,
        file_path: Path,
    ) -> dict:
        extractor = self.get_extractor(file_path)

        return extractor.extract(file_path)