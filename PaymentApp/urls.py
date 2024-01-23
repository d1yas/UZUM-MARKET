from django.urls import path

from .views import CardAdd, AddMoneyView, DeleteCardView

urlpatterns = [
    path('cardadd/', CardAdd.as_view()),
    path('addmoney', AddMoneyView.as_view()),
    path('carddelete/<int:number>/', DeleteCardView.as_view())
]
