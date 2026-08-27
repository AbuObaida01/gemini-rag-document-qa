from pydantic import BaseModel


class DocumentUploadResponse(BaseModel):
    message: str
    document: str
    file_type: str
    extraction_method: str
    chunks_created: int
    chunks_stored: int


class DocumentListResponse(BaseModel):
    documents: list[str]


class DocumentDeleteResponse(BaseModel):
    message: str
    document: str