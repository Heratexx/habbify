# Generated by Django 4.2.10 on 2024-02-09 22:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('habits', '0010_rename_exp_threshold_egg_xp_threshold'),
    ]

    operations = [
        migrations.AddField(
            model_name='egg',
            name='image',
            field=models.ImageField(default='', upload_to='egg_images/'),
            preserve_default=False,
        ),
    ]