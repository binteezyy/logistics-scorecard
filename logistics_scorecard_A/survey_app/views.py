from django.shortcuts import render
from django.http import HttpResponse
from .models import *
# Create your views here.


def index(request):
    # questions = Question.objects.filter(category="1")
    # credentials = Scorecard.objects.get(cid="butch1")
    # ratings = credentials.rating.all()
    # context = {
    #     "questions": questions,
    #     "credentials": credentials,
    #     "ratings": ratings,
    # }
    # return render(request, "try.html", context)
    # if models.Question.objects.all():
    #     return HttpResponse(questions.question_string[1])
    # else:
    #     return HttpResponse("Not")
    return HttpResponse("OK")
