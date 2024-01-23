from rest_framework.serializers import ModelSerializer
from .models import CardHolder


class CardSerializer(ModelSerializer):
    class Meta:
        model = CardHolder
        fields = '__all__'


class DeleteCardSerializer(ModelSerializer):
    class Meta:
        model = CardHolder
        fields = ('number',)


class AddMoneySerializer(ModelSerializer):
    class Meta:
        model = CardHolder
        fields = ('number', 'money')
