from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import (
    ChangePasswordAPIView,
    DeleteAccountAPIView,
    RegisterAPIView,
    UserModelViewSet,
    ImageModelViewSet,
    ForgotPasswordAPIView,
    ForgotPasswordConfirmAPIView
)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("its-me", UserModelViewSet)
router.register("image", ImageModelViewSet)


urlpatterns = [
    # path('userinfo/', UserGetAPIView.as_view()),
    path("", include(router.urls)),
    path("register/", RegisterAPIView.as_view(), name="register"),
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path(
        "change_password/",
        ChangePasswordAPIView.as_view(),
        name="change_password",
    ),
    path("refresh", TokenRefreshView.as_view()),
    path(
        "delete/",
        DeleteAccountAPIView.as_view(),
        name="delete-account",
    ),
    path('forgot_password/', ForgotPasswordAPIView.as_view()),
    path('forgot_password_confirm/', ForgotPasswordConfirmAPIView.as_view()),
]
