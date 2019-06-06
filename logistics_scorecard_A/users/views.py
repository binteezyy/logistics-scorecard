from django.shortcuts import render, redirect
from . models import *
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
import datetime
from django.contrib.auth import logout
from survey_app.models import *
# Create your views here.

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
                old_rate = scorecard.rating.get(
                    question__question_string=question.question_string)
                new_rate = Rating.objects.get(question__question_string=question.question_string, rate=request.POST.get(
                    'cat-%s-row-%s' % (category.category_number, question.question_number)))
                                
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
        return HttpResponse("OK")
    else:
        return render(request, "form.html", context)
