from django.shortcuts import render


from .models import KatalogModel

def filtr_by_katalog(katalog_bot):
    categorylar = KatalogModel.objects.all().filter(katalog=katalog_bot)
    return categorylar


# Create your views here.
