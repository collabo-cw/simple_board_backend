from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from core.models import APIResponseHandler
from .serializers import UserSignUpRequestSerializer

# 회원가입
@swagger_auto_schema(
    method="POST",
    request_body=UserSignUpRequestSerializer,
    responses={
        status.HTTP_200_OK: APIResponseHandler.CODE_0000.get_status_html(),
        status.HTTP_400_BAD_REQUEST: APIResponseHandler.CODE_0002.get_status_html() +
                                     APIResponseHandler.CODE_0005.get_status_html(),
    },
)
@api_view(["POST"])
def user_sign_up(request: Request):
    request_validator = UserSignUpRequestSerializer(data=request.data)
    if not request_validator.is_valid():
        print('양식에 맞지 않습니다.')
        print(request_validator.errors)
        return APIResponseHandler.CODE_0002.get_status_response()

    print(request_validator.validated_data)
    user_data = request_validator.get_data_for_user_create()

    from .models import User
    user_qs = User.objects.filter(
        email=request_validator.data.get('email'),
        is_active=True
    )
    if user_qs.exists():
        print('이미 존재하는 유저입니다.')
        return APIResponseHandler.CODE_0005.get_status_response()

    user_manager = User.objects
    user = user_manager.create_user(**user_data)
    print('생성된 유저 : ', user)

    return APIResponseHandler.CODE_0000.get_status_response()