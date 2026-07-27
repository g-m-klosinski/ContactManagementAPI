import json
import pathlib
import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI
from json_repository import JsonRepository


@pytest.fixture
def temp_contacts_file(
    tmp_path: pathlib.Path,
) -> pathlib.Path:
    """Create a temporary contacts file for testing."""
    contacts_file = tmp_path / "contacts.json"
    contacts_file.write_text("[]")
    return contacts_file


@pytest.fixture
def client(temp_contacts_file: pathlib.Path):
    """Provide a test client with isolated contacts file."""
    app = FastAPI(
        title="Contact Management API",
        version="0.1.0",
        description="API for managing contacts.",
    )

    repository = JsonRepository(temp_contacts_file)
    repository.register_routes(app)

    return TestClient(app)


@pytest.fixture
def sample_contact() -> dict[str, int | str]:
    """Provide a sample contact for testing."""
    return {
        "id": 1,
        "name": "Alice Brown",
        "phone": "555-0104",
        "email": "alice@example.com",
    }


@pytest.fixture
def sample_contacts() -> list[dict[str, int | str]]:
    """Provide multiple sample contacts for testing."""
    return [
        {
            "id": 1,
            "name": "John Doe",
            "phone": "555-0101",
            "email": "john@example.com",
        },
        {
            "id": 2,
            "name": "Jane Smith",
            "phone": "555-0102",
            "email": "jane@example.com",
        },
        {
            "id": 3,
            "name": "Bob Johnson",
            "phone": "555-0103",
            "email": "bob@example.com",
        },
    ]


@pytest.fixture
def populated_client(
    client: TestClient,
    temp_contacts_file: pathlib.Path,
    sample_contacts: list[dict[str, int | str]],
) -> TestClient:
    """Provide a test client with pre-populated contacts."""
    with open(temp_contacts_file, "w") as f:
        json.dump(sample_contacts, f, indent=2)
    return client
