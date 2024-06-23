from django.conf import settings
from django.core.mail import send_mail

# yaha pr hum user ko email send kara ga (k wo account activate kara)


def send_account_activation_email(email, email_token):
    subject = 'Your account needs to be verified'
    email_from = settings.EMAIL_HOST_USER
    message = f'Hi, click on the link to activate your account: http://127.0.0.1:8000/accounts/activate/{email_token}'
    # recipent_list = ["connecthassan76@gmail.com"]
    send_mail(subject, message, email_from, [email], fail_silently=False)