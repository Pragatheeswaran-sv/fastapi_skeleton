from fastapi import FastAPI

app = FastAPI(
    title="FastAPI JWT Auth",
    version="0.1.0",
)


@app.get("/health_check")
def health_check():
    return {"message": "FastAPI JWT Auth is running"}