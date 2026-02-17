from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class MyUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username","email","first_name","last_name",'profile_pic' )
        widgets = {'profile_pic': forms.FileInput()}

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'info', 'birth_date','profile_pic'] #добавил
        widgets = {'profile_pic':forms.FileInput()}