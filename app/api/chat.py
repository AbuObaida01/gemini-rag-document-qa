from fastapi import APIRouter

router = APIRouter(
    prefix="/api/chat",
    tags=["Chat"],
)


@router.get("/test")
def chat_router_test():
    return {
        "message": "Chat router is working"
    }