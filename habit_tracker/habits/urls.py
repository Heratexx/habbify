from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_habit, name='create_habit'),
    path('track/<int:habit_id>/', views.track_habit, name='track_habit'),
    path('list/', views.habits_list, name='habits_list'),
    # Add more URLs as needed
]