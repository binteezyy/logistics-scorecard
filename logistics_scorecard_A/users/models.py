from django.db import models
from django.contrib.auth.models import User

from survey_app.models import *

class Template(models.Model):
    name = models.CharField(max_length=32)
    category = models.ManyToManyField(Category)
    def __str__(self):
        return f'{self.name}'
class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    template = models.ForeignKey(Template, on_delete=models.CASCADE, null=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, null=True)
    manager = models.ForeignKey(Account_manager, on_delete=models.CASCADE, null=True)
    is_active = models.BooleanField(default=True)
    scorecard = models.ManyToManyField(Scorecard, through='AppraiserList')

    class Meta:
        unique_together = ('user','service',)
    def __str__(self):
        return f'{self.user}'

class AppraiserList(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    is_sent_sc = models.BooleanField(default=False)
    scorecard = models.ForeignKey(Scorecard, on_delete=models.CASCADE, null=True)

    class Meta:
        unique_together = ('account','scorecard',)

    def __str__(self):
        return f'{self.account}'
