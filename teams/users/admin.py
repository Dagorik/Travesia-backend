from django.contrib import admin
from teams.users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass
