from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.db.models import Avg
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from pytils.translit import slugify
from .models import Content, Movie, Game, Series, Rating
from .forms import RatingForm, MovieForm, GameForm, SeriesForm
from rest_framework import generics
from .serializers import ScoreSerializer

class PollsListAPI(generics.ListCreateAPIView ):
    queryset = Rating.objects.all()
    serializer_class = ScoreSerializer

class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff


class HomeView(ListView):
    model = Content
    template_name = 'main_pages/index.html'
    context_object_name = 'items'
    paginate_by = 9

    def get_queryset(self):
        queryset = Content.objects.all().order_by('-id')
        ctype = self.request.GET.get('type')

        if ctype == 'movies':
            return Movie.objects.all().order_by('-id')
        elif ctype == 'games':
            return Game.objects.all().order_by('-id')
        elif ctype == 'series':
            return Series.objects.all().order_by('-id')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_type'] = self.request.GET.get('type', 'all')
        return context

class ContentDetailView(DetailView):
    model = Content
    template_name = 'main_pages/detail.html'
    context_object_name = 'item'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reviews'] = self.object.ratings.exclude(review="").order_by('-created_at')

        if self.request.user.is_authenticated:
            user_rating = Rating.objects.filter(
                user=self.request.user, content=self.object
            ).first()
            context['user_rating'] = user_rating
            if user_rating:
                context['rating_form'] = RatingForm(instance=user_rating)
            else:
                context['rating_form'] = RatingForm()
        else:
            context['rating_form'] = RatingForm()
        return context


class AddRatingView(LoginRequiredMixin, View):
    def post(self, request, slug):
        content_obj = get_object_or_404(Content, slug=slug)
        status = request.POST.get('status')
        score = request.POST.get('score')
        review = request.POST.get('review', '').strip()
        rating, created = Rating.objects.get_or_create(
            user=request.user,
            content=content_obj
        )
        rating.status = status
        if status == 'PLANNING':
            rating.score = None
            rating.review = ""
        else:
            if score and score.isdigit():
                rating.score = int(score)
            rating.review = review
        rating.save()
        return redirect('main:content_detail', slug=slug)

    def get_success_url(self):
        return reverse('main:content_detail', kwargs={'slug': self.kwargs['slug']})

class MovieCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Movie
    form_class = MovieForm
    template_name = 'main_pages/manage_content.html'
    success_url = reverse_lazy('main:home')

    def form_valid(self, form):
        form.instance.category = 'MOVIE'

        if not form.instance.slug:
            form.instance.slug = slugify(form.instance.title)
        return super().form_valid(form)

class GameCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Game
    form_class = GameForm
    template_name = 'main_pages/manage_content.html'
    success_url = reverse_lazy('main:home')

    def form_valid(self, form):
        form.instance.category = 'GAME'
        if not form.instance.slug:
            form.instance.slug = slugify(form.instance.title)
        return super().form_valid(form)

class SeriesCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Series
    form_class = SeriesForm
    template_name = 'main_pages/manage_content.html'
    success_url = reverse_lazy('main:home')

    def form_valid(self, form):
        form.instance.category = 'SERIES'
        if not form.instance.slug:
            form.instance.slug = slugify(form.instance.title)
        return super().form_valid(form)

class MovieUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = Movie
    form_class = MovieForm
    template_name = 'main_pages/manage_content.html'

    def get_success_url(self):
        return reverse('main:content_detail', kwargs={'slug': self.object.slug})

class GameUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = Game
    form_class = GameForm
    template_name = 'main_pages/manage_content.html'

    def get_success_url(self):
        return reverse('main:content_detail', kwargs={'slug': self.object.slug})

class SeriesUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = Series
    form_class = SeriesForm
    template_name = 'main_pages/manage_content.html'

    def get_success_url(self):
        return reverse('main:content_detail', kwargs={'slug': self.object.slug})

class ContentDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Content
    template_name = 'main_pages/confirm_delete.html'
    success_url = reverse_lazy('main:home')