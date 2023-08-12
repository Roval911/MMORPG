from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail

from .models import *


@receiver(post_save, sender=Coment)
def coment_notify(sender, instance, **kwargs):
    author = instance.author.username
    text = instance.text
    post_pk = instance.post.pk
    post_author = instance.post.author

    if instance.accepted:
        mail = instance.post.author.email
        subject = f'Your coment has been approved by {post_author}'
        text_content2 = (
            f'Hello, {author}! \n\n'
            f'Your coment "{text}" is accepted by {post_author}. \n'
            f'Read: http://127.0.0.1:8000/post/{post_pk}'
        )

        send_mail(
            subject=subject,
            message=text_content2,
            from_email='ro-v-al@yandex.ru',
            recipient_list=[mail],
            fail_silently=False
        )
    else:
        mail = instance.post.author.email
        subject = f'A coment from {author} is waiting for your approval'
        text_content = (
            f'A coment to your post!'
            f' Accept or delete: http://127.0.0.1:8000/mycoments/'
        )

        mail1 = instance.author.email
        subject1 = f'You coment "{text}" is sent for approval'
        text_content1 = (
            f'You coment "{text}" is not approved yet. '
            f'We will notify you once it is approved and published'
        )

        send_mail(
            subject=subject,
            message=text_content,
            from_email='ro-v-al@yandex.ru',
            recipient_list=[mail],
            fail_silently=False
        )

        send_mail(
            subject=subject1,
            message=text_content1,
            from_email='ro-v-al@yandex.ru',
            recipient_list=[mail1],
            fail_silently=False
        )


@receiver(post_save, sender=Post)
def post_notify(sender, instance, **kwargs):
    author = instance.author
    title = instance.title
    mail = instance.author.email
    post_pk = instance.pk
    subject = f'Hello {author}! Your post is published'
    text_content = (
        f'Hello, {author}! \n\n'
        f'Your post "{title}" is published or changed. \n'
        f'Read: http://127.0.0.1:8000/post/{post_pk}'
    )

    send_mail(
        subject=subject,
        message=text_content,
        from_email='ro-v-al@yandex.ru',
        recipient_list=[mail],
        fail_silently=False
    )