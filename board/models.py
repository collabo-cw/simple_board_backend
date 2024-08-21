from django.db import models

from core.utils import EnumChoice
from user.models import User
# Create your models here.

class Board(models.Model):

    class category_choices(EnumChoice):
        notice = '공지사항',
        general = '일반 게시판',
        qna = '질문 게시판',

    # 카테고리
    category = models.CharField(
        max_length=10,
        choices=category_choices.get_choice(),
        verbose_name="카테고리",
        help_text="카테고리"
    )

    # 작성자 유저
    # 널을 허용하는 이유는 비회원도 글을 사용할 수 있기 때문에 널을 허용해준다.
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='boards',
        verbose_name="작성자",
        help_text="작성자(유저)",
        null=True,
        blank=False
    )

    # 작성자 비회원
    guest_author = models.CharField(
        max_length=5,
        help_text='작성자(비회원)',
        null=True,
        blank=False
    )

    # 작성자 암호
    guest_password = models.CharField(
        max_length=15,
        help_text='비회원 작성자 암호',
        null=True,
        blank=False
    )

    # 게시글 제목
    title = models.CharField(
        max_length=100,
        verbose_name="제목",
        help_text="게시글 제목"
    )

    # 게시글 내용
    content = models.TextField(
        verbose_name="내용",
        help_text="게시글 내용"
    )

    # 생성일
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="작성일",
        help_text="생성일"
    )

    # 수정일
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="수정일",
        help_text="수정일"
    )

    # 조회수
    view_count = models.PositiveIntegerField(
        default=0,
        verbose_name="조회수",
        help_text="조회수"
    )

    is_activate = models.BooleanField(
        default=True,
        verbose_name='활성화 여부',
    )

    def __str__(self):
        return self.title


# 첨부파일 관련 모델
class Attachment(models.Model):

    board = models.ForeignKey(
        Board,
        on_delete=models.CASCADE,
        related_name='attachments',
        verbose_name="게시글",
        help_text="게시글"
    )

    file = models.FileField(
        upload_to='attachments/',
        verbose_name="첨부파일",
        help_text='첨부파일'
    )

    uploaded_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="업로드 일시",
        help_text="업로드 생성일"
    )

    order = models.PositiveIntegerField(
        default=0,
        verbose_name="순서",
        help_text='첨부파일 순서'
    )

    def __str__(self):
        return f"{self.board.title} - {self.file.name}"