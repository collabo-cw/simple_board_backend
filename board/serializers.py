from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers

from core.serializers import ResponseBaseSerializer
from core.utils import EnumChoice, validate_file_extension
from .models import Board, Attachment


class BoardCategoryEnum(EnumChoice):
    NOTICE = '공지사항'
    GENERAL = '일반 게시판'
    QNA = '질문 게시판'

class BoardListUpRequestSerializer(serializers.Serializer):
    '''
        게시판 목록 요청 시리얼라이저
    '''

    class BoardCategoryEnum(EnumChoice):
        NOTICE = '공지사항'
        GENERAL = '일반 게시판'
        QNA = '질문 게시판'

    class CategorizeEnum(EnumChoice):
        CREATED = '작성일 기준'
        ABC = '글자순'
        HITS = '조회수 기준'

    category_type = serializers.ChoiceField(
        choices=BoardCategoryEnum.get_choice(),
        help_text='게시판 타입',
    )

    page_size = serializers.IntegerField(
        min_value=10,
        max_value=100,
        help_text='페이지 사이즈',
        default=10
    )

    categorize_type = serializers.ChoiceField(
        choices=CategorizeEnum.get_choice(),
        help_text='분류 기준',
        required=True,
    )

    desc = serializers.BooleanField(
        help_text='역순 flag',
        default=False,
    )

class BoardListItemSerializer(serializers.ModelSerializer):

    def get_id(self, instance:Board):
        return instance.pk
    # 작성자
    def get_author(self, instance:Board):
        if not instance.author.name:
            return None
        else:
            return instance.author.name

    # 작성자 비회원
    def get_guest_author(self, instance:Board):
        if not instance.guest_author:
            return None
        else:
            return instance.guest_author

    # 게시글 제목
    def get_title(self, instance:Board):
        return instance.title

    # 생성일
    def get_created_at(self, instance:Board):
        return instance.created_at

    # 조회수
    def get_view_count(self, instance:Board):
        return instance.view_count

    id = serializers.SerializerMethodField(
        help_text='게시판 id'
    )

    author = serializers.SerializerMethodField(
        help_text='작성자'
    )

    guest_author = serializers.SerializerMethodField(
        help_text='작성자(비회원)'
    )

    title = serializers.SerializerMethodField(
        help_text='제목'
    )

    created_at = serializers.SerializerMethodField(
        help_text='생성일'
    )

    view_count = serializers.SerializerMethodField(
        help_text='조회수'
    )

    class Meta:
        model = Board
        fields = (
            'id',
            'author',
            'guest_author',
            'title',
            'created_at',
            'view_count'
        )

# 게시판 목록 응답 시리얼라이저
class BoardListUpResponseSerializer(ResponseBaseSerializer):
    class BoardListUpResponseBody(serializers.Serializer):
        # 카테고리
        category = serializers.ChoiceField(
            help_text='게시판 카테고리',
            choices=Board.category_choices
        )
        def get_count(self, instance):
            count_val = self.context.get('count', 0)
            return count_val

        def get_page_size(self, instance):
            page_size_val = self.context.get('page_size')
            return page_size_val

        def get_current_page(self, instance):
            current_page_val = self.context.get('current_page')
            return current_page_val

        def get_max_page(self, instance):
            max_page_val = self.context.get('max_page')
            return max_page_val

        def get_next(self, instance):
            next_link = self.context.get('next_link', '')
            return next_link

        def get_previous(self, instance):
            previous_link = self.context.get('previous_link', '')
            return previous_link

        @swagger_serializer_method(
            serializer_or_field=BoardListItemSerializer(many=True)
        )
        def get_item_list(self, instance):
            if isinstance(instance, Board):
                instance = [instance]

            return BoardListItemSerializer(
                instance,
                many=True,
                context=self.context,
            ).data

        count = serializers.SerializerMethodField()
        page_size = serializers.SerializerMethodField()
        current_page = serializers.SerializerMethodField()
        max_page = serializers.SerializerMethodField()
        next = serializers.SerializerMethodField()
        previous = serializers.SerializerMethodField()
        item_list = serializers.SerializerMethodField()

    result = BoardListUpResponseBody()

# 게시판 등록 요청 시리얼라이저
class BoardRegisterRequestSerializer(serializers.Serializer):
    '''
        게시판 등록 요청 시리얼라이저
    '''

    category = serializers.ChoiceField(
        choices=BoardCategoryEnum.get_choice(),
        help_text='카테고리',
    )

    user_id = serializers.UUIDField(
        help_text='유저 UUID',
        allow_null=True,
        required=False
    )

    guest_id = serializers.CharField(
        max_length=10,
        help_text='비회원 작성자',
        allow_null=True,
        required=False
    )

    password = serializers.CharField(
        max_length=15,
        help_text='비회원 암호',
        allow_null=True,
        required=False
    )

    title = serializers.CharField(
        help_text='게시글 제목',
    )

    content = serializers.CharField(
        help_text='게시글 내용'
    )

    file = serializers.ListSerializer(
        child=serializers.FileField(validators=[validate_file_extension]),
        help_text='첨부파일',
        required=False,
        allow_empty=True,
        default=list
    )

# 게시판 상세 보기 요청 시리얼라이저
class BoardDetailRequestSerializer(serializers.Serializer):
    id = serializers.IntegerField(
        help_text='게시판 id',
        required=True,
        min_value=1
    )

    category = serializers.ChoiceField(
        choices=BoardCategoryEnum.get_choice(),
        help_text='카테고리',
        default='GENERAL'
    )

# 게시판 첨부파일 아이템 시리얼라이저
class BoardDetailAttachmentItemSerializer(serializers.Serializer):
    def get_file(self, instance:Attachment):
        return instance.file

    def get_order(self, instance:Attachment):
        return instance.order

    file = serializers.SerializerMethodField()
    order = serializers.SerializerMethodField()

# 게시판 상세 보기 응답 시리얼라이저
class BoardDetailResponseSerializer(ResponseBaseSerializer):
    class BoardDetailResponseBody(serializers.Serializer):

        def get_id(self, instance: Board):
            return instance.pk

        # 작성자
        def get_author(self, instance: Board):
            if not instance.author:
                return None
            else:
                return instance.author.name

        # 작성자 비회원
        def get_guest_author(self, instance: Board):
            if not instance.guest_author:
                return None
            else:
                return instance.guest_author

        # 게시글 제목
        def get_title(self, instance: Board):
            return instance.title

        # 생성일
        def get_created_at(self, instance: Board):
            return instance.created_at

        # 조회수
        def get_view_count(self, instance: Board):
            return instance.view_count

        # 첨부파일
        @swagger_serializer_method(
            serializer_or_field=BoardDetailAttachmentItemSerializer(many=True)
        )
        def get_file_item(self, instance: Board):
            from .models import Attachment
            # 첨부파일이 있는지 확인
            attachment = Attachment.objects.filter(
                board=instance.pk
            )
            return BoardDetailAttachmentItemSerializer(
                attachment,
                many=True,
                context=self.context,
            ).data


        id = serializers.SerializerMethodField(
            help_text='게시판 id'
        )

        author = serializers.SerializerMethodField(
            help_text='작성자'
        )

        guest_author = serializers.SerializerMethodField(
            help_text='작성자(비회원)'
        )

        title = serializers.SerializerMethodField(
            help_text='제목'
        )

        created_at = serializers.SerializerMethodField(
            help_text='생성일'
        )

        view_count = serializers.SerializerMethodField(
            help_text='조회수'
        )

        file_item = serializers.SerializerMethodField(
            help_text='첨부 파일'
        )

    result = BoardDetailResponseBody()