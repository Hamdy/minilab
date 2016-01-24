from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.mail import send_mail
from account.signals import actvation_token_reset

@receiver(post_save, sender=get_user_model())
def send_activation_email(sender,instance, signal, created, **kwargs):
    if created and not instance.is_active:
        #send activation email
        send_mail('Test', 
            instance.activation_token,
            'sender@test.com',
            ['receiver@test.com'],
            fail_silently=True)
    else:
        # send welcome mail
        pass


@receiver(actvation_token_reset, sender=get_user_model())
def resend_act_email(sender,token, **kwargs ):
    send_mail('Test', 
            token,
            'sender@test.com',
            ['receiver@test.com'],
            fail_silently=True)