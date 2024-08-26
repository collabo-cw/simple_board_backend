from django.contrib.auth import authenticate
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from core.models import APIResponseHandler
from .serializers import UserSignUpRequestSerializer, UserSignInRequestSerializer, UserSignInResponseSerializer
from rest_framework_simplejwt.tokens import RefreshToken


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
    # 요청 데이터 검증
    request_validator = UserSignUpRequestSerializer(data=request.data)
    if not request_validator.is_valid():
        print('양식에 맞지 않습니다.')
        print(request_validator.errors)
        return APIResponseHandler.CODE_0002.get_status_response()

    print(request_validator.validated_data)
    # 유저 데이터 리스트로 만들고
    user_data:list = request_validator.get_data_for_user_create()
    # 회원인지 아닌지 체크
    from .models import User
    user_qs = User.objects.filter(
        email=request_validator.data.get('email'),
        is_active=True
    )
    if user_qs.exists():
        print('이미 존재하는 유저입니다.')
        return APIResponseHandler.CODE_0005.get_status_response()

    # 유저모델에 유저데이터 리스트를 전달한다.
    user_manager = User.objects
    user = user_manager.create_user(**user_data)
    print('생성된 유저 : ', user)

    return APIResponseHandler.CODE_0000.get_status_response()

# 로그인
@swagger_auto_schema(
    method="POST",
    request_body=UserSignInRequestSerializer,
    responses={
        status.HTTP_200_OK: UserSignInResponseSerializer,
        status.HTTP_400_BAD_REQUEST: APIResponseHandler.CODE_0002.get_status_html() +
                                     APIResponseHandler.CODE_0003.get_status_html(),
    },
)
@api_view(["POST"])
def user_login(request: Request):
    '''
        유저 로그인 API
        로그인이 되면 Access Token 과 RefreshToken, user의 uuid를 전달해주는 API,
    '''
    # 요청 데이터 검증
    request_validator = UserSignInRequestSerializer(data=request.data)
    if not request_validator.is_valid():
        print('양식에 맞지 않습니다.')
        print(request_validator.errors)
        return APIResponseHandler.CODE_0002.get_status_response()

    print(request_validator.validated_data)

    email = request_validator.data.get('email')
    password = request_validator.data.get('password')

    # 유저의 이메일과 비밀번호가 일치하면 그유저의 정보를 가져온다
    user = authenticate(
        email=email,
        password=password
    )

    if not user or not user.is_active:
        return APIResponseHandler.CODE_0003.get_status_response()

    # JWT TOKEN 과 User의 UUID의 정보를 담는다
    tokens = RefreshToken.for_user(user)
    access_token = str(tokens.access_token)
    refresh_token = str(tokens)

    context = {
        'access_token': access_token,
        'refresh_token': refresh_token
    }

    return APIResponseHandler.create_response(
        status_object=APIResponseHandler.CODE_0000,
        serializing_class=UserSignInResponseSerializer,
        instance=user,
        context=context
    )