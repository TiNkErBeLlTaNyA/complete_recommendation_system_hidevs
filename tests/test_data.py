from data.database import SessionLocal
from data.repositories import UserRepository, ContentRepository


def test_users_exist():
    db = SessionLocal()
    repo = UserRepository(db)
    users = repo.all()

    assert len(users) >= 10

    # Check structure of one user
    user = users[0]
    assert hasattr(user, "id")
    assert hasattr(user, "name")
    assert hasattr(user, "interests")


def test_content_exist():
    db = SessionLocal()
    repo = ContentRepository(db)
    content = repo.all()

    assert len(content) >= 20

    # Check structure of one content item
    item = content[0]
    assert hasattr(item, "id")
    assert hasattr(item, "title")
    assert hasattr(item, "category")