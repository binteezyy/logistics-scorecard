from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from users import views as user_views

urlpatterns = [
    path('scorecards/<cid>', views.index, name='index'),
    path('email', views.email_view, name='email'),
]
