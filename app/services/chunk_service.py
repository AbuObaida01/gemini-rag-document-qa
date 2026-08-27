from app.config.settings import CHUNK_OVERLAP, CHUNK_SIZE


class ChunkService:

    def __init__(
        self,
        chunk_size: int = CHUNK_SIZE,
        chunk_overlap: int = CHUNK_OVERLAP,
    ) -> None:
        if chunk_size <= 0:
            raise ValueError(
                "Chunk size must be greater than zero."
            )

        if chunk_overlap < 0:
            raise ValueError(
                "Chunk overlap cannot be negative."
            )

        if chunk_overlap >= chunk_size:
            raise ValueError(
                "Chunk overlap must be smaller than chunk size."
            )

        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def chunk_text(
        self,
        text: str,
        metadata: dict | None = None,
    ) -> list[dict]:
        """
        Split generic extracted text into overlapping chunks.

        Used for non-page-based documents such as:
        - TXT
        - Markdown
        - DOCX
        - CSV
        - XLSX
        - PPTX
        - HTML
        - JSON
        - Images processed through OCR
        """

        text = text.strip()

        if not text:
            return []

        metadata = metadata or {}

        chunks = []

        start = 0
        chunk_number = 1

        while start < len(text):
            end = min(
                start + self.chunk_size,
                len(text),
            )

            chunk_text = text[start:end].strip()

            if chunk_text:
                chunk = {
                    "chunk": chunk_number,
                    "text": chunk_text,
                    "metadata": metadata.copy(),
                }

                chunks.append(chunk)

                chunk_number += 1

            if end == len(text):
                break

            start = end - self.chunk_overlap

        return chunks

    def chunk_page(
        self,
        text: str,
        page_number: int,
    ) -> list[dict]:
        """
        Split text from a single PDF page.

        Kept for backward compatibility with
        the existing PDF pipeline.
        """

        chunks = self.chunk_text(
            text=text,
            metadata={
                "page": page_number,
            },
        )

        for chunk in chunks:
            chunk["page"] = page_number

        return chunks

    def chunk_pages(
        self,
        pages: list[dict],
    ) -> list[dict]:
        """
        Chunk multiple PDF pages while preserving
        page numbers and global chunk numbering.
        """

        all_chunks = []
        global_chunk_number = 1

        for page in pages:
            page_chunks = self.chunk_page(
                text=page["text"],
                page_number=page["page"],
            )

            for chunk in page_chunks:
                chunk["chunk"] = global_chunk_number

                all_chunks.append(chunk)

                global_chunk_number += 1

        return all_chunks