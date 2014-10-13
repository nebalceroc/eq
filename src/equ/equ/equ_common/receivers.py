from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save
from models import UserProfile
from django.core.mail import EmailMultiAlternatives
import os

@receiver(post_save, sender=UserProfile)
def send_welcome_email(sender, instance, created, **kwargs):
	if created and not instance.welcome:
		message_html = open(r'/home/equallo/eq/src/equ/equ/equ_common/static/files/welcome_email.html').read()
		message_html = message_html.replace('{{ username }}',instance.user.email.encode('utf8'))
		message = 'The Equallo team welcomes you to our service. We hope Equallo helps you find what you are looking for.\n\nEnjoy!\n\nRegards,\n\nThe Equallo team'
		email = EmailMultiAlternatives('Welcome to Equallo!', message, settings.DEFAULT_FROM_EMAIL, [instance.user.email])
		email.attach_alternative(message_html, 'text/html')
		email.send(fail_silently=False)
		instance.welcome = True
		instance.save()
