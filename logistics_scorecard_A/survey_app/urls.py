from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from users import views as user_views

urlpatterns = [
    path('home', views.landing, name='landing'),
    path('scorecards/<cid>', views.index, name='scorecard'),
    path('email', views.email_view, name='email'),
    path('scorecards/<cid>/view', views.view_scorecard, name='view_scorecard'),
    path('create', views.create_template, name='create_template'),
    path('settings', views.date_settings_view, name='date_settings'),
    path('trigger_settings', views.trigger_update, name='update_trigger'),
]
