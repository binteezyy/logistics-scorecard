from django.shortcuts import render
from django.http import HttpResponse
from .models import *

from django.core.mail import EmailMessage
from django.core.mail import send_mail
import smtplib
from django.core.exceptions import ObjectDoesNotExist

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


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
                #         # return HttpResponse(request.POST.get('cat-%s-row-%s' % (category.category_number, question.question_number)))
                #         # for rating in scorecard.rating.all():
                #         #     if rating.question.question_string == question.question_string:
                #         # Rating.objects.filter(question__question_string=question.question_string).update(rate=request.POST.get('cat-%s-row-%s' % (category.category_number, question.question_number)))
                old_rate = scorecard.rating.get(
                    question__question_string=question.question_string)
                new_rate = Rating.objects.get(question__question_string=question.question_string, rate=request.POST.get(
                    'cat-%s-row-%s' % (category.category_number, question.question_number)))
                # new_rate = Scorecard.objects.get(cid=cid, rating__question__question_string=question.question_string, rating__rate=request.POST.get('cat-%s-row-%s' % (category.category_number, question.question_number)))[0]

                # new_rate = request.POST.get('cat-%s-row-%s' % (category.category_number, question.question_number))
                if old_rate != new_rate:
                    scorecard.rating.remove(old_rate)
                    scorecard.rating.add(new_rate)

                # return HttpResponse('old-%s new-%s' % (old_rate, new_rate))
        # msg = MIMEMultipart()
        # msg['From'] = "#"
        # msg['To'] = scorecard.account_manager.email
        # msg['Subject'] = "LOGISTICS MONTHLY SCORECARD"

        # message = "MenRTrashMenRTrashMenRTrashMenRTrashMenRTrash"

        # # add in the message body
        # msg.attach(MIMEText(message, 'plain'))

        # mailserver = smtplib.SMTP('smtp.office365.com',587)
        # mailserver.ehlo()
        # mailserver.starttls()
        # mailserver.login(msg['From'], 'password')
        # mailserver.sendmail(msg['From'], msg['To'], msg.as_string())
        return HttpResponse(scorecard.account_manager.email)
    else:
        return render(request, "form.html", context)


def email_view(request):

    send_mail('test', 'test', 'realtantan7@gmail.com',
              ['Alvin.Panganiban@artesyn.com'])
    return HttpResponse("OK")
