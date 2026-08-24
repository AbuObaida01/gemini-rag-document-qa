from fastapi import APIRouter, HTTPException

from app.schemas.query import QueryRequest, QueryResponse
from app.services.query_service import QueryService


router = APIRouter(
    prefix="/api",
    tags=["Query"],
)


query_service = QueryService()


@router.post(
    "/query",
    response_model=QueryResponse,
)
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