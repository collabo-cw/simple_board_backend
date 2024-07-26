from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from core.models import APIResponseHandler
from board.serializers import BoardListUpRequestSerializer, BoardListUpResponseSerializer
from .models import Board

#게시판 목록 조회 API
@swagger_auto_schema(
    method="POST",
    request_body=BoardListUpRequestSerializer,
    responses={
        status.HTTP_200_OK: BoardListUpResponseSerializer,
        status.HTTP_400_BAD_REQUEST: APIResponseHandler.CODE_0002.get_status_html()
    },
)
@api_view(["POST"])
def board_list_up(request: Request):
    # 요청 데이터 검증
    request_validator = BoardListUpRequestSerializer(data=request.data)
    if not request_validator.is_valid():
        print('양식에 맞지 않습니다.')
        print(request_validator.errors)
        return APIResponseHandler.CODE_0002.get_status_response()
    print(request_validator.validated_data)

    category = request_validator.data.get('category')

    board_qs = Board.objects.filter(
        category=category
    )

    return APIResponseHandler.create_response(
        status_object=APIResponseHandler.CODE_0000,
        serializing_class=BoardListUpResponseSerializer,
        instance=pass
    )