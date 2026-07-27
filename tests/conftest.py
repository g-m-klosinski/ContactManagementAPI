import json
import pytest
from pathlib import Path
from fastapi.testclient import TestClient
from main import app, Contact, CONTACTS_FILE


@pytest.fixture
def temp_contacts_file(tmp_path):
    """Create a temporary contacts file for testing."""
    contacts_file = tmp_path / "contacts.json"
    contacts_file.write_text("[]")
    return contacts_file


@pytest.fixture
def client(temp_contacts_file, monkeypatch):
    """Provide a test client with isolated contacts file."""
    monkeypatch.setattr("main.CONTACTS_FILE", temp_contacts_file)
    return TestClient(app)


@pytest.fixture
def sample_contact():
    """Provide a sample contact for testing."""
    return {
        "name": "Alice Brown",
        "phone": "555-0104",
        "email": "alice@example.com"
    }


@pytest.fixture
def sample_contacts():
    """Provide multiple sample contacts for testing."""
    return [
        {
            "name": "John Doe",
            "phone": "555-0101",
            "email": "john@example.com"
        },
        {
            "name": "Jane Smith",
            "phone": "555-0102",
            "email": "jane@example.com"
        },
        {
            "name": "Bob Johnson",
            "phone": "555-0103",
            "email": "bob@example.com"
        }
    ]


@pytest.fixture
def populated_client(client, temp_contacts_file, sample_contacts, monkeypatch):
    """Provide a test client with pre-populated contacts."""
    with open(temp_contacts_file, "w") as f:
        json.dump(sample_contacts, f, indent=2)
    return client
