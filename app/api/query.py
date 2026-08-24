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