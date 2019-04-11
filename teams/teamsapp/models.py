from django.db import models
from io import BytesIO
from django.utils.safestring import mark_safe
from uuid import uuid4
from django.core.files.uploadedfile import InMemoryUploadedFile
import string
import random
import qrcode
import base64


def generate_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))


class Teams(models.Model):
    id = models.UUIDField(editable=False, primary_key=True, default=uuid4)
    name = models.CharField(max_length=150, unique=True)
    mantra = models.TextField(null=True, blank=True)
    leader = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="equipo")
    logo = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    members = models.ManyToManyField(
        "users.User", blank=True, related_name="equipos")
    members_code = models.CharField(max_length=15, default=generate_code)

    def __str__(self):
        return "Team: %s" % self.name

    class Meta:
        ordering = ["created_at"]
        verbose_name = "Equipo"
        verbose_name_plural = "Equipos"


class Checkpoint(models.Model):
    id = models.UUIDField(editable=False, primary_key=True, default=uuid4)
    num_checkpoint = models.IntegerField(default=0)
    lat = models.FloatField(verbose_name="Latitud")
    long = models.FloatField(verbose_name="Longuitud")
    ref = models.CharField(max_length=150, verbose_name="Nombre Checkpoint")
    description = models.TextField(blank=True, null=True)
    kilometer = models.IntegerField(verbose_name="Numero del Kilometro")
    qrcode = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(
        default=True, verbose_name="¿Checkpoint Activo?")
    is_final = models.BooleanField(default=False, verbose_name="¿Es Final?")

    def __str__(self):
        return "%s" % self.ref

        class Meta:
            ordering = ["num_checkpoint"]

    def image_tag(self):
        code = self.qrcode.split('\'')
        return mark_safe('<img src="data:image/png;base64, %s" />' % code[1])

    image_tag.short_description = 'Image'

    def generate_qr_code(self):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=6,
            border=0,
        )
        qr.add_data(self.id)
        qr.make(fit=True)
        img = qr.make_image()

        buffer = BytesIO()
        img.save(buffer)
        filebuffer = base64.b64encode(buffer.getvalue())
        self.qrcode = filebuffer
        self.save()


class Race(models.Model):
    id = models.UUIDField(editable=False, primary_key=True, default=uuid4)
    name = models.CharField(
        max_length=150, verbose_name="Nombre de la Carrera")
    description = models.TextField(
        blank=True, null=True, verbose_name="Descricpion")
    start_hour = models.DateTimeField(
        verbose_name="Hora de Inicio", blank=True, null=True)
    kilometers = models.IntegerField(verbose_name="Distancia Total")
    checkpoints = models.ManyToManyField(Checkpoint, related_name="carrera")
    is_active = models.BooleanField(
        default=True, verbose_name="¿Carrera Activa?")

    def __str__(self):
        return "%s" % self.name

    class Meta:
        verbose_name = "Carrera"
        verbose_name_plural = "Carreras"


class Track(models.Model):
    id = models.UUIDField(editable=False, primary_key=True, default=uuid4)
    team = models.ForeignKey(Teams, on_delete=models.CASCADE)
    checkpoint = models.ForeignKey(Checkpoint, on_delete=models.CASCADE)
    check_time = models.DateTimeField()
    penalization = models.IntegerField(default=0)
    total_time = models.DateTimeField()

    def __str__(self):
        return "Track: %s %s " % (self.team.name, self.checkpoint.ref)

    class Meta:
        ordering = ['-total_time', 'checkpoint__num_checkpoint']
        verbose_name = "Track"
        verbose_name_plural = "Tracks"


class Leaderboard(models.Model):
    id = models.AutoField(primary_key=True)
    team = models.OneToOneField(
        Teams, on_delete=models.SET_NULL, related_name="position", null=True)
    time = models.DateTimeField()

    class Meta:
        ordering = ['time']

    def __str__(self):
        return self.team.name
