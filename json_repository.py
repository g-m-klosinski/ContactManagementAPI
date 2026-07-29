import json
from pathlib import Path
from fastapi import FastAPI, HTTPException

import models


class JsonRepository:
    """JSON file-based contact storage."""

    def __init__(self, file_path: Path):
        self.file_path = file_path

    async def get_all(self) -> list[models.Contact]:
        """Load contacts from JSON file."""
        if self.file_path.exists():
            with open(self.file_path, "r") as f:
                data = json.load(f)
                return [
                    models.Contact(**contact) for contact in data
                ]
        return []

    async def save(self, contacts: list[models.Contact]) -> None:
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

    async def get_by_id(self, contact_id: int) -> models.Contact | None:
        contacts = await self.get_all()

        try:
            result: models.Contact | None = contacts[contact_id - 1]
        except IndexError:
            result = None

        return result

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

        @app.get("/contacts", response_model=list[models.Contact])
        async def list_contacts() -> list[models.Contact]:
            """List all contacts."""
            return await repository.get_all()

        @app.get("/contacts/{contact_id}", response_model=models.Contact)
        async def read_contact(contact_id: int) -> models.Contact:
            contact = await repository.get_by_id(contact_id)
            if contact is None:
                raise HTTPException(status_code=404, detail="Contact not found")
            return contact

        @app.post(
            "/contacts",
            response_model=models.Contact,
            status_code=201,
        )
        async def create_contact(
            contact: models.Contact,
        ) -> models.Contact:
            """Add a new contact."""
            contacts = await repository.get_all()
            contacts.append(contact)
            await repository.save(contacts)
            return contact

        @app.put(
                "/contacts/{contact_id}",
                status_code=204
        )
        async def update_contact(
                contact_id: int,
                contact: models.Contact
        ) -> None:
            contacts = await repository.get_all()
            contacts[contact_id - 1] = contact
            await repository.save(contacts)

        @app.delete("/contacts/{contact_id}", status_code=204)
        async def delete_contact(contact_id: int) -> None:
            contacts = await repository.get_all()
            
            try:
                del contacts[contact_id - 1]
            except IndexError:
                raise HTTPException(status_code=404, detail="Contact not found")

            await repository.save(contacts)
            