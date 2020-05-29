from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from django.contrib import admin
from users import views as user_views


urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='login.html', redirect_authenticated_user=True), name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('scorecard/', views.latest_scorecard, name='latest_scorecard'),
    path('try/', views.verify, name='verify'),
]
