import inspect
from rest_framework import serializers
from .models import APIResponseHandler

class ResponseBaseSerializer(serializers.Serializer):
    @classmethod
    def get_response_body_class(cls):
        response_body_class = None
        for attr, obj in cls.__dict__.items():
            if inspect.isclass(obj) and issubclass(obj, serializers.Serializer):
                response_body_class = obj
                break

        if not response_body_class:
            raise ValueError('응답 바디 객체가 없습니다.')
        return response_body_class

    @classmethod
    def get_base_dict(cls):
        print('넘어온 클래스 : ', cls)
        return cls(instance=None).data

    status = serializers.ChoiceField(
        choices=('success', 'fail'),
    )
    code = serializers.ChoiceField(
        choices=APIResponseHandler.get_all_codes(),
    )
    message = serializers.ChoiceField(
        choices=APIResponseHandler.get_all_message(),
    )
    result = serializers.Serializer(default=None, allow_null=True)