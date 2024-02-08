from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Habit(models.Model):
    HABIT_FREQUENCY_CHOICES = [
        ('DAILY', 'Everyday'),
        ('WEEKLY', 'Weekly'),
        ('MONTHLY', 'Monthly'),
        ('YEARLY', 'Yearly'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    frequency = models.CharField(max_length=7, choices=HABIT_FREQUENCY_CHOICES)
    target = models.IntegerField(help_text="How many times per period?")
    current_progress = models.FloatField(default=0)  # Current progress towards the target
    is_complete = models.BooleanField(default=False)  # Whether the habit is completed

    def increase_progress(self, amount=1, exp_earned=0):
        """Increase the habit's progress, check for completion, and record completion."""
        self.current_progress += amount
        if self.current_progress >= self.target and not self.is_complete:
            self.is_complete = True
            # Record the completion
            completion = HabitCompletion(habit=self, date_completed=timezone.now().date(), exp_earned=exp_earned)
            completion.save()
        self.save()

    def __str__(self):
        return self.name

class HabitCompletion(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE)
    date_completed = models.DateField()
    exp_earned = models.IntegerField(default=0)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    exp = models.IntegerField(default=0)
    level = models.IntegerField(default=1)
