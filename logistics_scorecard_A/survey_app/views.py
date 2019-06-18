from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *

from django.core.mail import EmailMessage
from django.core.mail import send_mail
import smtplib
from django.core.exceptions import ObjectDoesNotExist

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.contrib.auth.decorators import login_required
from users.models import *

# Create your views here.

@login_required
def landing(request):
    current_user = request.user
    user = Account.objects.get(user=current_user)
    context = {
         'user':user,
         'day':datetime.datetime.now().day,
     }

    return render(request, 'landing.html', context)

def view_scorecard(request,cid):
    scorecard = Scorecard.objects.get(cid=cid)
    categories = scorecard.category_list.all()
    ratings = scorecard.rating.all()
    context = {
        "scorecard": scorecard,
        "categories": categories,
        "ratings": ratings,
    }
    return render(request, 'form.html', context)


@login_required
def index(request, cid):
    current_user = request.user
    scorecard = Scorecard.objects.get(cid=cid)
    user1 = scorecard.account_set.first()
    if str(user1) != str(current_user):
        return redirect('landing')
    if datetime.datetime.now().day > 15:
       return redirect('view_scorecard', cid)
    categories = scorecard.category_list.all()
    ratings = scorecard.rating.all()
    context = {
        "scorecard": scorecard,
        "categories": categories,
        "ratings": ratings,
        'date_now': datetime.datetime.now(),
    }

    if request.method == 'POST':
        for category in categories:
            for question in category.questions.all():
                try:
                    new_rate = Rating.objects.get(question__question_string=question.question_string, rate=request.POST.get(
                    'cat-%s-row-%s' % (category.category_number, question.question_number)))
                except Rating.DoesNotExist:
                    add_rate = Rating(question=question, rate=request.POST.get(
                    'cat-%s-row-%s' % (category.category_number, question.question_number)))
                    add_rate.save()
                    new_rate = Rating.objects.get(question__question_string=question.question_string, rate=request.POST.get(
                    'cat-%s-row-%s' % (category.category_number, question.question_number)))
                try:
                    old_rate = scorecard.rating.get(
                        question__question_string=question.question_string)
                    if old_rate != new_rate:
                        scorecard.rating.remove(old_rate)
                        scorecard.rating.add(new_rate)
                except Rating.DoesNotExist:
                    scorecard.rating.add(new_rate)

                # return HttpResponse('old-%s new-%s' % (old_rate, new_rate))
        msg = MIMEMultipart()
        msg['From'] = "#"
        msg['To'] = scorecard.account_manager.email
        msg['Subject'] = "LOGISTICS MONTHLY SCORECARD"

        message = "10.162.197.88/login"

        # add in the message body
        msg.attach(MIMEText(message, 'plain'))

        mailserver = smtplib.SMTP('smtp.office365.com',587)
        mailserver.ehlo()
        mailserver.starttls()
        mailserver.login(msg['From'], '#')
        mailserver.sendmail(msg['From'], msg['To'], msg.as_string())
        scorecard.is_applicable = True
        scorecard.save()
        return HttpResponse("OK")
    else:
        return render(request, "form.html", context)


def email_view(request):

    send_mail('test', 'test', 'realtantan7@gmail.com',
              ['Alvin.Panganiban@artesyn.com'])
    return HttpResponse("OK")
