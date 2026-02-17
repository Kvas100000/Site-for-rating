from django.contrib import admin
from .models import Genre, Content, Movie, Game, Series, Rating, Screenshot

class ScreenshotInline(admin.TabularInline):
    model = Screenshot
    extra = 3

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['title', 'release_year', 'director', 'category']
    filter_horizontal = ['genres']
    inlines = [ScreenshotInline]
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ['title', 'director']

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ['title', 'release_year', 'developer', 'category']
    filter_horizontal = ['genres']
    inlines = [ScreenshotInline]
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ['title', 'developer']

@admin.register(Series)
class SeriesAdmin(admin.ModelAdmin):
    list_display = ['title', 'release_year', 'status', 'seasons_count']
    filter_horizontal = ['genres']
    inlines = [ScreenshotInline]
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ['status']

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ['user', 'content', 'score']
    list_filter = ['score']