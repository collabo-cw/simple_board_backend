import pytest
from user.models import User, UserManager


@pytest.mark.django_db
def test_create_user():
    user_data = {
        "email": "test@example.com",
        "password": "testpassword",
        "name": "Test User",
        "birthday": "19900101",
        "gender": "M"
    }
    User.objects.all().delete()
    user = User.objects.create_user(**user_data)

    assert user.email == user_data["email"]
    assert user.check_password(user_data["password"])  # 비밀번호는 해시화되어 저장되므로 check_password 사용
    assert user.name == user_data["name"]
    assert user.birthday == user_data["birthday"]
    assert user.gender == user_data["gender"]
    assert user.is_active is True
    assert user.is_staff is False


@pytest.mark.django_db
def test_create_superuser():
    user_data = {
        "email": "admin@example.com",
        "password": "adminpassword",
        "name": "Admin User",
        "birthday": "19800101",
        "gender": "F"
    }
    User.objects.all().delete()
    user = User.objects.create_superuser(**user_data)

    assert user.email == user_data["email"]
    assert user.check_password(user_data["password"])
    assert user.name == user_data["name"]
    assert user.birthday == user_data["birthday"]
    assert user.gender == user_data["gender"]
    assert user.is_active is True
    assert user.is_staff is True
    assert user.is_superuser is True


@pytest.mark.django_db
def test_user_string_representation():
    user_data = {
        "email": "test@example.com",
        "password": "testpassword",
        "name": "Test User",
        "birthday": "19900101",
        "gender": "M"
    }
    User.objects.all().delete()
    user = User.objects.create_user(**user_data)

    assert str(user) == f"등록된 이메일 ={user.email}, 등록된 이름 ={user.name}, 등록된 역할={user.role}"


@pytest.mark.django_db
def test_user_unique_email():
    user_data = {
        "email": "test@example.com",
        "password": "testpassword",
        "name": "Test User",
        "birthday": "19900101",
        "gender": "M"
    }

    User.objects.all().delete()
    User.objects.create_user(**user_data)

    with pytest.raises(Exception):
        User.objects.create_user(**user_data)


@pytest.mark.django_db
def test_user_required_fields():
    user_data = {
        "email": "test@example.com",
        "password": "testpassword"
    }
    User.objects.all().delete()
    user = User.objects.create_user(**user_data)

    assert user.email == user_data["email"]
    assert user.check_password(user_data["password"])
    assert user.is_active is True
    assert user.is_staff is False

@pytest.mark.django_db
def test_not_exist_email_user():
    user_data = {
        "email": "",
        "password": "testpassword",
        "name": "Test User",
        "birthday": "19900101",
        "gender": "M"
    }
    User.objects.all().delete()
    with pytest.raises(ValueError, match='이메일 주소를 입력해야합니다.'):
        user = User.objects.create_user(**user_data)