from django.contrib import admin
from .models import HabitCompletion, Habit, Egg, Bird, UserEggs, UserBirds, Food

# Register your models here.
admin.site.register(HabitCompletion)
admin.site.register(Habit)
admin.site.register(Egg)
admin.site.register(Bird)
admin.site.register(UserEggs)
admin.site.register(UserBirds)
admin.site.register(Food)