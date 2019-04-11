from django.contrib import admin
from teams.teamsapp.models import Teams, Race, Checkpoint, Track, Leaderboard
from import_export import resources
from import_export.admin import ImportExportModelAdmin

# Register your models here.
@admin.register(Teams)
class TeamsAdmin(ImportExportModelAdmin):
    pass


@admin.register(Race)
class RaceAdmin(admin.ModelAdmin):
    pass


@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    pass


@admin.register(Checkpoint)
class Checkpoint(ImportExportModelAdmin):
    fields = ('id', 'num_checkpoint', 'lat', 'long', 'ref',
              'description', 'kilometer', 'is_active', 'is_final', 'image_tag')
    readonly_fields = ('image_tag','id')


def save_model(self, request, obj, form, change):
    obj.generate_qr_code()
    super().save_model(request, obj, form, change)


@admin.register(Leaderboard)
class LeaderboardAdmin(ImportExportModelAdmin):
    pass
