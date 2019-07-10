from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from django.urls import reverse_lazy

from django.core.mail import EmailMessage
from django.core.mail import send_mail
import smtplib
from django.core.exceptions import ObjectDoesNotExist

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.contrib.auth.decorators import login_required
from users.models import *

from ldap3 import Server, Connection, ALL, SUBTREE, ALL_ATTRIBUTES
from django.conf import settings
from django.contrib.auth.models import User
from . import tp

from django.views.generic import CreateView, UpdateView
from survey_app.forms import *
# Create your views here.

@login_required
def landing(request):
    current_user = request.user
    accounts = Account.objects.filter(user__username=current_user.username)
    is_manager = False
    if not accounts:
        accounts = Account.objects.filter(user_manager_email=current_user.email)
        is_manager = True
        context = {
            'accounts':accounts,
            # 'day':datetime.datetime.now().day,
            # 'month': datetime.datetime.now().month,
            'day': Dev_date.objects.get(pk=1).dev_day.day,
            'month': Dev_date.objects.get(pk=1).dev_month.month,
            'is_manager': is_manager,
        }

        return render(request, 'landing.html', context)

    context = {
            'accounts':accounts,
            # 'day':datetime.datetime.now().day,
            # 'month': datetime.datetime.now().month,
            'day': Dev_date.objects.get(pk=1).dev_day.day,
            'month': Dev_date.objects.get(pk=1).dev_month.month,
    }

    return render(request, 'landing.html', context)

@login_required
def view_scorecard(request,cid):
    scorecard = Scorecard.objects.get(cid=cid)
    categories = scorecard.category_list.all()
    ratings = scorecard.rating.all()
    feedbacks = scorecard.feedback.all()
    context = {
        "scorecard": scorecard,
        "categories": categories,
        "ratings": ratings,
        "feedbacks": feedbacks,
    }
    user1 = Account.objects.get(scorecard__cid=cid).user
    user2 = Account.objects.get(scorecard__cid=cid).user_manager_email
    current_user = request.user
    if str(user1) == str(current_user):
        return render(request, 'view.html', context)
    elif str(user2) == str(current_user.email):
        context.update({"is_manager": True})
        return render(request, 'view.html', context)
    return HttpResponse("Not ur scorecard")


@login_required
def index(request, cid):
    trigger = Trigger.objects.last()
    current_user = request.user
    scorecard = Scorecard.objects.get(cid=cid)
    user1 = Account.objects.get(scorecard__cid=cid).user
    categories = scorecard.category_list.all()
    ratings = scorecard.rating.all()
    feedbacks = scorecard.feedback.all()
    released = scorecard.date_released
    trigger = Trigger.objects.last()
    context = {
        "trigger": trigger,
        "scorecard": scorecard,
        "categories": categories,
        "ratings": ratings,
        # 'date_now': datetime.datetime.now(),
        'date_now': Dev_date.objects.get(pk=1),
        "feedbacks": feedbacks,
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

        logistics_manager_email = Account.objects.get(scorecard__cid=cid).user_manager_email
        scorecard.is_rated = True
        scorecard.is_applicable = True
        scorecard.save()

        msg = MIMEMultipart()
        msg['From'] = "joshuapascual@artesyn"
        #msg['PWD'] = ""
        msg['To'] = scorecard.account_manager.email
        msg['Subject'] = "LOGISTICS MONTHLY SCORECARD"

        message = "10.162.197.88/login"

        # # add in the message body
        msg.attach(MIMEText(message, 'plain'))

        set = Trigger.objects.get(pk=1)
        smpt_set = set.use_fake_smtp

        msg = MIMEMultipart('alternative')
        mailserver = smtplib.SMTP('')

        print("(1)365.OUTLOOK\t(2)fakeSMTP")
        if smpt_set == False:
            print("365.OUTLOOK")
            mailserver = smtplib.SMTP('smtp.office365.com',587)
            mailserver.ehlo()
            mailserver.starttls()
            mailserver.login(msg['From'],msg['PWD'])

        elif smpt_set == True:
            print("fakeSMTP")
            mailserver = smtplib.SMTP('localhost',25)
            mailserver.ehlo()

        else:
            print("INVALID smpt_set")

        clear()

        mailserver.sendmail(msg['From'], msg['To'], msg.as_string())
        return redirect('view_scorecard',cid)
    else:
        if str(user1) != str(current_user):
            return redirect('view_scorecard',cid)
        # if (datetime.datetime.now().day > 15 or datetime.datetime.now().month > released.month) and not scorecard.is_applicable and not scorecard.is_rated:
        if (Dev_date.objects.get(pk=1).dev_day.day > trigger.set_applicable_to_no or Dev_date.objects.get(pk=1).dev_month.month > released.month) and not scorecard.is_applicable and not scorecard.is_rated:
            return redirect('landing')
        # el# if (datetime.datetime.now().day > 15 or datetime.datetime.now().month > released.month) and scorecard.is_applicable and scorecard.is_rated:
        elif (Dev_date.objects.get(pk=1).dev_day.day > trigger.set_applicable_to_no or Dev_date.objects.get(pk=1).dev_month.month > released.month) and scorecard.is_applicable and scorecard.is_rated:
            return redirect('view_scorecard', cid)
        elif scorecard.is_applicable and scorecard.is_rated:
            return redirect('view_scorecard', cid)
        else:
            return render(request, 'form.html', context)

def trigger_update(request):
    settings = Trigger.objects.last()
    form = TriggerForm(instance=settings)
    if request.method == 'POST':
        form = TriggerForm(request.POST, instance=settings)
        if form.is_valid():
            form.save()
            return redirect('landing')
    else:
        form = TriggerForm(instance=settings)


    return render(request, 'survey_app/trigger_form.html', {"form":form})



def date_settings_view(request):
    today = Dev_date.objects.get(pk=1)
    if request.method == 'GET':
        context = {
            "today": today,
        }
        return render(request, 'date_form.html', context)
    else:
        # month_now = Dev_month.objects.get(month=request.POST.get('month'))
        # day_now = Dev_day.objects.get(day=request.POST.get('day'))
        # date_now = Dev_date.objects.get(dev_month=month_now, dev_day=day_now)
        # return HttpResponse(date_now)

        try:
            new_month = Dev_month.objects.get(month=request.POST.get('month'))
        except Dev_month.DoesNotExist:
            new_month = Dev_month(month=request.POST.get('month'))
            new_month.save()
            new_month = Dev_month.objects.get(month=request.POST.get('month'))
        try:
            new_day = Dev_day.objects.get(day=request.POST.get('day'))
        except Dev_day.DoesNotExist:
            new_day = Dev_day(day=request.POST.get('day'))
            new_day.save()
            new_day = Dev_day.objects.get(day=request.POST.get('day'))

        if new_month.month != today.dev_month.month:
            today.dev_month = new_month
            today.save()
        if new_day.day != today.dev_day.day:
            today.dev_day = new_day
            today.save()

        return redirect('date_settings')

def email_view(request):
    current_user = request.user
    userCN = 'CN=' + str(current_user.last_name) + '\, ' + str(current_user.first_name)

    server_url = settings.LDAP_AUTH_URL
    server = Server(server_url, get_info=ALL)

    connection_account = str(settings.LDAP_CN) + ',' + str(settings.LDAP_AUTH_SEARCH_BASE)
    connection_password = str(settings.LDAP_AUTH_CONNECTION_PASSWORD)

    conn = Connection(
    server,
    connection_account,
    connection_password,
    auto_bind=True)

    conn.search(
        search_base = str(userCN) + ',' + str(settings.LDAP_AUTH_SEARCH_BASE),
        search_filter = '(objectClass=user)',
        search_scope = SUBTREE,
        types_only=False,
        attributes=['manager'],
        get_operational_attributes=True,
        size_limit=1,
        )

    manager_dn = conn.response[0]['attributes']['manager']

    conn.search(
        search_base = manager_dn,
        search_filter = '(objectClass=user)',
        search_scope = SUBTREE,
        types_only=False,
        attributes=['mail'],
        get_operational_attributes=True,
        size_limit=1,
        )

    return HttpResponse(conn.response[0]['attributes']['mail'])

def create_template(request):
    #C1
    create_cat = Category(version=1, category_number=tp.C1_Cn, category_name=tp.C1_C)
    create_cat.save()
    cat = Category.objects.get(version=1, category_number=tp.C1_Cn, category_name=tp.C1_C)

    create_question = Question(question_number=tp.C1_Q1_N, question_string=tp.C1_Q1_S, multiplier=tp.C1_Q1_W)
    create_question.save()
    add_question = Question.objects.get(question_number=tp.C1_Q1_N, question_string=tp.C1_Q1_S, multiplier=tp.C1_Q1_W)
    cat.questions.add(add_question)

    create_question = Question(question_number=tp.C1_Q2_N, question_string=tp.C1_Q2_S, multiplier=tp.C1_Q2_W)
    create_question.save()
    add_question = Question.objects.get(question_number=tp.C1_Q2_N, question_string=tp.C1_Q2_S, multiplier=tp.C1_Q2_W)
    cat.questions.add(add_question)

    #C2
    create_cat = Category(version=1, category_number=tp.C2_Cn, category_name=tp.C2_C)
    create_cat.save()
    cat = Category.objects.get(version=1, category_number=tp.C2_Cn, category_name=tp.C2_C)

    create_question = Question(question_number=tp.C2_Q1_N, question_string=tp.C2_Q1_S, multiplier=tp.C2_Q1_W)
    create_question.save()
    add_question = Question.objects.get(question_number=tp.C2_Q1_N, question_string=tp.C2_Q1_S, multiplier=tp.C2_Q1_W)
    cat.questions.add(add_question)

    create_question = Question(question_number=tp.C2_Q2_N, question_string=tp.C2_Q2_S, multiplier=tp.C2_Q2_W)
    create_question.save()
    add_question = Question.objects.get(question_number=tp.C2_Q2_N, question_string=tp.C2_Q2_S, multiplier=tp.C2_Q2_W)
    cat.questions.add(add_question)

    create_question = Question(question_number=tp.C2_Q3_N, question_string=tp.C2_Q3_S, multiplier=tp.C2_Q3_W)
    create_question.save()
    add_question = Question.objects.get(question_number=tp.C2_Q3_N, question_string=tp.C2_Q3_S, multiplier=tp.C2_Q3_W)
    cat.questions.add(add_question)

    create_question = Question(question_number=tp.C2_Q4_N, question_string=tp.C2_Q4_S, multiplier=tp.C2_Q4_W)
    create_question.save()
    add_question = Question.objects.get(question_number=tp.C2_Q4_N, question_string=tp.C2_Q4_S, multiplier=tp.C2_Q4_W)
    cat.questions.add(add_question)

    #c3
    create_cat = Category(version=1, category_number=tp.C3_Cn, category_name=tp.C3_C)
    create_cat.save()
    cat = Category.objects.get(version=1, category_number=tp.C3_Cn, category_name=tp.C3_C)

    create_question = Question(question_number=tp.C3_Q1_N, question_string=tp.C3_Q1_S, multiplier=tp.C3_Q1_W)
    create_question.save()
    add_question = Question.objects.get(question_number=tp.C3_Q1_N, question_string=tp.C3_Q1_S, multiplier=tp.C3_Q1_W)
    cat.questions.add(add_question)

    create_question = Question(question_number=tp.C3_Q2_N, question_string=tp.C3_Q2_S, multiplier=tp.C3_Q2_W)
    create_question.save()
    add_question = Question.objects.get(question_number=tp.C3_Q2_N, question_string=tp.C3_Q2_S, multiplier=tp.C3_Q2_W)
    cat.questions.add(add_question)

    #C4
    create_cat = Category(version=1, category_number=tp.C4_Cn, category_name=tp.C4_C)
    create_cat.save()
    cat = Category.objects.get(version=1, category_number=tp.C4_Cn, category_name=tp.C4_C)

    create_question = Question(question_number=tp.C4_Q1_N, question_string=tp.C4_Q1_S, multiplier=tp.C4_Q1_W)
    create_question.save()
    add_question = Question.objects.get(question_number=tp.C4_Q1_N, question_string=tp.C4_Q1_S, multiplier=tp.C4_Q1_W)
    cat.questions.add(add_question)

    #C5
    create_cat = Category(version=1, category_number=tp.C5_Cn, category_name=tp.C5_C)
    create_cat.save()
    cat = Category.objects.get(version=1, category_number=tp.C5_Cn, category_name=tp.C5_C)

    create_question = Question(question_number=tp.C5_Q1_N, question_string=tp.C5_Q1_S, multiplier=tp.C5_Q1_W)
    create_question.save()
    add_question = Question.objects.get(question_number=tp.C5_Q1_N, question_string=tp.C5_Q1_S, multiplier=tp.C5_Q1_W)
    cat.questions.add(add_question)

    create_question = Question(question_number=tp.C5_Q2_N, question_string=tp.C5_Q2_S, multiplier=tp.C5_Q2_W)
    create_question.save()
    add_question = Question.objects.get(question_number=tp.C5_Q2_N, question_string=tp.C5_Q2_S, multiplier=tp.C5_Q2_W)
    cat.questions.add(add_question)

    create_question = Question(question_number=tp.C5_Q3_N, question_string=tp.C5_Q3_S, multiplier=tp.C5_Q3_W)
    create_question.save()
    add_question = Question.objects.get(question_number=tp.C5_Q3_N, question_string=tp.C5_Q3_S, multiplier=tp.C5_Q3_W)
    cat.questions.add(add_question)

    create_question = Question(question_number=tp.C5_Q4_N, question_string=tp.C5_Q4_S, multiplier=tp.C5_Q4_W)
    create_question.save()
    add_question = Question.objects.get(question_number=tp.C5_Q4_N, question_string=tp.C5_Q4_S, multiplier=tp.C5_Q4_W)
    cat.questions.add(add_question)

    create_question = Question(question_number=tp.C5_Q5_N, question_string=tp.C5_Q5_S, multiplier=tp.C5_Q5_W)
    create_question.save()
    add_question = Question.objects.get(question_number=tp.C5_Q5_N, question_string=tp.C5_Q5_S, multiplier=tp.C5_Q5_W)
    cat.questions.add(add_question)

    #C6
    create_cat = Category(version=1, category_number=tp.C6_Cn, category_name=tp.C6_C)
    create_cat.save()
    cat = Category.objects.get(version=1, category_number=tp.C6_Cn, category_name=tp.C6_C)

    create_question = Question(question_number=tp.C6_Q1_N, question_string=tp.C6_Q1_S, multiplier=tp.C6_Q1_W)
    create_question.save()
    add_question = Question.objects.get(question_number=tp.C6_Q1_N, question_string=tp.C6_Q1_S, multiplier=tp.C6_Q1_W)
    cat.questions.add(add_question)

    create_question = Question(question_number=tp.C6_Q2_N, question_string=tp.C6_Q2_S, multiplier=tp.C6_Q2_W)
    create_question.save()
    add_question = Question.objects.get(question_number=tp.C6_Q2_N, question_string=tp.C6_Q2_S, multiplier=tp.C6_Q2_W)
    cat.questions.add(add_question)

    create_question = Question(question_number=tp.C6_Q3_N, question_string=tp.C6_Q3_S, multiplier=tp.C6_Q3_W)
    create_question.save()
    add_question = Question.objects.get(question_number=tp.C6_Q3_N, question_string=tp.C6_Q3_S, multiplier=tp.C6_Q3_W)
    cat.questions.add(add_question)

    return HttpResponse("OK")
