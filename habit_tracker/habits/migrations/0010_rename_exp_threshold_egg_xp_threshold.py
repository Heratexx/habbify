# Generated by Django 4.2.10 on 2024-02-09 22:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('habits', '0009_egg_exp_threshold'),
    ]

    operations = [
        migrations.RenameField(
            model_name='egg',
            old_name='exp_threshold',
            new_name='xp_threshold',
        ),
    ]
