from django.core.mail import send_mail
from django.conf import settings
import os
from django.conf import settings


class SendMail:

    def __init__(self,email,**kwargs):
        self.email = email
        self.kwargs = kwargs
        self.sender = "info@travesiarover.com.mx"



    def send(self,subject,body,**kwargs):
        print("Enviando Email")
        send_mail(
            subject=subject,
            message=body,
            from_email=self.sender,
            recipient_list=[self.email],
            html_message=kwargs['html']

        )



    def new_account_activate(self):

        subject = "Activa tu cuenta Travesia"
        html_body  = f'<p>Ingresa  el  siguiente codigo para activar tu cuenta <br' \
                     f'<a>{"CODIGO: "+self.kwargs["code"]}</a>'

        self.send(subject=subject,body=html_body,html=html_body)

    def recover_password(self):
        subject = "Recupera tu password"
        html_body = f'<p>Ingresa  a la siguiente ruta para recuperar el password de tu  cuenta <br' \
                    f'<a>{self.url+"users/recover/check/"+self.kwargs["code"]+"/"}</a>'

        self.send(subject=subject, body=html_body, html=html_body)



