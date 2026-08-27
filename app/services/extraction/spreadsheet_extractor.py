from pathlib import Path
from typing import Any

import pandas as pd

from app.services.extraction.base import BaseExtractor


class SpreadsheetExtractor(BaseExtractor):
    """
    Extract structured data from CSV and XLSX files.
    """

    SUPPORTED_EXTENSIONS = {
        ".csv",
        ".xlsx",
    }

    def extract(self, file_path: Path) -> dict[str, Any]:
        if not file_path.exists():
            raise FileNotFoundError(
                f"File not found: {file_path}"
            )

        extension = file_path.suffix.lower()

        if extension not in self.SUPPORTED_EXTENSIONS:
            raise ValueError(
                f"SpreadsheetExtractor does not support "
                f"{extension} files."
            )

        if extension == ".csv":
            return self._extract_csv(file_path)

        return self._extract_xlsx(file_path)

    def _extract_csv(
        self,
        file_path: Path,
    ) -> dict[str, Any]:
        dataframe = pd.read_csv(file_path)

        return self._build_result(
            dataframe=dataframe,
            file_path=file_path,
            sheet_name=None,
        )

    def _extract_xlsx(
        self,
        file_path: Path,
    ) -> dict[str, Any]:
        excel_file = pd.ExcelFile(file_path)

        sections = []
        all_text = []

        for sheet_name in excel_file.sheet_names:
            dataframe = pd.read_excel(
                file_path,
                sheet_name=sheet_name,
            )

            result = self._build_result(
                dataframe=dataframe,
                file_path=file_path,
                sheet_name=sheet_name,
            )

            if result["text"]:
                all_text.append(result["text"])

            sections.extend(result["sections"])

        if not sections:
            raise ValueError(
                "No extractable data was found in the XLSX file."
            )

        return {
            "text": "\n\n".join(all_text),
            "sections": sections,
            "metadata": {
                "filename": file_path.name,
                "file_type": "xlsx",
                "sheet_count": len(excel_file.sheet_names),
                "sheets": excel_file.sheet_names,
            },
        }

    def _build_result(
        self,
        dataframe: pd.DataFrame,
        file_path: Path,
        sheet_name: str | None,
    ) -> dict[str, Any]:
        if dataframe.empty:
            return {
                "text": "",
                "sections": [],
            }

        dataframe = dataframe.fillna("")

        headers = [
            str(column)
            for column in dataframe.columns
        ]

        lines = [
            " | ".join(headers)
        ]

        for _, row in dataframe.iterrows():
            values = [
                str(value)
                for value in row.tolist()
            ]

            lines.append(
                " | ".join(values)
            )

        text = "\n".join(lines).strip()

        metadata = {
            "type": "spreadsheet",
            "filename": file_path.name,
        }

        if sheet_name is not None:
            metadata["sheet"] = sheet_name

        return {
            "text": text,
            "sections": [
                {
                    "text": text,
                    "metadata": metadata,
                }
            ],
        }