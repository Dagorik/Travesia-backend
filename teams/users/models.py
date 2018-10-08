from django.db import models
from django.contrib.auth.models import AbstractUser
from uuid import uuid4

class User(AbstractUser):
    id = models.UUIDField(editable=False,primary_key=True,default=uuid4)
    birth_date =  models.DateField()
    gender = models.CharField(max_length=10,choices=(('H',"Hombre"),('M',"Mujer")))
    phone = models.CharField(max_length=12)
    is_leader =  models.BooleanField(default=False)
    profile_pic = models.URLField()


