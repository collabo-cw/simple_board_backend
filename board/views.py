from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from core.models import APIResponseHandler
from board.serializers import BoardListUpRequestSerializer, BoardListUpResponseSerializer, \
    BoardRegisterRequestSerializer, BoardDetailRequestSerializer, BoardDetailResponseSerializer
from core.utils import calculate_pagination_max_page, set_atomic_transaction


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
    '''
        게시판 목록 조회 API
    '''
    # 요청 데이터 검증
    request_validator = BoardListUpRequestSerializer(data=request.data)
    if not request_validator.is_valid():
        print('양식에 맞지 않습니다.')
        print(request_validator.errors)
        return APIResponseHandler.CODE_0002.get_status_response()
    print(request_validator.validated_data)

    category = request_validator.data.get('category_type')
    page_size = request_validator.data.get('page_size')
    # 분류 유형 ex) 날짜순, 이름순, 조회수 순
    categorize_type = request_validator.data.get('categorize_type')
    desc = request_validator.data.get('desc', False)

    from .models import Board
    board_qs = Board.objects.filter(
        category=category
    )
    if not board_qs.exists():
        return APIResponseHandler.CODE_0003.get_status_response()

    # 오더링
    ordering = '-id'
    if categorize_type == request_validator.CategorizeEnum.CREATED.name:
        ordering = '-created_at'
    elif categorize_type == request_validator.CategorizeEnum.ABC.name:
        ordering = '-title'
    elif categorize_type == request_validator.CategorizeEnum.HITS.name:
        ordering = '-view_count'
    else:
        ordering = '-id'

    # 순서 방향
    if desc:
        if ordering.startswith('-'):
            ordering = ordering[1:]
        else:
            ordering = f'-{ordering}'

    board_qs = board_qs.order_by(ordering)

    # 페이징
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
        context=context,
        many=True,
    )

# 게시판 등록 API

@swagger_auto_schema(
    method="POST",
    request_body=BoardRegisterRequestSerializer,
    responses={
        status.HTTP_200_OK: APIResponseHandler.CODE_0000.get_status_html(),
        status.HTTP_400_BAD_REQUEST: APIResponseHandler.CODE_0002.get_status_html() +
                                     APIResponseHandler.CODE_0003.get_status_html()
    },
)
@api_view(["POST"])
@set_atomic_transaction
def board_register(request: Request):
    '''
        게시판 등록 API
    '''
    # 요청 데이터 검증
    request_validator = BoardRegisterRequestSerializer(data=request.data)
    if not request_validator.is_valid():
        print('양식에 맞지 않습니다.')
        print(request_validator.errors)
        return APIResponseHandler.CODE_0002.get_status_response()
    print(request_validator.validated_data)

    category = request_validator.data.get('category')
    user_id = request_validator.data.get('user_id')
    guest_id = request_validator.data.get('guest_id')
    password = request_validator.data.get('password')
    title = request_validator.data.get('title')
    content = request_validator.data.get('content')
    file = request_validator.data.get('file')

    # 유저가 없을수도 있음
    from user.models import User
    from .models import Board, Attachment

    user_qs = User.objects.filter(
        external_uuid=user_id,
        is_active=True
    )
    if user_qs.exists():
        user = user_qs.first()
        board_instance = Board.objects.create(
            category=category,
            author=user,
            title=title,
            content=content,
        )
    else:
        if not guest_id or password:
            return APIResponseHandler.CODE_0001.get_status_response()
        board_instance = Board.objects.create(
            category=category,
            guest_author=guest_id,
            password=password,
            title=title,
            content=content,
        )

    if file:
        for i,obj in enumerate(file):
            Attachment.objects.create(
                board=board_instance,
                file=obj,
                order=i,
            )

    return APIResponseHandler.CODE_0000.get_status_response()

# 게시판 상세보기 API
@swagger_auto_schema(
    method="POST",
    request_body=BoardDetailRequestSerializer,
    responses={
        status.HTTP_200_OK: BoardDetailResponseSerializer,
        status.HTTP_400_BAD_REQUEST: APIResponseHandler.CODE_0002.get_status_html() +
                                     APIResponseHandler.CODE_0003.get_status_html()
    },
)
@api_view(["POST"])
@set_atomic_transaction
def board_detail(request: Request):
    '''
        게시판 상세 조회 API
    '''
    # 요청 데이터 검증
    request_validator = BoardDetailRequestSerializer(data=request.data)
    if not request_validator.is_valid():
        print('양식에 맞지 않습니다.')
        print(request_validator.errors)
        return APIResponseHandler.CODE_0002.get_status_response()
    print(request_validator.validated_data)

    id = request_validator.data.get('id')
    category = request_validator.data.get('category')

    # 게시판 정보가 있는지 확인

    from .models import Board
    board_qs = Board.objects.filter(
        id=id,
        category=category,
        is_activate=True
    )
    if not board_qs.exists():
        return APIResponseHandler.CODE_0003.get_status_response()

    board = board_qs.first()
    # 게시판을 클릭한것과 마찬가지 이므로 조회수 +1 해준다
    board.view_count += board.view_count
    board.save(update_fields=['view_count'])

    return APIResponseHandler.create_response(
        status_object=APIResponseHandler.CODE_0000,
        serializing_class=BoardDetailResponseSerializer,
        instance=board
    )