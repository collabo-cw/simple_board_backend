from core.serializers import ResponseBaseSerializer, APIResponseHandler
import pytest
from rest_framework import serializers

# 테스트를 위한 더미 클래스들
class DummyResponseBody(serializers.Serializer):
    field = serializers.CharField()

class DummySerializer(ResponseBaseSerializer):
    class ResponseBody(serializers.Serializer):
        field = serializers.CharField()

class EmptySerializer(ResponseBaseSerializer):
    pass

def test_get_response_body_class():
    # 정상적인 경우
    assert DummySerializer.get_response_body_class() == DummySerializer.ResponseBody

    # 응답 바디 객체가 없는 경우
    with pytest.raises(ValueError, match='응답 바디 객체가 없습니다.'):
        EmptySerializer.get_response_body_class()

def test_get_base_dict(capfd):
    base_dict = DummySerializer.get_base_dict()

    # 출력 확인
    out, _ = capfd.readouterr()
    assert "넘어온 클래스 :  <class 'tests.test_core.test_serializers.DummySerializer'>" in out

    # 반환값 확인
    assert isinstance(base_dict, dict)
    assert 'status' in base_dict
    assert 'code' in base_dict
    assert 'message' in base_dict
    assert 'result' in base_dict

def test_status_field():
    serializer = ResponseBaseSerializer()
    assert isinstance(serializer.fields['status'], serializers.ChoiceField)
    assert set(serializer.fields['status'].choices.keys()) == {'success', 'fail'}

def test_code_field():
    serializer = ResponseBaseSerializer()
    assert isinstance(serializer.fields['code'], serializers.ChoiceField)
    assert set(serializer.fields['code'].choices) == set(APIResponseHandler.get_all_codes())

def test_message_field():
    serializer = ResponseBaseSerializer()
    assert isinstance(serializer.fields['message'], serializers.ChoiceField)
    assert set(serializer.fields['message'].choices) == set(APIResponseHandler.get_all_message())

def test_result_field():
    serializer = ResponseBaseSerializer()
    assert isinstance(serializer.fields['result'], serializers.Serializer)
    assert serializer.fields['result'].default is None
    assert serializer.fields['result'].allow_null is True

@pytest.mark.parametrize("data,is_valid", [
    ({"status": "success", "code": APIResponseHandler.CODE_0000.code, "message": APIResponseHandler.CODE_0000.message, "result": None}, True),
    ({"status": "invalid", "code": APIResponseHandler.CODE_0000.code, "message": APIResponseHandler.CODE_0000.message, "result": None}, False),
    ({"status": "success", "code": "invalid", "message": APIResponseHandler.CODE_0000.message, "result": None}, False),
    ({"status": "success", "code": APIResponseHandler.CODE_0000.code, "message": "invalid", "result": None}, False),
])
def test_serializer_validation(data, is_valid):
    serializer = ResponseBaseSerializer(data=data)
    assert serializer.is_valid() == is_valid