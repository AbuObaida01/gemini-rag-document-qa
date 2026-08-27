from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any


class BaseExtractor(ABC):
    """
    Base interface for all document extractors.

    Every extractor must:
    1. Accept a file path.
    2. Extract text from the file.
    3. Return extracted text and metadata.
    """

    @abstractmethod
    def extract(self, file_path: Path) -> dict[str, Any]:
        """
        Extract text and metadata from a file.

        Args:
            file_path: Path to the file being processed.

        Returns:
            Dictionary containing extracted text and metadata.
        """
        raise NotImplementedError