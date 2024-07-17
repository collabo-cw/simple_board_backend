from django.urls import path
from . import views

urlpatterns = [
    path("user-sign-up", views.user_sign_up),
]