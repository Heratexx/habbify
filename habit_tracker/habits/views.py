import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Food, Habit, HabitCompletion, Progression, ExperiencePoint, Level, Egg, Bird, UserBirds, UserEggs
from .forms import HabitForm
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import timedelta, datetime
import random
from django.core import serializers

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
            HabitCompletion.objects.create(
                habit = habit
            )
            xp += award_xp(request.user, "complete habit")
            food = Food.objects.filter(user=request.user)[0]
            food.amount += 1
            food.save()

        hatched_birds = increase_players_egg_progress(request.user, xp)

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
def calc_user_exp(user):
    return ExperiencePoint.objects.filter(user=user).aggregate(Sum('amount'))['amount__sum'] or 0

@login_required
def feed_bird(request, user_bird_id):
    if request.method == "POST":
        food_amount = Food.objects.filter(user=request.user).aggregate(Sum('amount'))['amount__sum'] or 0
        if(food_amount > 0):
            food = Food.objects.filter(user=request.user)[0]
            food.amount -= 1
            food.save()

            bird = UserBirds.objects.get(pk=user_bird_id)
            bird.feed()
            bird.save()
            print(bird.lives_in_forest)
            if(bird.lives_in_forest):
                #generate 3 random eggs to choos from
                user_current_xp = calc_user_exp(request.user)
                eggs = get_random_eggs(user_current_xp)

                serialized_eggs = serializers.serialize('json', eggs)
                print(serialized_eggs)
            else:
                serialized_eggs = None
            
            
            bird_json = {
                "id": bird.id,
                "stage": bird.stage
            }
            food_amount = Food.objects.filter(user=request.user).aggregate(Sum('amount'))['amount__sum'] or 0
            return JsonResponse({
                'bird': bird_json,
                'bird_growed_old': bird.lives_in_forest,
                'eggs': serialized_eggs,
                'food_amount': food_amount,
            })
        else:
            return JsonResponse({'error': 'No Food available.'}, status=500)
    
    return JsonResponse({})
@login_required
def choose_egg(request, egg_id):
    if request.method == "POST":
        UserEggs.objects.create(egg_id = egg_id, user=request.user)
        return JsonResponse({"code": 200})
    
    return JsonResponse({})
def get_random_eggs(user_xp):
    quality_xp_ranges = {
        'common': (0, 200, 5),
        'uncommon': (201, 1000, 3),
        'rare': (1001, 2000, 1),
    }
    # Get all eggs from the database
    suitable_eggs = Egg.objects.filter(xp_required__lte=user_xp)

    
    weighted_eggs = []
    for egg in suitable_eggs:
        quality = None
        for q, xp_range in quality_xp_ranges.items():
            if xp_range[0] <= egg.xp_required <= xp_range[1]:
                quality = q
                break
        if quality:
            print(f"EGG: {egg.name} ({egg.xp_required}) - Q: {quality} - W: {xp_range[2]} - RANGE: {xp_range}")
            weighted_eggs.extend([egg] * xp_range[2])
    # Shuffle the queryset to randomize the order

    selected_eggs = random.choices(weighted_eggs, k=3)
    
    return selected_eggs

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
            'is_completed': habit.is_completed,  # Assuming is_completed is a property/method that evaluates completion
        })

    seven_day_hist = get_seven_day_completion_history(request.user)
    print(seven_day_hist)
    return render(request, 'habits_list.html', {'habits_with_progress': habits_with_progress, 'seven_day_hist': seven_day_hist})

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
    birds = UserBirds.objects.filter(user=request.user, lives_in_forest=False)    
    food_amount = Food.objects.filter(user=request.user).aggregate(Sum('amount'))['amount__sum'] or 0
    return render(request, 'bird_collection.html', {'birds': birds, 'food_amount': food_amount})

@login_required
def forest_collection(request):
    birds = UserBirds.objects.filter(user=request.user, lives_in_forest=True)
    return render(request, 'forest.html', {'birds': birds})

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
    
    adjusted_probability = base_probability + (exp_earned / 250)  
    random_number = random.random()
    
    if random_number < adjusted_probability:
        all_egg_ids = Egg.objects.values_list('id', flat=True)
    
        # Randomly choose one egg ID from the list
        random_egg_id = random.choice(all_egg_ids)
        UserEggs.objects.create(user=user, egg_id=random_egg_id)
        return True
    else:
        return False 
    
@login_required
def clear_user_collections(request):
    # Alle Einträge in UserEggs löschen
    UserEggs.objects.filter(user=request.user).delete()
    
    # Alle Einträge in UserBirds löschen
    UserBirds.objects.filter(user=request.user).delete()

    Habit.objects.filter(user=request.user).delete()

    print("Alle UserEggs und UserBirds wurden erfolgreich gelöscht.")
    return redirect('habits_list')

def get_seven_day_completion_history(user):
    today = datetime.now().date()
    seven_days_ago = today - timedelta(days=7)
    habit_completions = HabitCompletion.objects.filter(
        habit__user=user,
        date_completed__gte=seven_days_ago,
        date_completed__lte=today
    ).values('date_completed').annotate(count=Count('id'))
    print(habit_completions)
    habit_completion_status = {}

    current_date = seven_days_ago
    while current_date <= today:
        habit_completion_status[current_date] = habit_completions.filter(date_completed=current_date).exists()
        current_date += timedelta(days=1)

    return habit_completion_status