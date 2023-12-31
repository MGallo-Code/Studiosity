# Generated by Django 4.2.7 on 2024-01-02 22:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('study_sets', '0006_alter_studyterm_back_voice_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='studyterm',
            name='sort_order',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterUniqueTogether(
            name='studyterm',
            unique_together={('study_set', 'sort_order')},
        ),
    ]
