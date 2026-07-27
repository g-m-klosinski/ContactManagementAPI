from enum import Enum
from pydantic import BaseModel


class DatabaseType(Enum):
    """Supported database backends."""
    JSON = "json"
    SQLITE = "sqlite"
    MONGODB = "mongodb"


class Contact(BaseModel):
    name: str
    phone: str
    email: str
