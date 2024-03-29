# Generated by Django 5.0.2 on 2024-02-08 10:13

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('habits', '0004_remove_habit_is_complete'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='habit',
            name='current_progress',
        ),
        migrations.CreateModel(
            name='Progression',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_logged', models.DateField(default=django.utils.timezone.now)),
                ('amount', models.FloatField()),
                ('habit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='progressions', to='habits.habit')),
            ],
            options={
                'ordering': ['-date_logged'],
            },
        ),
    ]
