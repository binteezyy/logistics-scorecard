from django.shortcuts import render
from django.http import HttpResponse
from .models import *

from django.core.mail import EmailMessage

# Create your views here.


def index(request):
    category = Category.objects.all()
    context = {
        "category": category,
    }

    return render(request, "form.html", context)

def email_view(request):
    email = EmailMessage('Test', 'Test', to=['alvinpanganiban22@gmail.com'])
    email.send()
    return HttpResponse("OK")