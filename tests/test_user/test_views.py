import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from user.models import User


@pytest.mark.django_db
class TestUserSignUp:

    @pytest.fixture
    def api_client(self):
        return APIClient()

    @pytest.fixture
    def valid_user_data(self):
        return {
            "email": "test@example.com",
            "password": "strong_password",
            "name": "Test User",
            "birthday": "1990-01-01",
            "gender": "M"
        }

    @pytest.fixture
    def invalid_user_data(self):
        return {
            "email": "invalid-email",
            "password": "",
            "name": "",
            "birthday": "",
            "gender": ""
        }

    def test_user_sign_up_success(self, api_client, valid_user_data):
        User.objects.all().delete()
        url = reverse('user-sign-up')
        response = api_client.post(url, valid_user_data, format='json')
        assert response.status_code == 200
        assert User.objects.filter(email=valid_user_data['email']).exists()

    def test_user_sign_up_invalid_data(self, api_client, invalid_user_data):
        User.objects.all().delete()
        url = reverse('user-sign-up')
        response = api_client.post(url, invalid_user_data, format='json')
        assert response.status_code == 400

    def test_user_sign_up_existing_user(self, api_client, valid_user_data):
        User.objects.all().delete()
        # 먼저 유저를 생성합니다.
        url = reverse('user-sign-up')
        api_client.post(url, valid_user_data, format='json')
        response = api_client.post(url, valid_user_data, format='json')
        assert response.status_code == 400  # 이미 존재하는 유저에 대한 응답 코드 확인
