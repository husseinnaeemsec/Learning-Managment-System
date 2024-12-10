from django.urls import path
from .views import RegisterAPIView, LoginAPIView, LogoutAPIView,CheckAuthenticationAPIView

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('check/', CheckAuthenticationAPIView.as_view(), name='check-auth')
]
