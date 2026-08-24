from fastapi import APIRouter, File, HTTPException, UploadFile

from app.schemas.document import (
    DocumentDeleteResponse,
    DocumentListResponse,
    DocumentUploadResponse,
)
from app.services.document_service import DocumentService


router = APIRouter(
    prefix="/api/documents",
    tags=["Documents"],
)


document_service = DocumentService()


@router.post(
    "/upload",
    response_model=DocumentUploadResponse,
)
async def upload_document(
    file: UploadFile = File(...),
):
    try:
        result = await document_service.process_upload(
            file
        )

        return {
            "message": "Document processed successfully",
            "document": file.filename,
            "pages_extracted": len(result["pages"]),
            "chunks_created": len(result["chunks"]),
            "chunks_stored": result["chunks_stored"],
        }

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except FileExistsError as exc:
        raise HTTPException(
            status_code=409,
            detail=str(exc),
        ) from exc

    except RuntimeError as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc


@router.get(
    "",
    response_model=DocumentListResponse,
)
async def list_documents():
    return {
        "documents": document_service.list_documents()
    }


@router.delete(
    "/{document_name}",
    response_model=DocumentDeleteResponse,
)
async def delete_document(
    document_name: str,
):
    try:
        document_service.delete_document(
            document_name
        )

        return {
            "message": "Document deleted successfully",
            "document": document_name,
        }

    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except RuntimeError as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc