# Generated by Django 3.1 on 2020-08-31 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_remove_person_consumes_alcohol'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='email',
        ),
        migrations.AddField(
            model_name='person',
            name='username',
            field=models.CharField(default=1, max_length=50, unique=True, verbose_name='Nome de usuário'),
            preserve_default=False,
        ),
    ]