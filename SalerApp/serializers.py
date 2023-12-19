from rest_framework import serializers
from .models import SalerApp

class ForLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalerApp
        fields = '__all__'