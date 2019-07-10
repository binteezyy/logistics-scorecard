from django import forms
from survey_app.models import *
import calendar
import datetime



def get_last_day():
    return calendar.monthrange(datetime.datetime.now().year, datetime.datetime.now().month)[1]
class TriggerForm(forms.ModelForm):
    end_of_month_lock = forms.ChoiceField(
        choices=((str(x), x) for x in range(1,get_last_day()+1))
    )
    create_scorecards = forms.ChoiceField(
        choices=((str(x), x) for x in range(1,get_last_day()+1))
    )
    set_applicable_to_no = forms.ChoiceField(
        choices=((str(x), x) for x in range(1,get_last_day()+1))
    )
    send_to_providers = forms.ChoiceField(
        choices=((str(x), x) for x in range(1,get_last_day()+1))
    )
    extract_feedbacks  = forms.ChoiceField(
        choices=((str(x), x) for x in range(1,get_last_day()+1))
    )
    class Meta:
        model = Trigger
        fields = '__all__'