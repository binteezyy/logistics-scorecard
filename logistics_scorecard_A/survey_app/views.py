from django.shortcuts import render
from django.http import HttpResponse
<<<<<<< HEAD
from .models import *
=======
from . models import *
from O365 import Message
>>>>>>> superdry
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
<<<<<<< HEAD
    send_mail('test','test','realtantan7@gmail.com', ['Alvin.Panganiban@artesyn.com'])
=======
    send_mail('subject','alvin carloser','realtantan7@gmail.com', ['Alvin.Panganiban@artesyn.com'])
>>>>>>> superdry
    return HttpResponse("OK")