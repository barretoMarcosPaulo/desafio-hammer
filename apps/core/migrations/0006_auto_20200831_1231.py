# Generated by Django 3.1 on 2020-08-31 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20200831_1158'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hammerbarbecue',
            name='date',
            field=models.DateField(verbose_name='Data do churrasco'),
        ),
        migrations.AlterField(
            model_name='person',
            name='username',
            field=models.CharField(max_length=50, unique=True, verbose_name='Nome de usuário'),
        ),
    ]
