from abc import ABC, abstractmethod
from fastapi import FastAPI
from models import Contact


class ContactRepository(ABC):
    """Abstract interface for contact persistence."""
    
    @abstractmethod
    async def get_all(self) -> list[Contact]:
        """Retrieve all contacts."""
        raise NotImplementedError
    
    @abstractmethod
    async def save(self, contacts: list[Contact]) -> None:
        """Save all contacts."""
        raise NotImplementedError
    
    @abstractmethod
    def register_routes(self, app: FastAPI) -> None:
        """Register CRUD routes on the FastAPI app."""
        raise NotImplementedError
