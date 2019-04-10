from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from teams.users.models import User, Codes
from import_export import resources
from import_export.admin import ImportExportModelAdmin


class UserResource(resources.ModelResource):
    class Meta:
        model = User


@admin.register(User)
class UserAdmin(BaseUserAdmin,ImportExportModelAdmin):
	
	add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )

@admin.register(Codes)
class CodesAdmin(admin.ModelAdmin):
    pass
