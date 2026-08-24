from fastapi import FastAPI
from app.api.chat import router as chat_router
from app.api.upload import router as upload_router
from app.api.query import router as query_router

app=FastAPI(
    title="RAG Document QA System"
)

app.include_router(upload_router)
app.include_router(chat_router)
app.include_router(query_router)

@app.get("/")
def root():
    return{
        "message":"Hello"
    }