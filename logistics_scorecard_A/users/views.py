from django.shortcuts import render, redirect
from . models import *
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
import datetime
from django.contrib.auth import logout
from django.contrib.auth import authenticate
from survey_app.models import *
from django.http import JsonResponse
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.contrib.auth.models import User
import time
# Create your views here.


def verify(request):
    verify=False
    userstore = ""
    if request.method == 'POST':
        username = request.POST['username']
        if username is not None:
            try:
                userstore = User.objects.get(username=username)
            except:
                pass
            if userstore:
                print(userstore)
                verify=True
            

    status = {
        "verified": verify,
    }
    return JsonResponse(status)

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
    if datetime.datetime.now().day > 15 and scorecard.is_applicable == False:
       return HttpResponse("You can't change it anymore!")
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
        return render(request, "try.html", context)
