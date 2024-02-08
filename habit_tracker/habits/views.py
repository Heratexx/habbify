from django.shortcuts import render, redirect, get_object_or_404
from .models import Habit, HabitCompletion, UserProfile, Progression
from .forms import HabitForm
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta

@login_required
def create_habit(request):
    if request.method == 'POST':
        form = HabitForm(request.POST)
        if form.is_valid():
            habit = form.save(commit=False)
            habit.user = request.user
            habit.save()
            return redirect('habits_list')
    else:
        form = HabitForm()
    return render(request, 'create_habit.html', {'form': form})

@login_required
def track_habit(request, habit_id):
    """View to track progress of a habit and handle completion."""
    habit = get_object_or_404(Habit, id=habit_id, user=request.user)
    if request.method == 'POST':
        # Define or calculate EXP earned for this habit
        exp_earned = 10  # Example fixed value, adjust as needed
        
        # Increase progress and potentially mark as complete
        Progression.objects.create(habit=habit, amount=1)
        
        # Redirect to a success page or the habit list
        return redirect('habits_list')  # Adjust redirection as needed
    else:
        # GET request handling or error message
        return redirect('habit_detail', habit_id=habit.id)  # Adjust as needed

def calculate_exp(user_profile, habit):
    # Implementation to calculate EXP based on habit completion
    pass

def level_up(user_profile):
    # Implementation to increase level based on EXP
    pass

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