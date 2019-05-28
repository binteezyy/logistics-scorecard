from django.urls import path, include
from . import views


urlpatterns = [
    path('scorecards/<cid>', views.index, name='index'),
    path('email', views.email_view, name='email'),
]
