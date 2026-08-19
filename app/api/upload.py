from fastapi import APIRouter

router=APIRouter(
    prefix="/api/documents",
    tags=["Documnets"],
)

@router.get("/test")
def upload_router_test():
    return{
        "message":"Router is working"
    }