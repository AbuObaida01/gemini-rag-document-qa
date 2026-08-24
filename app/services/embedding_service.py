from google import genai

from app.config.settings import GEMINI_API_KEY


EMBEDDING_MODEL = "gemini-embedding-001"


class EmbeddingService:
    def __init__(self) -> None:
        if not GEMINI_API_KEY:
            raise ValueError(
                "GEMINI_API_KEY is not configured."
            )

        self.client = genai.Client(
            api_key=GEMINI_API_KEY
        )

    def generate_embedding(self, text: str) -> list[float]:
        if not text.strip():
            raise ValueError(
                "Cannot generate an embedding for empty text."
            )

        response = self.client.models.embed_content(
            model=EMBEDDING_MODEL,
            contents=text,
        )

        return response.embeddings[0].values