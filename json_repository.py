import json
from pathlib import Path
from fastapi import FastAPI, HTTPException
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
                return [
                    Contact(**contact) for contact in data
                ]
        return []

    async def save(self, contacts: list[Contact]) -> None:
        """Save contacts to JSON file."""
        with open(self.file_path, "w") as f:
            json.dump(
                [
                    contact.model_dump(exclude_none=True)
                    for contact in contacts
                ],
                f,
                indent=2,
            )

    async def get_by_id(self, contact_id: int) -> Contact | None:
        contacts = await self.get_all()
        return next(
            (contact for contact in contacts if contact.id == contact_id),
            None,
        )

    def register_routes(self, app: FastAPI) -> None:
        """Register CRUD routes on the FastAPI app."""
        repository = self

        @app.get("/")
        async def root() -> dict[str, str]:
            return {
                "message": "Contact Management API is running"
            }

        @app.get("/health")
        async def health_check() -> dict[str, str]:
            return {"status": "ok"}

        @app.get("/contacts", response_model=list[Contact])
        async def list_contacts() -> list[Contact]:
            """List all contacts."""
            return await repository.get_all()

        @app.get("/contacts/{contact_id}", response_model=Contact)
        async def read_contact(contact_id: int) -> Contact:
            contact = await repository.get_by_id(contact_id)
            if contact is None:
                raise HTTPException(status_code=404, detail="Contact not found")
            return contact

        @app.post(
            "/contacts",
            response_model=Contact,
            status_code=201,
        )
        async def create_contact(
            contact: Contact,
        ) -> Contact:
            """Add a new contact."""
            contacts = await repository.get_all()
            next_id = max(
                (
                    existing.id
                    for existing in contacts
                    if existing.id is not None
                ),
                default=0,
            ) + 1
            contact = contact.model_copy(update={"id": next_id})
            contacts.append(contact)
            await repository.save(contacts)
            return contact
