from django.db import models


# Create your models here.
class Contact(models.Model):
    email = models.EmailField()
