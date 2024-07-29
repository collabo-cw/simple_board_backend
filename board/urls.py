from django.urls import path
from . import views


urlpatterns = [
    path("get/board-list", views.board_list_up, name='board_list'),
]