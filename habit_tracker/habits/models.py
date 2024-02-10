from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
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

    @property
    def is_completed(self):
        today = timezone.now().date()
        if self.frequency == 'DAILY':
            start_date = today
        elif self.frequency == 'WEEKLY':
            start_date = today - timedelta(days=today.weekday())  # Assuming week starts on Monday
        elif self.frequency == 'MONTHLY':
            start_date = today.replace(day=1)
        elif self.frequency == 'YEARLY':
            start_date = today.replace(month=1, day=1)
        else:
            return False

        total_progress = self.progressions.filter(date_logged__gte=start_date).aggregate(total=models.Sum('amount'))['total'] or 0
        
        return total_progress >= self.target
    
    def __str__(self):
        return self.name

class Progression(models.Model):
    habit = models.ForeignKey(Habit, related_name='progressions', on_delete=models.CASCADE)
    date_logged = models.DateField(default=timezone.now)
    amount = models.FloatField()

    class Meta:
        ordering = ['-date_logged']

class HabitCompletion(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE)
    date_completed = models.DateField()
    exp_earned = models.IntegerField(default=0)

class ExperiencePoint(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.IntegerField()
    action_type = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)

class Level(models.Model):
    level_number = models.IntegerField(unique=True)
    xp_threshold = models.IntegerField()
    
class Egg(models.Model):
    name = models.CharField(max_length=100)
    xp_required = models.IntegerField(default=100)  # XP required to hatch the egg
    xp_threshold = models.IntegerField(default=100)
    image = models.ImageField(upload_to='egg_images/')
class Bird(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='bird_images/')
    egg = models.ForeignKey(Egg, on_delete=models.CASCADE)

class UserEggs(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    egg = models.ForeignKey(Egg, on_delete=models.CASCADE)
    progress = models.IntegerField(default=0)

class UserBirds(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bird = models.ForeignKey(Bird, on_delete=models.CASCADE)
    stage = models.IntegerField(default=1)
    lives_in_forest = models.BooleanField(default=False)

    def feed(self):
        self.stage += 1
        #NOTE: Currently hard codeded stage 3 as final Stage
        if(self.stage == 3):
            self.lives_in_forest = True
        self.save()
