from fastapi import FastAPI

from app.api.query import router as query_router
from app.api.upload import router as document_router
from app.core.logging_config import configure_logging


configure_logging()


app = FastAPI(
    title="Gemini RAG API",
    version="1.0.0",
)


app.include_router(document_router)
app.include_router(query_router)


@app.get(
    "/health",
    tags=["Health"],
)
async def health_check():
    return {
        "status": "ok"
    }