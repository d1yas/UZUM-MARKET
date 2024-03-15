from django.db import models


# Create your models here.

class SalerRegister(models.Model):
    username = models.CharField(max_length=18, unique=True)
    password = models.CharField(max_length=16)
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)
    phone = models.IntegerField(unique=True)
    PasportSeria = models.CharField(max_length=2)
    PasportNumber = models.IntegerField(unique=True)


    def __str__(self):
        return self.username
