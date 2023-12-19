from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import ForLoginSerializer
from drf_yasg.utils import swagger_auto_schema
from .models import SalerApp
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken


class Register(APIView):
    serializer_class = ForLoginSerializer

    @swagger_auto_schema
    def post(self, request):
        serializer = ForLoginSerializer(data=request.data)
        if serializer.is_valid():
            seriya = request.data.get("")
            seriya_raqam = request.data.get("")
            password = request.data.get("")
            login = request.data.get("")
            tel_raqam = request.data.get("")
            crt = SalerApp.objects.create(tel_raqam=tel_raqam, login=login, password=password,
                                           ps_seriya_raqam=seriya_raqam, ps_seriya=seriya)
            user = SalerApp.objects.filter(ps_seriya=seriya, ps_seriya_raqam=seriya_raqam, password=password).first()

    if user:
        acsess_token = AccessToken.for_user(user)
        refresh_token = RefreshToken(user)
        # serializer.save()  # Save the serializer after creating the user
        return Response({"Register Success": str(acsess_token),
                         })
    else:
        return Response({"error": "User not found with provided credentials"},
                        status=status.HTTP_400_BAD_REQUEST)
    else:
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginUser(APIView):
    serializer_class = ForLoginSerializer

    @swagger_auto_schema
    def post(self, request):
        seriya = request.data.get("PasportSeria")
        seriya_raqam = request.data.get("PasportNumber")
        password = request.data.get("password")
        user = UserModel.objects.filter(password=password, PasportSeria=seriya, PasportNumber=seriya_raqam).first()
        return Response({"Login saccess": user.id})
