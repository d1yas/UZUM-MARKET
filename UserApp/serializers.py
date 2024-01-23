from rest_framework import serializers
from .models import User


class UserSRL(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class Login_Serializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class RecoverPassword(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=100)
    corfim_password = serializers.CharField(max_length=100)


class ChangePasswordSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    old_password = serializers.CharField(max_length=100)
    new_password = serializers.CharField(max_length=100)
    confirm_password = serializers.CharField(max_length=100)
