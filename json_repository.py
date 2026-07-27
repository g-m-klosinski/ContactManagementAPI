import json
from pathlib import Path
from fastapi import FastAPI
from repositories import ContactRepository
from models import Contact


class JsonRepository(ContactRepository):
    """JSON file-based contact storage."""
    
    def __init__(self, file_path: Path):
        self.file_path = file_path
    
    async def get_all(self) -> list[Contact]:
        """Load contacts from JSON file."""
        if self.file_path.exists():
            with open(self.file_path, "r") as f:
                data = json.load(f)
                return [Contact(**contact) for contact in data]
        return []
    
    async def save(self, contacts: list[Contact]) -> None:
        """Save contacts to JSON file."""
        with open(self.file_path, "w") as f:
            json.dump([contact.model_dump() for contact in contacts], f, indent=2)
    
    def register_routes(self, app: FastAPI) -> None:
        """Register CRUD routes on the FastAPI app."""
        repository = self
        
        @app.get("/")
        async def root() -> dict[str, str]:
            return {"message": "Contact Management API is running"}
        
        @app.get("/health")
        async def health_check() -> dict[str, str]:
            return {"status": "ok"}
        
        @app.get("/contacts", response_model=list[Contact])
        async def list_contacts() -> list[Contact]:
            """List all contacts."""
            return await repository.get_all()
        
        @app.post("/contacts", response_model=Contact, status_code=201)
        async def create_contact(contact: Contact) -> Contact:
            """Add a new contact."""
            contacts = await repository.get_all()
            contacts.append(contact)
            await repository.save(contacts)
            return contact
