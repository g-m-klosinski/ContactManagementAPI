def test_create_contact(client, sample_contact):
    response = client.post("/contacts", json=sample_contact)
    assert response.status_code == 201