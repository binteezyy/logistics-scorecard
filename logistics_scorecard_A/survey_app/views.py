from django.shortcuts import render
from django.http import HttpResponse
from .models import *

# Create your views here.


def index(request):
    questions1 = Category.objects.filter(category_name="Cleanliness")

    context = {
        "questions1": questions1,
    }

    return render(request, "form.html", context)
