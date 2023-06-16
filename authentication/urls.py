from django.urls import path
from .views import RegisterView, LoginAPIView, LogoutAPIView, ProfileViewAPIView, ProfileEditAPIView

urlpatterns = [
    path('register/', RegisterView.as_view(), name="register"),
    path('profile/<str:username>', RegisterView.as_view(), name="profile"),
    path('login/', LoginAPIView.as_view(), name="login"),
    path('logout/', LogoutAPIView.as_view(), name="logout"),
    path('profile/<str:username>/', ProfileViewAPIView.as_view(), name="profile-view"),
    path('profile/<str:username>/edit/', ProfileEditAPIView.as_view(), name="profile-edit"),
]
