from django.urls import path
from .views import RegisterView, LoginAPIView, LogoutAPIView, ProfileViewAPIView, ProfileEditAPIView, PhoneEntryAPIView, PhoneVerificationAPIView

urlpatterns = [
    path('register/', RegisterView.as_view(), name="register"),
    path('login/', LoginAPIView.as_view(), name="login"),
    path('logout/', LogoutAPIView.as_view(), name="logout"),
    path('profile/<str:username>/', ProfileViewAPIView.as_view(), name="profile-view"),
    path('profile/<str:username>/edit/', ProfileEditAPIView.as_view(), name="profile-edit"),
    path('profile/<str:username>/phone-entry/', PhoneEntryAPIView.as_view(), name="phone-entry"),
    path('profile/<str:username>/phone-verify/', PhoneVerificationAPIView.as_view(), name="phone-verify")
]
