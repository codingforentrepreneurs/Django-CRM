from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL  # -> "auth.User"


# user_id => 1
# Create your models here.
class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField()
