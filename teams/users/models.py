from django.db import models
from django.contrib.auth.models import AbstractUser
from uuid import uuid4

class User(AbstractUser):
    id = models.UUIDField(editable=False,primary_key=True,default=uuid4)
    birth_date =  models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=10,choices=(('H',"Hombre"),('M',"Mujer")),null=True)
    phone = models.CharField(max_length=12,null=True)
    is_leader =  models.BooleanField(default=False)
    profile_pic = models.URLField()
    name_group_scout = model.CharField(max_length=250,blank=True, null=True)
    clan_name =  model.CharField(max_length=250,blank=True, null=True)
    province =  model.CharField(max_lengt=250,blank=True, null=True)
    state =  model.CharField(max_length=250,blank=True, null=True)
    blod_type =  models.CharField(max_length=150,blank=True, null=True)
    allergies = models.CharField(max_length=250,blank=True, null=True)
    ailment = models.TextField(blank=True, null=True)
    special_medicine =  models.TextField(blank=True, null=True)
    emergency_contact_name =  models.CharField(max_length=150,blank=True, null=True)
    emergency_contact_phone =  model.CharField(max_length=150,blank=True, null=True)



