from django.shortcuts import render, redirect
from . models import *
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
import datetime
from django.contrib.auth import logout
# Create your views here.

def get_latest():
    prev = datetime.datetime.today() - datetime.timedelta(30)
    return prev.month

def logoutUser(request):
   logout(request)
   return redirect('login')    

@login_required
def latest_scorecard(request):
    current_user = request.user
    user = Account.objects.get(user=current_user)
    scorecard = user.scorecard.get(month_covered__month=get_latest())


    context = {
        "scorecard": scorecard,
    }

    return render(request, "form.html", context)
