from pydantic import BaseModel


class Contact(BaseModel):
    id: int | None = None
    name: str
    phone: str
    email: str
