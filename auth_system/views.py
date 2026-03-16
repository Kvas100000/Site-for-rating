from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import User
from .forms import MyUserCreationForm,UserUpdateForm


class SignUpView(CreateView):
    form_class = MyUserCreationForm
    success_url = reverse_lazy('auth_system:login')
    template_name = 'auth_system/signup.html'

class ProfileUpdateView(LoginRequiredMixin,UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'auth_system/profile_edit.html'
    success_url = reverse_lazy('auth_system:profile_edit')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ratings = self.request.user.user_ratings.select_related('content')
        context['watched'] = ratings.filter(status='WATCHED')
        context['planning'] = ratings.filter(status='PLANNING')
        context['favorites'] = ratings.filter(status='FAVORITE')
        return context

    def get_object(self, queryset=None):
        return self.request.user