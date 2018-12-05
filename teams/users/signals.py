from django.db.models.signals import pre_save,post_save
from django.dispatch import receiver
from teams.users.models import User,Codes
from teams.users.tasks import send_mail_activate


@receiver(post_save, sender=User)
def create_code(sender, instance,created,**kwargs):
    if created:
        code = Codes.objects.create(user=instance,type_code="AC")
        send_mail_activate(email=instance.email,code=code.code)




