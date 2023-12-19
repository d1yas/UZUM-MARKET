from django.urls import path, include

from .views import LoginUser, Register

urlpatterns = [
    path("login", LoginUser.as_view()),
    path("register/", Register.as_view()),
]
