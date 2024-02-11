from django.urls import path
from . import views

urlpatterns = [
    path('/', views.habits_list, name='habits_list'),
    path('create/', views.create_habit, name='create_habit'),
    path('track/<int:habit_id>/', views.track_habit, name='track_habit'),
    path('list/', views.habits_list, name='habits_list'),
    path('eggs/', views.egg_collection, name='egg_collection'),
    path('eggs/<int:egg_id>/choose/', views.choose_egg, name='choose_egg'),
    path('birds/', views.bird_collection, name='bird_collection'),
    path('birds/<int:user_bird_id>/feed/', views.feed_bird, name='feed_bird'),
    path('forest/', views.forest_collection, name='forest_collection'),
    path('clear/', views.clear_user_collections, name='clear_user_data'),
]