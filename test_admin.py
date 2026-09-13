import pytest

class DummyUserService:
    def __init__(self):
        self.users = [
            {"user_id": 1, "username": "alice", "is_locked": False},
            {"user_id": 2, "username": "bob", "is_locked": True}
        ]

    def get_all_users(self):
        return self.users

    def get_total_users(self):
        return len(self.users)

    def lock_user(self, user_id):
        for u in self.users:
            if u["user_id"] == int(user_id):
                u["is_locked"] = True
                return True
        return False

    def unlock_user(self, user_id):
        for u in self.users:
            if u["user_id"] == int(user_id):
                u["is_locked"] = False
                return True
        return False

    lock_account = lock_user
    unlock_account = unlock_user


def test_get_all_users():
    service = DummyUserService()
    users = service.get_all_users()
    assert len(users) == 2


def test_lock_account():
    service = DummyUserService()
    res = service.lock_account(1)
    assert res is True
    assert service.users[0]["is_locked"] is True


def test_unlock_account():
    service = DummyUserService()
    res = service.unlock_account(2)
    assert res is True
    assert service.users[1]["is_locked"] is False


def test_get_total_users():
    service = DummyUserService()
    assert service.get_total_users() == 2


def test_lock_account_not_found():
    service = DummyUserService()
    res = service.lock_account(999)
    assert res is False


def test_unlock_account_not_found():
    service = DummyUserService()
    res = service.unlock_account(999)
    assert res is False