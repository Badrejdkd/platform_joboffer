from django.urls import path
from . import views
from .views import custom_login,custom_logout,job_list, job_detail
app_name = 'jobradar'
urlpatterns = [
    path('', job_list, name='job_list'),
    path('job/<int:job_id>/', job_detail, name='job_detail'),
    path('signup/' , views.Signup.as_view() , name='user-signup'),
    path('signup/success/', views.RegisterSuccess.as_view(), name='register-success'),
    path('login/', custom_login, name='login'),
    path('logout/', custom_logout, name='logout'),
]