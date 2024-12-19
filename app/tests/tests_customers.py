from fastapi import status

def test_create_customer(client):
    response = client.post(
        "/customers",
        json = {
            "name":"John Doe",
            "email": "user@example.com",
            "age":33
        }
    )

    assert response.status_code == status.HTTP_201_CREATED