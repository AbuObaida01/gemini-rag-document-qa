from fastapi import APIRouter, File, HTTPException, UploadFile

from app.services.document_service import DocumentService


router = APIRouter(
    prefix="/api/documents",
    tags=["Documents"],
)


document_service = DocumentService()


@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
):
    try:
        result = await document_service.process_upload(file)

        return {
            "message": "Document processed successfully",
            "document": file.filename,
            "pages_extracted": len(result["pages"]),
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