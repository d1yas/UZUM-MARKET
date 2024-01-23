from django.shortcuts import render
from django.shortcuts import render
from rest_framework import status

from rest_framework.views import APIView
from rest_framework.response import Response
# Create your views here.
from .serializer import CardSerializer, AddMoneySerializer, DeleteCardSerializer
from .models import CardHolder
from drf_yasg.utils import swagger_auto_schema


class CardAdd(APIView):
    queryset = CardHolder.objects.all()
    serializer_class = CardSerializer

    @swagger_auto_schema(request_body=CardSerializer)
    def post(self, request):
        serializer = CardSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"MSG": "Card Created"})
        else:
            return Response(serializer.errors)


##
class AddMoneyView(APIView):
    @swagger_auto_schema(request_body=AddMoneySerializer)
    def post(self, request):
        number = request.data.get("number")
        money = request.data.get("money")
        filtr_c = CardHolder.objects.all().filter(number=number)
        for i in filtr_c:
            user_puli = i.money
        hamma_pul = user_puli + money
        updater = CardUser.objects.all().filter(number=number).update(money=hamma_pul)
        return Response({"message": "ok"})


class DeleteCardView(APIView):
    serializer_class = DeleteCardSerializer

    def delete(self, request, number):
        f = CardHolder.objects.all().filter(number=number)
        if f:
            CardHolder.objects.all().filter(number=number).delete()
            return Response({'message': 'card deleted'})
        else:
            return Response({"msg": "card not found"})
