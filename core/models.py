import enum
import json
import warnings

import rest_framework.serializers
from rest_framework import status
from dataclasses import dataclass
from django.db import models

# Create your models here.

class StatusHandlerMeta(type):
    def __init__(cls, *args, **kwargs):
        super().__init__(cls)
        for attr, obj in cls.__dict__.items():
            if 'CODE_' in attr:
                obj: StatusObject
                obj.code = attr.split('_')[-1]

# API 성공/실패 여부 Enum 클래스
class API_STATUS(enum.Enum):
    SUCCESS = "success"
    FAIL = "fail"

@dataclass
class StatusObject:
    drf_status: status = status.HTTP_400_BAD_REQUEST
    status: str = API_STATUS.FAIL.value
    code: str = ''
    message: str = ''

    def get_instance(self):
        return {
            'status': self.status,
            'code': self.code,
            'message': self.message,
            'result': None
        }

    # api문서의 상태 객체 형태 반환기
    def get_status_html(self, result=None):
        if not result:
            result = 'null'
        value_base = {
            "status": self.status,
            "code": self.code,
            "message": self.message,
            "result": result
        }
        # 위의 dict를 json으로 변환
        value_base = json.dumps(
            value_base,
            indent=4,
            separators=(',', ': '),
            ensure_ascii=False,
        )
        # 줄바꿈처리
        value_base = value_base.replace('",', '",\n')
        return f'\n\n> **{self.message}**\n\n```\n' + \
            '' + \
            f'{value_base}' + \
            '\n\n```'

    def status_result_dict(self):
        from core.serializers import ResponseBaseSerializer
        return ResponseBaseSerializer(
            instance=self.get_instance(),
            many=False
        ).data

    def get_base_response_serializer(self):
        from core.serializers import ResponseBaseSerializer
        return ResponseBaseSerializer(
            instance=self.get_instance(),
            many=False
        )

    def get_status_response(self):

        from rest_framework.response import Response
        return Response(
            status=self.drf_status,
            data=self.status_result_dict()
        )

    def get_custom_status_result_dict(self, custom_result):
        from core.serializers import ResponseBaseSerializer
        return_data = ResponseBaseSerializer(
            instance=self.get_instance(),
            many=False
        ).data
        return_data['result'] = custom_result
        return return_data

    # result가 null이 아닌 커스텀 상태 응답 반환시
    # 사용하는 메서드.
    def get_custom_status_response(self, custom_result):
        print(self.drf_status)
        print(self.status_result_dict())
        from rest_framework.response import Response
        return Response(
            status=self.drf_status,
            data=self.get_custom_status_result_dict(custom_result)
        )

    def create_response(
            self,
            instance=None,
            serializing_class=None,
            many=False,
            context=None):
        # serializing class 가 없는 경우
        # base status response 반환
        if not serializing_class:
            return self.get_status_response()

        # response serializing class 가 있는 경우
        # ResponseBaseSerializer 를 상속 받았는지 확인한다.
        from core.serializers import ResponseBaseSerializer
        if not issubclass(serializing_class, ResponseBaseSerializer):
            raise ValueError('유효하지 않은 serializing_class 입니다.')

        # 응답바디 클래스 get
        response_body_class = serializing_class.get_response_body_class()
        from rest_framework.response import Response
        return Response(
            status=status.HTTP_200_OK,
            data={
                **self.status_result_dict(),
                'result': response_body_class(
                    instance,
                    many=many,
                    context=context,
                ).data,
            },
        )

class APIResponseHandler(metaclass=StatusHandlerMeta):

    # 성공응답코드
    # 모든 에러코드중 유일하게 성공을 담당
    CODE_0000 = StatusObject(
        drf_status=status.HTTP_200_OK,
        status=API_STATUS.SUCCESS.value,
        message='정상적으로 수행되었습니다.'
    )

    # 에러응답코드
    CODE_0001 = StatusObject(
        message='잘못된 요청입니다.'
    )

    CODE_0002 = StatusObject(
        message='요청양식에 맞지 않습니다.'
    )

    CODE_0003 = StatusObject(
        message='존재하지 않는 대상입니다.'
    )

    CODE_0004 = StatusObject(
        message='준비중인 기능입니다.'
    )

    CODE_0005 = StatusObject(
        message='이미 존재하는 유저입니다.'
    )

    CODE_0006 = StatusObject(
        message='작업 권한이 존재하지 않습니다.'
    )

    CODE_0007 = StatusObject(
        message='비밀번호가 일치하지 않습니다.'
    )

    CODE_0008 = StatusObject(
        message='데이터 처리중 서버 내부 에러 발생.'
    )

    CODE_0009 = StatusObject(
        message='이미 계정이 존재하므로 계정정보를 반환합니다.'
    )

    CODE_0010 = StatusObject(
        message='비밀번호를 변경할 수 없는 유저입니다.'
    )

    CODE_0011 = StatusObject(
        message='이메일 전송에 실패하였습니다.'
    )

    CODE_0012 = StatusObject(
        message='이미 존재하는 대상입니다.'
    )

    @classmethod
    def create_success_response(
            cls,
            serializing_class,
            instance,
            many=False,
            context=None, ):
        warnings.warn("추후 제거 될 예정 입니다. create_response 를 대신 사용 할 것을 권장 합니다.", DeprecationWarning)
        if not issubclass(serializing_class, rest_framework.serializers.Serializer):
            raise ValueError('유효하지 않은 serializing_class 입니다.')
        from rest_framework.response import Response
        return Response(
            status=status.HTTP_200_OK,
            data=serializing_class(
                instance={
                    **cls.CODE_0000.status_result_dict(),
                    'result': instance,
                },
                many=many,
                context=context
            ).data
        )

    # 지정된 serializing class 내부의
    # response body serializer 를 찾아낸다음,
    # many, context 등의 파라미터를 동적으로 적용할 수 있음.
    # serializing_class가 지정되지 않은 경우는
    # 시리얼라이징할 내용이 없음으로 판단하여
    # error_object를 통해 기본응답을 반환한다.
    @classmethod
    def create_response(
            cls,
            status_object: StatusObject,
            instance=None,
            serializing_class=None,
            many=False,
            context=None):
        # serializing class 가 없는 경우
        # base status response 반환
        if not serializing_class:
            return status_object.get_status_response()

        # response serializing class 가 있는 경우
        # ResponseBaseSerializer 를 상속 받았는지 확인한다.
        from core.serializers import ResponseBaseSerializer
        if not issubclass(serializing_class, ResponseBaseSerializer):
            raise ValueError('유효하지 않은 serializing_class 입니다.')

        # 응답바디 클래스 get
        response_body_class = serializing_class.get_response_body_class()
        from rest_framework.response import Response
        return Response(
            status=status.HTTP_200_OK,
            data={
                **status_object.status_result_dict(),
                'result': response_body_class(
                    instance,
                    many=many,
                    context=context,
                ).data,
            },
        )

    @classmethod
    def get_all_codes(cls):
        return [v.code for k, v in cls.__dict__.items() if 'CODE_' in k]

    @classmethod
    def get_all_message(cls):
        return [v.message for k, v in cls.__dict__.items() if 'CODE_' in k]