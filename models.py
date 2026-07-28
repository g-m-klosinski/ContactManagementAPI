from pydantic import BaseModel


class Contact(BaseModel):
    name: str
    phone: str
    email: str
