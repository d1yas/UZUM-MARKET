from django.db import models
class User(models.Model):
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    email = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=100)
    phone = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name 

