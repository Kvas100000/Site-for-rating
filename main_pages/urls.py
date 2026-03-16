from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),

    path('content/<slug:slug>/', views.ContentDetailView.as_view(), name='content_detail'),
    path('content/<slug:slug>/rate/', views.AddRatingView.as_view(), name='add_rating'),

    path('movie/add/', views.MovieCreateView.as_view(), name='movie_add'),
    path('game/add/', views.GameCreateView.as_view(), name='game_add'),
    path('series/add/', views.SeriesCreateView.as_view(), name='series_add'),

    path('movie/edit/<slug:slug>/', views.MovieUpdateView.as_view(), name='movie_edit'),
    path('game/edit/<slug:slug>/', views.GameUpdateView.as_view(), name='game_edit'),
    path('series/edit/<slug:slug>/', views.SeriesUpdateView.as_view(), name='series_edit'),

    path('content/<slug:slug>/delete/', views.ContentDeleteView.as_view(), name='content_delete'),

    path('api/score/', views.PollsListAPI.as_view(), name = 'polls-list-api')
    
]