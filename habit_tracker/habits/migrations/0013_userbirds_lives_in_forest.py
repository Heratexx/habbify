# Generated by Django 4.2.10 on 2024-02-10 16:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('habits', '0012_userbirds_stage'),
    ]

    operations = [
        migrations.AddField(
            model_name='userbirds',
            name='lives_in_forest',
            field=models.BooleanField(default=False),
        ),
    ]
