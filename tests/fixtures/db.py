import pytest
from app.models import Book, Member, Loan
from datetime import date


@pytest.fixture
def sample_book():
    return Book(
        title="Sample Book",
        author="Sample Author",
        isbn="999999",
        published_date=None
    )


@pytest.fixture
def sample_member():
    return Member(
        name="Test User",
        email="test@example.com",
        membership_date=date.today()
    )