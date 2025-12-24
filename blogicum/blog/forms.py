from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Comment, Post


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ('author', 'is_published', 'created_at')
        widgets = {
            'pub_date': forms.DateTimeInput(
                format='%Y-%m-%dT%H:%M',
                attrs={'type': 'datetime-local'},
            )
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')
