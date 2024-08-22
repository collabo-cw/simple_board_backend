from django.urls import path
from . import views


urlpatterns = [
    # 게시판 리스트 목록 보기 API
    path("get/board-list", views.board_list_up, name='board_list'),
    # 게시판 생성 API
    path("create/board", views.board_register, name='board_create'),
    # 게시판 상세 API
    path("get/board-detail", views.board_detail, name='board_detail'),
]