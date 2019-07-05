from django.contrib import admin
from survey_app.models import *
from django import forms
import calendar
import datetime
# Register your models here.
def get_last_day():
    return calendar.monthrange(datetime.datetime.now().year, datetime.datetime.now().month)[1]
class TriggerForm(forms.ModelForm):
    choice_field = forms.ChoiceField(
        choices=((str(x), x) for x in range(1,get_last_day()+1))
    )
    class Meta:
        model = Trigger
        fields = '__all__'
    
admin.site.register(Category)
admin.site.register(Question)
admin.site.register(Account_manager)
admin.site.register(Scorecard)
admin.site.register(Provider)
admin.site.register(Rating)
admin.site.register(Service)
admin.site.register(Feedback)
admin.site.register(Dev_date)
admin.site.register(Dev_month)
admin.site.register(Dev_day)
admin.site.register(Trigger)