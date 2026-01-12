import pytest

@pytest.mark.asyncio
async def test_create_and_return_loan(client):
    book = await client.post(
        "/books/",
        json={
            "title": "Loan Book",
            "author": "Author",
            "isbn": "999888777"
        }
    )
    member = await client.post(
        "/members/",
        json={
            "name": "Loan User",
            "email": "loan.user@example.com"
        }
    )

    book_id = book.json()["id"]
    member_id = member.json()["id"]

    loan = await client.post(
        "/loans/",
        json={
            "book_id": book_id,
            "member_id": member_id
        }
    )

    assert loan.status_code == 200
    loan_id = loan.json()["id"]

    returned = await client.post(f"/loans/{loan_id}/return")
    assert returned.status_code == 200
    assert returned.json()["return_date"] is not None