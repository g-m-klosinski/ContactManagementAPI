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


def save_contacts(contacts: list[Contact]) -> None:
    """Save contacts to JSON file."""
    with open(CONTACTS_FILE, "w") as f:
        json.dump([contact.model_dump() for contact in contacts], f, indent=2)


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


@app.post("/contacts", response_model=Contact, status_code=201)
async def create_contact(contact: Contact) -> Contact:
    """Add a new contact."""
    contacts = load_contacts()
    contacts.append(contact)
    save_contacts(contacts)
    return contact