# Generated by Django 4.2.7 on 2023-12-21 02:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_usermodel_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='usermodel',
            name='bio',
            field=models.TextField(default='', max_length=500),
        ),
    ]
