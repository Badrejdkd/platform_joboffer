from email.policy import default

from django import forms
from django.core.exceptions import ValidationError

from . import models
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model

User = get_user_model()
from django import forms
from django.contrib.auth import authenticate

from django import forms

class LoginForm(forms.Form):
    email = forms.EmailField(label="Adresse email", max_length=191, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput(attrs={'class': 'form-control'}))


    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if email and password:
            user = authenticate(email=email, password=password)
            if not user:
                raise forms.ValidationError("Email ou mot de passe invalide.")
            cleaned_data['user'] = user  # Pour le récupérer plus tard dans la vue
        return cleaned_data

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'autofocus': True, 'class': 'form-control'})
    )

    def confirm_login_allowed(self, user):
        # Tu peux ajouter des vérifications personnalisées ici
        return super().confirm_login_allowed(user)




class CreateUser(forms.ModelForm):
    USER_TYPES = [
        ('jobSeeker', 'Job Seeker'),
        ('recruiter', 'Recruiter')
    ]

    confirmed_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm your password'
        })
    )

    user_type = forms.ChoiceField(
        choices=USER_TYPES,
        initial='jobSeeker',
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'userType'
        })
    )
    company_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control recruiter-field',
            'placeholder': 'Enter company name'
        })
    )

    position_title = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control recruiter-field',
            'placeholder': 'Enter position title '
        })
    )

    department = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control recruiter-field',
            'placeholder': 'Enter department name'
        })
    )


    class Meta:
        model = models.JobSeeker
        fields = ['name', 'email' , 'phone_number','profession' ,'password','confirmed_password' ,  'profile_picture']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your full name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your email'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your phone number'
            }),

            'profession': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your profession'
            }),

            'password': forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your password'
            }),
            'profile_picture': forms.FileInput(attrs={
                'class': 'form-control'
            })
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirmed_password = cleaned_data.get('confirmed_password')

        if password and confirmed_password:
            if password != confirmed_password:
                raise ValidationError("Passwords do not match")

        return cleaned_data