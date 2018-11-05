from django.contrib import admin
from teams.teamsapp.models import Teams

# Register your models here.
@admin.register(Teams)
class TeamsAdmin(admin.ModelAdmin):
    pass