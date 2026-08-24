from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=1,
        description="Question to ask about the uploaded documents",
    )


class SourceResponse(BaseModel):
    document: str
    page: int
    chunk: int
    distance: float


class QueryResponse(BaseModel):
    answer: str
    sources: list[SourceResponse]