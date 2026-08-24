from google import genai

from app.config.settings import GEMINI_API_KEY


GENERATION_MODEL = "gemini-3.6-flash"


class GenerationService:
    def __init__(self) -> None:
        if not GEMINI_API_KEY:
            raise ValueError(
                "GEMINI_API_KEY is not configured."
            )

        self.client = genai.Client(
            api_key=GEMINI_API_KEY
        )

    def generate_answer(
        self,
        question: str,
        context: str,
    ) -> str:
        if not question.strip():
            raise ValueError(
                "Question cannot be empty."
            )

        if not context.strip():
            raise ValueError(
                "Context cannot be empty."
            )

        prompt = f"""
You are a document question-answering assistant.

Answer the user's question using ONLY the information
provided in the context below.

If the answer cannot be found in the context, say:
"I could not find the answer in the provided documents."

Rules:
- Do not use outside knowledge.
- Do not invent facts.
- Do not make unsupported claims.
- Keep the answer clear and concise.

Context:
{context}

Question:
{question}
"""

        try:
            response = self.client.models.generate_content(
                model=GENERATION_MODEL,
                contents=prompt,
            )

        except Exception as exc:
            raise RuntimeError(
                "Failed to generate an answer with Gemini."
            ) from exc

        if not response.text:
            raise RuntimeError(
                "Gemini returned an empty response."
            )

        return response.text.strip()