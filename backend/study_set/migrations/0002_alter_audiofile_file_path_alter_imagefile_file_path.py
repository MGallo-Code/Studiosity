# Generated by Django 4.2.7 on 2023-11-18 02:22

from django.db import migrations, models
import study_set.models


class Migration(migrations.Migration):

    dependencies = [
        ('study_set', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='audiofile',
            name='file_path',
            field=models.FileField(upload_to=study_set.models.get_safe_audio_path),
        ),
        migrations.AlterField(
            model_name='imagefile',
            name='file_path',
            field=models.ImageField(upload_to=study_set.models.get_safe_image_path),
        ),
    ]
