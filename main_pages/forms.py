from django import forms
from .models import Movie, Game, Series, Rating

class BootstrapFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

class RatingForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['score', 'review']
        widgets = {
            'score': forms.NumberInput(attrs={'min': 1, 'max': 10, 'placeholder': 'Оценка от 1 до 10'}),
            'review': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Напишите, что думаете...'}),
        }

class MovieForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Movie
        exclude = ['average_rating']
        widgets = {
            'release_date': forms.DateInput(attrs={'type': 'date'}),
        }

class GameForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Game
        exclude = ['average_rating']
        widgets = {
            'release_date': forms.DateInput(attrs={'type': 'date'}),
        }

class SeriesForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Series
        exclude = ['average_rating']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }