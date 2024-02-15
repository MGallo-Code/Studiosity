# Generated by Django 4.2.7 on 2024-01-20 21:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('study_sets', '0008_alter_studyterm_sort_order'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='studyterm',
            unique_together=set(),
        ),
        migrations.AlterField(
            model_name='studyterm',
            name='study_set',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='terms', to='study_sets.studyset'),
        ),
    ]