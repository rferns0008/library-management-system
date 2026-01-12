import pytest

@pytest.mark.asyncio
async def test_create_book(client):
    payload = {
        "title": "Nowhere To Run",
        "author": "C.J. Box",
        "isbn": "0399156453",
        "published_date": "2010-04-06"
    }

    response = await client.post("/books/", json=payload)
    assert response.status_code == 200

    data = response.json()
    assert data["title"] == payload["title"]
    assert data["author"] == payload["author"]
    assert data["isbn"] == payload["isbn"]


@pytest.mark.asyncio
async def test_list_books(client):
    response = await client.get("/books/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_get_book_by_id(client):
    create = await client.post(
        "/books/",
        json={
            "title": "Test Book",
            "author": "Author",
            "isbn": "111222333"
        }
    )
    book_id = create.json()["id"]

    response = await client.get(f"/books/{book_id}")
    assert response.status_code == 200
    assert response.json()["id"] == book_id