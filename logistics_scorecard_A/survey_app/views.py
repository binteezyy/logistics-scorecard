from django.shortcuts import render
from django.http import HttpResponse

from .models import *

from django.core.mail import EmailMessage
from django.core.mail import send_mail
import smtplib



# Create your views here.


def index(request, cid):
    scorecard = Scorecard.objects.get(cid=cid)
    categories = scorecard.category_list.all()
    ratings = scorecard.rating.all()
    context = {
        "scorecard": scorecard,
        "categories": categories,
        "ratings": ratings,
    }
    
    if request.method == 'POST':
        for category in categories:
            for question in category.questions.all():
                old_rate = scorecard.rating.get(question__question_string=question.question_string)
                new_rate = Rating.objects.get(question__question_string=question.question_string, rate=request.POST.get('cat-%s-row-%s' % (category.category_number, question.question_number)))
                if old_rate != new_rate:
                    scorecard.rating.remove(old_rate)
                    scorecard.rating.add(new_rate)
        return HttpResponse("OK")
                # old_rate = scorecard.rating.get(question__question_number=2)
                # new_rate = Rating.objects.get(question__question_number=2, rate=request.POST.get('cat-1-row-2'))
                # return HttpResponse('old-%s new-%s' % (old_rate, new_rate))
    else:
        return render(request, "form.html", context)
    

def email_view(request):

    send_mail('test','test','realtantan7@gmail.com', ['Alvin.Panganiban@artesyn.com'])
    return HttpResponse("OK")

