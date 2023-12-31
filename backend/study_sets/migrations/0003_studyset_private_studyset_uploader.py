# Generated by Django 4.2.7 on 2023-11-24 03:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('study_sets', '0002_alter_studyterm_back_audio_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='studyset',
            name='private',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='studyset',
            name='uploader',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='study_sets', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
