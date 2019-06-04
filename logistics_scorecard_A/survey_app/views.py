from django.shortcuts import render
from django.http import HttpResponse
from . models import *
from django.core.mail import EmailMessage
from django.core.mail import send_mail
import smtplib



# Create your views here.


def index(request, cid):
    scorecard = Scorecard.objects.get(cid=cid)
    context = {
        "scorecard": scorecard,
    }

    return render(request, "form.html", context)

def email_view(request):
    send_mail('subject','alvin carloser','realtantan7@gmail.com', ['Alvin.Panganiban@artesyn.com'])
    return HttpResponse("OK")
