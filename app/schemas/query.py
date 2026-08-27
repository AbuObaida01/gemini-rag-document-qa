from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=1,
        description="Question to ask about the uploaded documents",
    )


class SourceResponse(BaseModel):
    document: str
    page: int | None = None
    chunk: int
    distance: float
    file_type: str | None = None
    extraction_method: str | None = None


class QueryResponse(BaseModel):
    answer: str
    sources: list[SourceResponse]