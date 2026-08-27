import json
from pathlib import Path
from typing import Any

from bs4 import BeautifulSoup

from app.services.extraction.base import BaseExtractor


class WebExtractor(BaseExtractor):
    """
    Extract text from HTML and JSON files.
    """

    SUPPORTED_EXTENSIONS = {
        ".html",
        ".htm",
        ".json",
    }

    def extract(self, file_path: Path) -> dict[str, Any]:
        if not file_path.exists():
            raise FileNotFoundError(
                f"File not found: {file_path}"
            )

        extension = file_path.suffix.lower()

        if extension not in self.SUPPORTED_EXTENSIONS:
            raise ValueError(
                f"WebExtractor does not support {extension} files."
            )

        if extension in {".html", ".htm"}:
            return self._extract_html(file_path)

        return self._extract_json(file_path)

    def _extract_html(
        self,
        file_path: Path,
    ) -> dict[str, Any]:
        html = file_path.read_text(
            encoding="utf-8"
        )

        soup = BeautifulSoup(
            html,
            "html.parser",
        )

        # Remove content that isn't useful for
        # document question answering.
        for element in soup(
            ["script", "style", "noscript"]
        ):
            element.decompose()

        text = soup.get_text(
            separator="\n",
            strip=True,
        )

        if not text:
            raise ValueError(
                "No extractable text was found in the HTML file."
            )

        return {
            "text": text,
            "metadata": {
                "filename": file_path.name,
                "file_type": "html",
            },
        }

    def _extract_json(
        self,
        file_path: Path,
    ) -> dict[str, Any]:
        try:
            data = json.loads(
                file_path.read_text(
                    encoding="utf-8"
                )
            )
        except json.JSONDecodeError as exc:
            raise ValueError(
                "The JSON file contains invalid JSON."
            ) from exc

        text = json.dumps(
            data,
            indent=2,
            ensure_ascii=False,
        )

        if not text.strip():
            raise ValueError(
                "No extractable data was found in the JSON file."
            )

        return {
            "text": text,
            "metadata": {
                "filename": file_path.name,
                "file_type": "json",
            },
        }