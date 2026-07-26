from fastapi import FastAPI

app = FastAPI(
    title="Contact Management API",
    version="0.1.0",
    description="API for managing contacts.",
)


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "Contact Management API is running"}


@app.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "ok"}