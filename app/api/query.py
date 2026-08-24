from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.query_service import QueryService


router = APIRouter(
    prefix="/api",
    tags=["Query"],
)


query_service = QueryService()


class QueryRequest(BaseModel):
    question: str

class SourceResponse(BaseModel):
    document: str
    page: int
    chunk: int
    distance: float


class QueryResponse(BaseModel):
    answer: str
    sources: list[SourceResponse]

@router.post("/query")
async def query_documents(
    request: QueryRequest,
):
    try:
        return query_service.query(
            question=request.question
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except RuntimeError as exc:
        raise HTTPException(
            status_code=502,
            detail=str(exc),
        ) from exc