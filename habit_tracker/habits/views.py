from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Habit, HabitCompletion, Progression, ExperiencePoint, Level, Egg, Bird, UserBirds, UserEggs
from .forms import HabitForm
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta
import random

@login_required
def create_habit(request):
    if request.method == 'POST':
        form = HabitForm(request.POST)
        if form.is_valid():
            habit = form.save(commit=False)
            habit.user = request.user
            habit.save()
            award_xp(request.user, "create habit")
            return redirect('habits_list')
        
    else:
        form = HabitForm()
    return render(request, 'create_habit.html', {'form': form})

@login_required
def track_habit(request, habit_id):
    """View to track progress of a habit and handle completion, updated for AJAX."""
    if request.method == 'POST':
        habit = get_object_or_404(Habit, id=habit_id, user=request.user)
        xp = 0
        got_new_egg = False
        # Increase progress and potentially mark as complete
        Progression.objects.create(habit=habit, amount=1)
        xp += award_xp(request.user, "progress habit")
        
        # Calculate the new total progress for the habit
        total_progress = Progression.objects.filter(habit=habit).aggregate(Sum('amount'))['amount__sum'] or 0
        progress_percentage = (total_progress / habit.target) * 100
        is_completed = habit.is_completed
        if(habit.is_completed):
            xp += award_xp(request.user, "complete habit")

        hatched_birds = increase_players_egg_progress(request.user, xp)
        
        if(habit.is_completed):
            got_new_egg = get_new_egg(request.user, xp)
        # Instead of redirecting, return a JSON response with the updated progress info
        return JsonResponse({
            'progress_percentage': progress_percentage,
            'is_completed': is_completed,
            'xp_gain': xp,
            'got_new_egg': got_new_egg,
            'num_hatched_birds': len(hatched_birds)
        })

    # If the request method isn't POST, you can decide how to handle it. 
    # For simplicity, this example just returns an empty JSON response or you could return an error message.
    return JsonResponse({})

@login_required
def habits_list(request):
    habits_with_progress = []
    today = timezone.now().date()
    
    habits = Habit.objects.filter(user=request.user)  # Assuming you want to filter by the logged-in user

    for habit in habits:
        # Determine the start date for calculating progress
        start_date = get_start_date_for_habit(habit.frequency, today)

        # Aggregate the total progress for the habit since the start date
        total_progress = habit.progressions.filter(date_logged__gte=start_date).aggregate(Sum('amount'))['amount__sum'] or 0
        progress_percentage = (total_progress / habit.target * 100) if  habit.target > 0 else 0
        # Append the habit and its calculated current progress to the list
        habits_with_progress.append({
            'habit': habit,
            'current_progress': total_progress,
            'progress_percentage': min(progress_percentage, 100),  # Ensure it does not exceed 100%
            'is_completed': habit.is_completed  # Assuming is_completed is a property/method that evaluates completion
        })

    return render(request, 'habits_list.html', {'habits_with_progress': habits_with_progress})

@login_required
def profile(request):
    user = request.user

    # Calculate user's total XP
    total_xp = ExperiencePoint.objects.filter(user=user).aggregate(Sum('amount'))['amount__sum'] or 0

    # Calculate user's level
    user_level = calculate_user_level(total_xp)

    context = {
        'user_level': user_level,
        'total_xp': total_xp
    }
    return render(request, 'base.html', context)

def calculate_user_level(total_xp):
    levels = Level.objects.all().order_by('level_number')
    user_level = 1
    for level in levels:
        if total_xp >= level.xp_threshold:
            user_level = level.level_number
        else:
            break
    return user_level

def get_start_date_for_habit(frequency, today):
    if frequency == 'DAILY':
        return today
    elif frequency == 'WEEKLY':
        return today - timedelta(days=today.weekday())  # Week starts on Monday
    elif frequency == 'MONTHLY':
        return today.replace(day=1)
    elif frequency == 'YEARLY':
        return today.replace(month=1, day=1)
    return today  # Default fallback

def award_xp(user, action_type):
    xp_amounts = {
        'create habit': 20,
        'progress habit': 20,
        'complete habit': 100,
    }

    amount = xp_amounts.get(action_type, 0) 
    if amount > 0:
        ExperiencePoint.objects.create(user=user, amount=amount, action_type=action_type)
    
    return amount

@login_required
def egg_collection(request):
    eggs = UserEggs.objects.filter(user=request.user)
    return render(request, 'egg_collection.html', {'eggs': eggs})

@login_required
def bird_collection(request):
    birds = UserBirds.objects.filter(user=request.user)
    return render(request, 'bird_collection.html', {'birds': birds})

def increase_players_egg_progress(user, xp):
    eggs = UserEggs.objects.filter(user = user)
    hatched_birds = set()
    for egg in eggs:
        egg.progress += xp
        egg.save()
        bird = hatch(user, egg)
        if bird:
            hatched_birds.add(bird)
    
    return hatched_birds



def hatch(user, egg):
    if egg.progress >= egg.egg.xp_threshold:
        available_birds = Bird.objects.filter(egg=egg.egg)
        if available_birds.exists():
            chosen_bird = random.choice(available_birds)
            user_bird = UserBirds.objects.create(bird=chosen_bird, user=user)
            UserEggs.objects.get(pk=egg.id).delete()
            return user_bird
        else:
            return None
    else:
        return None

def get_new_egg(user, exp_earned):
    base_probability = 0.2
    
    adjusted_probability = base_probability + (exp_earned / 10)  
    
    random_number = random.random()
    
    if random_number < adjusted_probability:
        all_egg_ids = Egg.objects.values_list('id', flat=True)
    
        # Randomly choose one egg ID from the list
        random_egg_id = random.choice(all_egg_ids)
        UserEggs.objects.create(user=user, egg_id=random_egg_id)
        return True
    else:
        return False 