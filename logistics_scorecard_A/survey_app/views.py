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

from ldap3 import Server, Connection, ALL, SUBTREE, ALL_ATTRIBUTES
from django.conf import settings
from django.contrib.auth.models import User
from . import tp

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
    feedbacks = scorecard.feedback.all()
    context = {
        "scorecard": scorecard,
        "categories": categories,
        "ratings": ratings,
        "feedbacks": feedbacks,
    }
    return render(request, 'view.html', context)


@login_required
def index(request, cid):
    current_user = request.user
    scorecard = Scorecard.objects.get(cid=cid)
    user1 = scorecard.account_set.first()
    categories = scorecard.category_list.all()
    ratings = scorecard.rating.all()
    feedbacks = scorecard.feedback.all()
    context = {
        "scorecard": scorecard,
        "categories": categories,
        "ratings": ratings,
        'date_now': datetime.datetime.now(),
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

                # return HttpResponse('old-%s new-%s' % (old_rate, new_rate))

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

        logistics_manager_email = conn.response[0]['attributes']['mail']
        scorecard.is_applicable = True
        scorecard.save()
        return HttpResponse(logistics_manager_email)

        # msg = MIMEMultipart()
        # msg['From'] = "#"
        # msg['To'] = scorecard.account_manager.email
        # msg['Subject'] = "LOGISTICS MONTHLY SCORECARD"

        # message = "10.162.197.88/login"

        # # add in the message body
        # msg.attach(MIMEText(message, 'plain'))

        # mailserver = smtplib.SMTP('smtp.office365.com',587)
        # mailserver.ehlo()
        # mailserver.starttls()
        # mailserver.login(msg['From'], '#')
        # mailserver.sendmail(msg['From'], msg['To'], msg.as_string())
        # scorecard.is_applicable = True
        # scorecard.save()
        # return HttpResponse("OK")
    else:
        if str(user1) != str(current_user):
            return redirect('landing')
        if datetime.datetime.now().day > 15 and not scorecard.is_applicable:
            return redirect('landing')
        elif datetime.datetime.now().day > 30:
            return redirect('view_scorecard', cid)
        else:   
            return render(request, 'form.html', context)


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
    
<<<<<<< HEAD
    return HttpResponse(conn.response[0]['attributes']['mail'])
=======
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
>>>>>>> new-ldap
