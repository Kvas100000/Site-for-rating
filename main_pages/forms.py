from django import forms
from .models import Movie, Game, Series, Rating

class BootstrapFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['score', 'status', 'review']
        widgets = {
            'score': forms.Select(choices=[(i, i) for i in range(1, 11)], attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'review': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class MovieForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Movie
        exclude = ['average_rating','category', 'slug']
        widgets = {
            'release_date': forms.DateInput(attrs={'type': 'date'}),
        }

class GameForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Game
        exclude = ['average_rating','category', 'slug']
        widgets = {
            'release_date': forms.DateInput(attrs={'type': 'date'}),
        }

class SeriesForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Series
        exclude = ['average_rating','category', 'slug']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }