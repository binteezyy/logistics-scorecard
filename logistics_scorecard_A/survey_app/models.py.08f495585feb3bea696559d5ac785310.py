from django.db import models
import datetime
from django import forms

# Create your models here.
class Dev_month(models.Model):
    month = models.IntegerField(default=0)

    def __str__(self):
        return str(self.month)

class Dev_day(models.Model):
    day = models.IntegerField(default=0)

    def __str__(self):
        return str(self.day)

class Dev_date(models.Model):
    dev_month = models.ForeignKey(Dev_month, on_delete=models.CASCADE)
    dev_day = models.ForeignKey(Dev_day, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.dev_month} / {self.dev_day}'

    class Meta:
        unique_together = ('dev_month', 'dev_day')

class Provider(models.Model):
    provider_name = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.provider_name}'

class Service(models.Model):
    name = models.CharField(max_length=30)
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, null=True)

    class Meta:
        unique_together = ('provider','name',)

    def __str__(self):
        return f'{self.provider}—{self.name}'

class Account_manager(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()

    def __str__(self):
        return str(self.name)

class Question(models.Model):
    question_number = models.IntegerField(default=0)
    question_string = models.TextField(unique=True)
    multiplier = models.DecimalField(max_digits=3, decimal_places=2, default=0)

    class Meta:
        ordering = ['question_number']

    def __str__(self):
        return str(self.question_number) + ". " + str(self.question_string)

class Category(models.Model):
    version = models.IntegerField(default=1)
    category_number = models.CharField(max_length=1)
    category_name = models.CharField(max_length=40)
    questions = models.ManyToManyField(Question)


    class Meta:
        unique_together = (('version','category_name','category_number'),)
        ordering = ['category_number']

    def __str__(self):
        return str(self.category_number) + ". " + str(self.category_name) + " v" +  str(self.version)

class Feedback(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    feedback = models.TextField(default="")

    def __str__(self):
        return str(self.question.question_number) + str(self.feedback)


class Rating(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    rate = models.IntegerField(blank=True)

    class Meta:
        unique_together = (('question','rate'),)

    def __str__(self):
        return "Question: " + str(self.question.question_number) + " Rating: " + str(self.rate)

class Scorecard(models.Model):
    cid = models.CharField(max_length=15, unique=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, null=True)
    month_covered = models.DateTimeField(blank=True)
    date_released = models.DateTimeField()
    account_manager = models.ForeignKey(Account_manager, on_delete=models.CASCADE)
    rating = models.ManyToManyField(Rating, blank=True)
    category_list = models.ManyToManyField(Category, blank=True)
    is_applicable = models.BooleanField(default=False)
    is_locked = models.BooleanField(default=False)
    feedback = models.ManyToManyField(Feedback, blank=True)

    def save(self, *args, **kwargs):
        self.month_covered = self.date_released - datetime.timedelta(30)
        super(Scorecard, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.cid)
