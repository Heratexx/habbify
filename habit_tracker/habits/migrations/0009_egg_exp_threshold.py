# Generated by Django 4.2.10 on 2024-02-09 22:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('habits', '0008_remove_bird_owner_remove_egg_progress_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='egg',
            name='exp_threshold',
            field=models.IntegerField(default=100),
        ),
    ]