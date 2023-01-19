from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

from users.models import CustomUser


@receiver(post_save,sender=CustomUser)
def send_velcome_email(sender,instance,created,**kwargs):
    if created:
        send_mail(
            "Welocome to Goodreads Clone",
            f"Hi, {instance.username}.Welcome to Goodreads Clone.Enjoy the books and reviews.",
            "khusniddindatascientistn1@gmail.com",
            [instance.email]
        )
