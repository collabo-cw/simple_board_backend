from rest_framework import serializers

from core.serializers import ResponseBaseSerializer
from core.utils import EnumChoice
from .models import Board

class BoardListUpRequestSerializer(serializers.Serializer):
    '''
        게시판 목록 요청 시리얼라이저
    '''

    class BoardCategoryEnum(EnumChoice):
        NOTICE = '공지사항'
        GENERAL = '일반 게시판'
        QNA = '질문 게시판'

    category_type = serializers.ListSerializer(
        child=serializers.ChoiceField(
            choices=BoardCategoryEnum.get_choice()
        ),
        help_text='게시판 타입',
    )

# 게시판 목록 응답 시리얼라이저
class BoardListUpResponseSerializer(ResponseBaseSerializer):
    class BoardListUpResponseBody(serializers.Serializer):
        # 카테고리
        category = serializers.ChoiceField(
            help_text='게시판 카테고리',
            choices=Board.category_choices
        )
        # 작성자
        def get_author(self, instance):
            return instance.user.name
        # 게시글 제목
        def get_title(self, instance):
            pass
        # 생성일
        def get_created_at(self, instance):
            pass
        # 조회수
        def get_view_count(self, instance):
            pass

    result = BoardListUpResponseBody()