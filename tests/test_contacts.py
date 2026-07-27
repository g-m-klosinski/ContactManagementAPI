from httpx2 import Response


def test_get_all(populated_client):
    response: Response = populated_client.get("/contacts")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)

    assert len(data) == 3
    assert len(data[0]) == 3


def test_get_contact(populated_client):
    response: Response = populated_client.get("/contacts/2")

    assert response.status_code == 200


def test_create_contact(client, sample_contact):
    response: Response = client.post("/contacts", json=sample_contact)
    assert response.status_code == 201
