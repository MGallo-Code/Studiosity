# Generated by Django 4.2.7 on 2023-12-21 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_usermodel_bio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermodel',
            name='bio',
            field=models.TextField(blank=True, max_length=1500, null=True),
        ),
    ]
