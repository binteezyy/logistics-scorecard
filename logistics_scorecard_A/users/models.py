from django.db import models
from django.contrib.auth.models import User

from survey_app.models import *

class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, null=True)
    is_active = models.BooleanField(default=True)
    scorecard = models.ManyToManyField(Scorecard, through='AppraiserList')

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
