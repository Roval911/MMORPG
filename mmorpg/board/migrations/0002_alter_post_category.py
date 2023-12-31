# Generated by Django 4.2.4 on 2023-08-12 16:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='category',
            field=models.CharField(choices=[('SPELL_MASTERS', 'Мастера заклинаний'), ('DD', 'ДД'), ('QUEST_GIVERS', 'Квестгиверы'), ('TANKS', 'Танки'), ('GUILD_MATERS', 'Гилдмастеры'), ('VENDORS', 'Торговцы'), ('POTION_MASTERS', 'Зельевары'), ('BLACKSMITHS', 'Кузнецы'), ('HEALERS', 'Хилы'), ('SKINNERS', 'Кожевники')], default='Tanks', max_length=28, verbose_name='category'),
        ),
    ]
