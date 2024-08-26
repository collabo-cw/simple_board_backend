from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("user-sign-up", views.user_sign_up, name='user-sign-up'),
    path('login', views.user_login, name='login'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]