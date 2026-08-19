from app.config.settings import(
    CHROMA_DB_PATH,
    CHUNK_OVERLAP,
    CHUNK_SIZE,
    TOP_K,
    UPLOAD_DIR,
)

def test_settings_loaded():
    assert CHROMA_DB_PATH=="./chroma_db"
    assert UPLOAD_DIR=="./uploads"
    assert CHUNK_SIZE==800
    assert CHUNK_OVERLAP==150
    assert TOP_K==3