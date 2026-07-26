import json
from pathlib import Path
from pydantic import BaseModel
from fastapi import FastAPI

app = FastAPI(
    title="Contact Management API",
    version="0.1.0",
    description="API for managing contacts.",
)

CONTACTS_FILE = Path(__file__).parent / "contacts.json"


class Contact(BaseModel):
    name: str
    phone: str
    email: str


def load_contacts() -> list[Contact]:
    """Load contacts from JSON file."""
    if CONTACTS_FILE.exists():
        with open(CONTACTS_FILE, "r") as f:
            data = json.load(f)
            return [Contact(**contact) for contact in data]
    return []


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "Contact Management API is running"}


@app.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/contacts", response_model=list[Contact])
async def list_contacts() -> list[Contact]:
    """List all contacts."""
    return load_contacts()