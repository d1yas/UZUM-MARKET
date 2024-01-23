from django.db import models

from UserApp.models import User
# Create your models here.


class CardHolder(models.Model):
    name = models.ForeignKey(User,on_delete=models.CASCADE)
    data = models.DateTimeField()
    number = models.IntegerField(default=8600,unique=True)
    money = models.IntegerField(default=0)
