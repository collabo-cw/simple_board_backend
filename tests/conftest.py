import pytest
import os
from django.conf import settings
from dotenv import load_dotenv
import django


load_dotenv()
# Django 설정 모듈 설정
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'simple_board_backend.settings')  # 실제 프로젝트 설정 모듈 경로로 변경
# Django 초기화
django.setup()

@pytest.fixture(scope='session')
def django_db_setup():
    settings.DATABASES['default'] = {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'test_simple_board',  # 테스트 데이터베이스 이름
        'USER': os.getenv('DATABASE_USER'),
        'PASSWORD': os.getenv('DATABASE_PASSWORD'),
        'HOST': os.getenv('DATABASE_HOST'),
        'PORT': os.getenv('DATABASE_PORT')
    }