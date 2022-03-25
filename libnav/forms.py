from django import forms
from django.contrib.auth.models import User
from django.forms import TextInput, PasswordInput, EmailInput, URLInput, FileInput, Textarea, Select
from libnav.models import User, UserProfile


class UserForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:

        model = User
        fields = ('username', 'email', 'password')
        widgets = {'username': TextInput(attrs={
            'type': 'text',
            'class': 'input',
            'id': 'id_username',
            'placeholder': ' ',
            }),
            'email': EmailInput(attrs={
            'type': 'email',
            'class': 'input',
            'id': 'id_email',
            'placeholder': ' ',
            }),
            'password': PasswordInput(attrs={
            'type': 'password',
            'class': 'input',
            'id': 'id_password',
            'placeholder': ' ',
            })}



class UserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ('picture','website', 'description', 'favouriteFloor',)
        widgets = {
            'picture': FileInput(attrs={
            'type': 'file',
            'class': 'file-input',
            'id': 'id_picture',
            'accept': 'image/*',
            }),
            'website': URLInput(attrs={
            'type': 'url',
            'class': 'input',
            'id': 'id_email',
            'placeholder': ' ',
            }),
            'description': Textarea(attrs={
            'type': 'text',
            'class': 'input',
            'id': 'id_password',
            'placeholder': ' ',
            }),
            'favouriteFloor': Select(attrs={
                'type': 'select',
                'class': 'input',
                'id':'id_floor',
                'placeholder':' ',
            })
            }