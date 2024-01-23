from django.urls import path
from .views import Register, SalerLogin, UpdateSalerPassword, SalerPasswordChange

urlpatterns = [
    path('register/', Register.as_view()),
    path('login/', SalerLogin.as_view()),
    path('update/', UpdateSalerPassword.as_view()),
    path('change/', SalerPasswordChange.as_view()),



]
