from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from core.models import APIResponseHandler
from board.serializers import BoardListUpRequestSerializer, BoardListUpResponseSerializer
from core.utils import calculate_pagination_max_page
from .models import Board

#게시판 목록 조회 API
@swagger_auto_schema(
    method="POST",
    request_body=BoardListUpRequestSerializer,
    responses={
        status.HTTP_200_OK: BoardListUpResponseSerializer,
        status.HTTP_400_BAD_REQUEST: APIResponseHandler.CODE_0002.get_status_html() +
                                     APIResponseHandler.CODE_0003.get_status_html()
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
    page_size = request_validator.data.get('page_size')
    # 분류 유형 ex) 날짜순, 이름순, 조회수 순
    categorize_type = request_validator.data.get('categorize_type')
    desc = request_validator.data.get('desc', False)

    board_qs = Board.objects.filter(
        category=category
    )
    if not board_qs.exists():
        return APIResponseHandler.CODE_0003.get_status_response()

    ordering = '-id'
    if categorize_type == request_validator.CategorizeEnum.CREATED.name:
        ordering = '-created_at'
    elif categorize_type == request_validator.CategorizeEnum.ABC.name:
        ordering = '-title'
    elif categorize_type == request_validator.CategorizeEnum.HITS.name:
        ordering = '-view_count'
    else:
        ordering = '-id'

    if desc:
        if ordering.startswith('-'):
            ordering = ordering[1:]
        else:
            ordering = f'-{ordering}'

    board_qs = board_qs.order_by(ordering)

    from rest_framework.pagination import PageNumberPagination
    paginator = PageNumberPagination()
    paginator.page_size = page_size
    paginated_qs = paginator.paginate_queryset(
        board_qs,
        request=request
    )
    count = board_qs.count()
    next_link = paginator.get_next_link()
    previous_link = paginator.get_previous_link()

    context = {
        'count': count,
        'page_size': paginator.page_size,
        'current_page': paginator.page.number,
        'next_link': next_link,
        'max_page': calculate_pagination_max_page(count, page_size),
        'previous_link': previous_link,
        'paginated_qs': paginated_qs,
        'board': board_qs,
    }

    return APIResponseHandler.create_response(
        status_object=APIResponseHandler.CODE_0000,
        serializing_class=BoardListUpResponseSerializer,
        instance=paginated_qs,
        context=context
    )