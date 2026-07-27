from pathlib import Path
from fastapi import FastAPI
from json_repository import JsonRepository

app = FastAPI(
    title="Contact Management API",
    version="0.1.0",
    description="API for managing contacts.",
)

contacts_file = Path(__file__).parent / "contacts.json"
repository = JsonRepository(contacts_file)

repository.register_routes(app)