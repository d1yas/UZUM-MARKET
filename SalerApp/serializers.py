from rest_framework import serializers
from .models import SalerRegister


class ForLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalerRegister
        fields = '__all__'


class ForRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalerRegister
        fields = ('username', 'password')


class SalerRecoverPassword(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=100)
    corfim_password = serializers.CharField(max_length=100)


class SalerChangePasswordSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    old_password = serializers.CharField(max_length=100)
    new_password = serializers.CharField(max_length=100)
    confirm_password = serializers.CharField(max_length=100)
