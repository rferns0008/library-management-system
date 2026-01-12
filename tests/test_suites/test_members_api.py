import pytest

@pytest.mark.asyncio
async def test_create_member(client):
    payload = {
        "name": "John Doe",
        "email": "john.doe@example.com"
    }

    response = await client.post("/members/", json=payload)
    assert response.status_code == 200

    data = response.json()
    assert data["name"] == payload["name"]
    assert data["email"] == payload["email"]


@pytest.mark.asyncio
async def test_list_members(client):
    response = await client.get("/members/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_get_member_by_id(client):
    create = await client.post(
        "/members/",
        json={
            "name": "Jane Smith",
            "email": "jane.smith@example.com"
        }
    )
    member_id = create.json()["id"]

    response = await client.get(f"/members/{member_id}")
    assert response.status_code == 200
    assert response.json()["id"] == member_id