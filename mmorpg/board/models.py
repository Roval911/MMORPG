from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import pgettext_lazy


class Post(models.Model):
    CATEGORY = {('TANKS', 'Танки'),
                ('HEALERS', 'Хилы'),
                ('DD', 'ДД'),
                ('VENDORS', 'Торговцы'),
                ('GUILD_MATERS', 'Гилдмастеры'),
                ('QUEST_GIVERS', 'Квестгиверы'),
                ('BLACKSMITHS', 'Кузнецы'),
                ('SKINNERS', 'Кожевники'),
                ('POTION_MASTERS', 'Зельевары'),
                ('SPELL_MASTERS', 'Мастера заклинаний')}

    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='author')
    category = models.CharField(max_length=28, choices=CATEGORY, default='Tanks', verbose_name='category')
    dateCreation = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=128, verbose_name=pgettext_lazy('post title', 'title'))
    text = models.TextField(default='Введите текст объявления')

    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        return f'{self.pk}'

class Coment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    dateCreation = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)

    def get_absolute_url(self):
        return f'{self.pk}'