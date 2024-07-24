import pytest
from rest_framework import status
from core.models import APIResponseHandler, StatusObject, API_STATUS


@pytest.fixture
def status_object():
    return StatusObject(
        drf_status=status.HTTP_400_BAD_REQUEST,
        status=API_STATUS.FAIL.value,
        message='테스트 메시지'
    )

def test_status_object_get_instance(status_object):
    instance = status_object.get_instance()
    assert instance['status'] == API_STATUS.FAIL.value
    assert instance['code'] == ''
    assert instance['message'] == '테스트 메시지'
    assert instance['result'] is None


def test_status_object_get_status_html(status_object):
    html = status_object.get_status_html()
    assert '테스트 메시지' in html

def test_status_result_dict(status_object):
    result_dict = status_object.status_result_dict()

    assert result_dict['status'] == API_STATUS.FAIL.value
    assert result_dict['code'] == ''
    assert result_dict['message'] == '테스트 메시지'
    assert result_dict['result'] is None


def test_base_response_serializer(status_object):
    response_serializer = status_object.get_base_response_serializer()

    assert response_serializer.data['status'] == API_STATUS.FAIL.value
    assert response_serializer.data['code'] == ''
    assert response_serializer.data['message'] == '테스트 메시지'
    assert response_serializer.data['result'] is None

def test_get_status_response(status_object):
    response = status_object.get_status_response()
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data['status'] == API_STATUS.FAIL.value
    assert response.data['code'] == ''
    assert response.data['message'] == '테스트 메시지'


def test_api_response_handler_codes():
    codes = APIResponseHandler.get_all_codes()
    expected_codes = ['0000', '0001', '0002', '0003', '0004', '0005', '0006', '0007', '0008', '0009', '0010', '0011',
                      '0012']
    assert codes == expected_codes


def test_api_response_handler_messages():
    messages = APIResponseHandler.get_all_message()
    expected_messages = [
        '정상적으로 수행되었습니다.', '잘못된 요청입니다.', '요청양식에 맞지 않습니다.',
        '존재하지 않는 대상입니다.', '준비중인 기능입니다.', '이미 존재하는 유저입니다.',
        '작업 권한이 존재하지 않습니다.', '비밀번호가 일치하지 않습니다.', '데이터 처리중 서버 내부 에러 발생.',
        '이미 계정이 존재하므로 계정정보를 반환합니다.', '비밀번호를 변경할 수 없는 유저입니다.', '이메일 전송에 실패하였습니다.',
        '이미 존재하는 대상입니다.'
    ]
    assert messages == expected_messages

def test_api_response_handler_create_response():
    from core.serializers import ResponseBaseSerializer
    class MockResponseBodySerializer(ResponseBaseSerializer):
        def to_representation(self, instance):
            return instance

    class MockSerializer(ResponseBaseSerializer):
        @staticmethod
        def get_response_body_class():
            return MockResponseBodySerializer

    instance = {"key": "value"}
    response = APIResponseHandler.create_response(APIResponseHandler.CODE_0000, instance, MockSerializer)

    assert response.status_code == status.HTTP_200_OK
    assert response.data['status'] == APIResponseHandler.CODE_0000.status
    assert response.data['message'] == APIResponseHandler.CODE_0000.message
    assert response.data['result'] == instance


def test_get_custom_status_result_dict(status_object):
    custom_result = {"key": "custom_value"}
    result_dict = status_object.get_custom_status_result_dict(custom_result)

    assert result_dict['status'] == API_STATUS.FAIL.value
    assert result_dict['code'] == ''
    assert result_dict['message'] == '테스트 메시지'
    assert result_dict['result'] == custom_result


def test_get_custom_status_response(status_object):
    custom_result = {"key": "custom_value"}
    response = status_object.get_custom_status_response(custom_result)

    assert response.status_code == status_object.drf_status
    assert response.data['status'] == API_STATUS.FAIL.value
    assert response.data['code'] == ''
    assert response.data['message'] == '테스트 메시지'
    assert response.data['result'] == custom_result

def test_create_response_without_serializing_class(status_object):
    response = status_object.create_response()

    assert response.status_code == status_object.drf_status
    assert response.data['status'] == API_STATUS.FAIL.value
    assert response.data['code'] == ''
    assert response.data['message'] == '테스트 메시지'
    assert response.data['result'] is None


def test_create_response_with_serializing_class(status_object):
    from core.serializers import ResponseBaseSerializer
    class MockResponseBodySerializer(ResponseBaseSerializer):
        def to_representation(self, instance):
            return instance

    class MockSerializer(ResponseBaseSerializer):
        @staticmethod
        def get_response_body_class():
            return MockResponseBodySerializer

    instance = {"key": "value"}
    response = status_object.create_response(instance, MockSerializer)
    exclude_class_response = APIResponseHandler.create_response(status_object)
    expected_response = status_object.get_status_response()

    assert exclude_class_response.status_code == expected_response.status_code
    assert response.status_code == status.HTTP_200_OK
    assert response.data['status'] == API_STATUS.FAIL.value
    assert response.data['code'] == ''
    assert response.data['message'] == '테스트 메시지'
    assert response.data['result'] == instance

def test_create_response_invalid_serializing_class(status_object):
    class InvalidClass:
        pass

    with pytest.raises(ValueError, match='유효하지 않은 serializing_class 입니다.'):
        status_object.create_response(serializing_class=InvalidClass)

    with pytest.raises(ValueError, match='유효하지 않은 serializing_class 입니다.'):
        APIResponseHandler.create_response(status_object, serializing_class=InvalidClass)
