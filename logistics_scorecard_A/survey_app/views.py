from django.shortcuts import render
from django.http import HttpResponse
from .models import *

# Create your views here.


def index(request):
    category = Category.objects.all()
    context = {
        "category": category,
    }

    return render(request, "form.html", context)
