from drf_yasg.utils import swagger_auto_schema
from .models import SalerRegister
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import ForLoginSerializer, ForRegisterSerializer, SalerChangePasswordSerializer, SalerRecoverPassword
from rest_framework_simplejwt.tokens import RefreshToken


class Register(APIView):
    @swagger_auto_schema(request_body=ForRegisterSerializer)
    def post(self, request):
        serializer = ForRegisterSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"msg": "registered"})
        else:
            return Response(serializer.errors)


class SalerLogin(APIView):
    queryset = SalerRegister.objects.all()
    serializer_cl = ForLoginSerializer

    @swagger_auto_schema(request_body=ForLoginSerializer)
    def post(self, request):
        name = request.data.get('name')
        password = request.data.get('password')
        user = SalerRegister.objects.all().filter(name=name, password=password)
        return Response({"Message": "Succes"})


class UpdateSalerPassword(APIView):
    queryset = SalerRegister.objects.all()
    serializer_class = SalerRecoverPassword

    @swagger_auto_schema(request_body=SalerRecoverPassword)
    def patch(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        corfim_password = request.data.get("corfim_password")
        tekshirish_email = SalerRegister.objects.all().filter(email=email)
        if tekshirish_email:
            if password == corfim_password:
                update = SalerRegister.objects.all().filter(email=email).update(password=corfim_password)
                return Response({"msg": "password is changed"})
            else:
                return Response({"msg": "password != password_corfim"})
        else:
            return Response({"msg": "email not found"})


from .serializers import SalerChangePasswordSerializer
class SalerPasswordChange(APIView):
    @swagger_auto_schema(request_body=SalerChangePasswordSerializer)
    def put(self, request):
        name = request.data.get("name")
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")
        confirm_password = request.data.get("confirm_password")
        if new_password == confirm_password:
            topish = SalerRegister.objects.all().filter(name=name, password=old_password).update(password=new_password)
            return Response({"msg": "Password is changed"})
        else:
            return Response({"msg": "new password corfim passwordga teng emas"})
