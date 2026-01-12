import pytest

@pytest.mark.asyncio
async def test_member_cannot_borrow_more_than_5_books(client):
    member = await client.post(
        "/members/",
        json={
            "name": "Limit User",
            "email": "limit.user@example.com"
        }
    )
    member_id = member.json()["id"]

    for i in range(5):
        book = await client.post(
            "/books/",
            json={
                "title": f"Book {i}",
                "author": "Author",
                "isbn": f"ISBN{i}000"
            }
        )
        await client.post(
            "/loans/",
            json={
                "book_id": book.json()["id"],
                "member_id": member_id
            }
        )

    sixth_book = await client.post(
        "/books/",
        json={
            "title": "Book 6",
            "author": "Author",
            "isbn": "ISBN6000"
        }
    )

    response = await client.post(
        "/loans/",
        json={
            "book_id": sixth_book.json()["id"],
            "member_id": member_id
        }
    )

    assert response.status_code == 400