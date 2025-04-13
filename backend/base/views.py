from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.hashers import make_password
from django.contrib import messages
import logging
from .forms import CreateUser, CustomAuthenticationForm

from .forms import CreateUser
from .models import Recruiter, JobSeeker, JobPost

logger = logging.getLogger(__name__)

from .forms import LoginForm
from django.contrib.auth import login
from django.contrib import messages


from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import LoginForm
from .models import JobSeeker, Recruiter

def custom_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Bienvenue {user.name} 👋")
                return redirect('jobradar:job_list')
            else:
                messages.error(request, "Email ou mot de passe incorrect.")
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


# ------------------------
# LOGOUT
# ------------------------
def custom_logout(request):
    logout(request)
    return redirect('jobradar:login')  # Redirige vers login après déconnexion

# ------------------------
# LISTE DES OFFRES
# ------------------------
def job_list(request):
    jobs = JobPost.objects.all()
    return render(request, 'job_list.html', {'jobs': jobs})

# ------------------------
# DÉTAIL D'UNE OFFRE
# ------------------------
def job_detail(request, job_id):
    job = get_object_or_404(JobPost, id=job_id)
    return render(request, 'job_detail.html', {'job': job})

# ------------------------
# ACCUEIL (TEST)
# ------------------------
class Home(View):
    def get(self, request):
        return render(request, 'hello.html')

# ------------------------
# PAGE DE SUCCÈS APRÈS INSCRIPTION
# ------------------------
class RegisterSuccess(View):
    def get(self, request):
        return render(request, 'register_success.html')

# ------------------------
# INSCRIPTION
# ------------------------
class Signup(View):
    signup_template = 'signup.html'

    def get(self, request):
        form = CreateUser()
        return render(request, self.signup_template, {'form': form})

    def post(self, request):
        form = CreateUser(request.POST, request.FILES)
        if form.is_valid():
            user_data = form.cleaned_data
            user_type = user_data.pop('user_type')
            user_data['password'] = make_password(user_data['password'])
            user_data.pop('confirmed_password')

            try:
                if user_type == 'jobSeeker':
                    user_data.pop('company_name')
                    user_data.pop('position_title')
                    user_data.pop('department')
                    JobSeeker.objects.create(**user_data)
                elif user_type == 'recruiter':
                    Recruiter.objects.create(**user_data)

                return redirect('jobradar:register-success')

            except Exception as e:
                logger.error(f'Error creating user: {str(e)}')
                form.add_error(None, "Erreur lors de la création de l'utilisateur.")

        return render(request, self.signup_template, {'form': form})
