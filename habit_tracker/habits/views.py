from django.shortcuts import render, redirect, get_object_or_404
from .models import Habit, HabitCompletion, UserProfile
from .forms import HabitForm
from django.contrib.auth.decorators import login_required

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
        habit.increase_progress(amount=1, exp_earned=exp_earned)
        
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
    habits = Habit.objects.filter(user=request.user)  # Assuming you want to filter by the logged-in user
    return render(request, 'habits_list.html', {'habits': habits})
