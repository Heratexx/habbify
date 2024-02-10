from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_habit, name='create_habit'),
    path('track/<int:habit_id>/', views.track_habit, name='track_habit'),
    path('list/', views.habits_list, name='habits_list'),
    path('eggs/', views.egg_collection, name='egg_collection'),
    path('birds/', views.bird_collection, name='bird_collection'),
]