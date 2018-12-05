from teams.users.MailService import SendMail



def send_mail_activate(email,**kwargs):
    mail = SendMail(email=email,**kwargs)
    mail.new_account_activate()