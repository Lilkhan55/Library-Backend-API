from django.contrib.auth.views import LogoutView
from django.urls import path
from django.views.generic import TemplateView
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import reverse_lazy

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from . import views

app_name = 'users'

urlpatterns = [
    path('api/v1/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/v1/registration/', views.RegisterAPIView.as_view(), name='register'),
    path('api/v1/userlist/', views.UserAPIView.as_view(), name='register')
]
