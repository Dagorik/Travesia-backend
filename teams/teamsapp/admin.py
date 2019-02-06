from django.contrib import admin
from teams.teamsapp.models import Teams
from import_export import resources
from import_export.admin import ImportExportModelAdmin

# Register your models here.
@admin.register(Teams)
class TeamsAdmin(ImportExportModelAdmin):
    pass