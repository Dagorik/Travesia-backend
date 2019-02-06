from django.contrib import admin
from teams.users.models import User,Codes
from import_export import resources
from import_export.admin import ImportExportModelAdmin

class UserResource(resources.ModelResource):
    class Meta:
        model = User

@admin.register(User)
class UserAdmin(ImportExportModelAdmin):
    pass

@admin.register(Codes)
class CodesAdmin(admin.ModelAdmin):
    pass
