from django.db import models
from uuid import uuid4
import string
import random


def generate_code(): 
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))


class Teams(models.Model):
    id = models.UUIDField(editable=False,primary_key=True,default=uuid4)
    name =  models.CharField(max_length=150,unique=True)
    mantra =  models.TextField(null=True,blank=True)
    leader =  models.ForeignKey("users.User",on_delete=models.CASCADE,related_name="equipo")
    logo =  models.URLField(blank=True, null=True)
    created_at =  models.DateTimeField(auto_now_add=True)
    is_active =  models.BooleanField(default=True)
    members =  models.ManyToManyField("users.User",blank=True)
    members_code = models.CharField(max_length=15,default=generate_code)

    class Meta:
        ordering = ["created_at"] 
        verbose_name = "Equipo"
        verbose_name_plural = "Equipos"

