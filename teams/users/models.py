from django.db import models
from django.contrib.auth.models import AbstractUser
from uuid import uuid4
import hashlib
import random
import datetime
import string

class User(AbstractUser):
    id = models.UUIDField(editable=False,primary_key=True,default=uuid4)
    birth_date =  models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=10,choices=(('H',"Hombre"),('M',"Mujer")),null=True)
    phone = models.CharField(max_length=12,null=True)
    is_leader =  models.BooleanField(default=False)
    profile_pic = models.URLField(blank=True, null=True)
    name_group_scout = models.CharField(max_length=250,blank=True, null=True)
    clan_name =  models.CharField(max_length=250,blank=True, null=True)
    province =  models.CharField(max_length=250,blank=True, null=True)
    state =  models.CharField(max_length=250,blank=True, null=True)
    blod_type =  models.CharField(max_length=150,blank=True, null=True)
    allergies = models.CharField(max_length=250,blank=True, null=True)
    ailment = models.TextField(blank=True, null=True)
    special_medicine =  models.TextField(blank=True, null=True)
    emergency_contact_name =  models.CharField(max_length=150,blank=True, null=True)
    emergency_contact_phone =  models.CharField(max_length=150,blank=True, null=True)
    baucher =  models.URLField(blank=True, null=True)

def generate_codes():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))


def add_one_day():
    return datetime.datetime.now() + datetime.timedelta(hours=24)


class Codes(models.Model):

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    code = models.CharField(max_length=250,default=generate_codes)
    starts_at = models.DateTimeField(auto_now_add=True)
    ends_at = models.DateTimeField(default=add_one_day)
    type_code = models.CharField(choices=(('AC',"Activate"),('RC',"Recover")),max_length=50)
    is_used = models.BooleanField(default=False)


    class Meta:
        verbose_name = 'Codigo de validacion'
        verbose_name_plural = 'Codigos de validación'

    def __str__(self):
        type_code = "Activacion" if self.type_code else "Recuperacion"
        return f'Codigo de {type_code} del usuario {self.user.email}'



