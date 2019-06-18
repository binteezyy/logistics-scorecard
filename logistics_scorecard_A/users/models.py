from django.db import models
from survey_app.models import Scorecard
from django.contrib.auth.models import User

class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    scorecard = models.ManyToManyField(Scorecard)
    is_active = models.BooleanField(default=True)
    is_sent_sc = models.BooleanField(default=False)
    def __str__(self):
        return str(self.user)

class Transactions(models.Model):
    scorecard = models.ManyToManyField(Scorecard)

    def __str__(self):
        return str(self.scorecard)
