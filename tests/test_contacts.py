import httpx2
import fastapi.testclient

import models


def test_get_all(populated_client: fastapi.testclient.TestClient):
    response: httpx2.Response = populated_client.get("/contacts")

    assert response.status_code == 200

    data: list[dict[str, int | str]] = response.json()

    assert isinstance(data, list)

    assert len(data) == 3
    assert len(data[0]) == 3


def test_get_contact(populated_client: fastapi.testclient.TestClient):
    response: httpx2.Response = populated_client.get("/contacts/2")

    assert response.status_code == 200


def test_create_contact(client: fastapi.testclient.TestClient, sample_contact: models.Contact):
    response: httpx2.Response = client.post("/contacts", json=sample_contact)
    assert response.status_code == 201


def test_update_contact(populated_client: fastapi.testclient.TestClient, sample_contact: models.Contact):
    response: httpx2.Response = populated_client.put("/contacts/1", json=sample_contact)

    assert response.status_code == 204