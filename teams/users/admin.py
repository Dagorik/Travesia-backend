from django.contrib import admin
from teams.users.models import User,Codes


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass

@admin.register(Codes)
class CodesAdmin(admin.ModelAdmin):
    pass
