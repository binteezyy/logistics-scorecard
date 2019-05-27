from django.db import models

# Create your models here.
class Service(models.Model):
    name = models.CharField(max_length=30)
    
    def __str__(self):
        return str(self.name)

class Provider(models.Model):
    provider_name = models.CharField(max_length=50)
    services = models.ManyToManyField(Service)
    
    def __str__(self):
        return str(self.provider_name)
    
class Account_manager(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    
    def __str__(self):
        return str(self.name)

class Question(models.Model):
    question_number = models.IntegerField(default=0)
    question_string = models.TextField(unique=True)
    multiplier = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    
    def __str__(self):
        return str(self.question_string)

class Category(models.Model):
    category_number = models.IntegerField(default=0)
    category_name = models.CharField(max_length=40)
    questions = models.ManyToManyField(Question)
    
    def __str__(self):
        return str(self.category_name)
    
class Rating(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    rate = models.IntegerField(blank=True)
    
    def __str__(self):
        return str(self.question)    

class Scorecard(models.Model):
    cid = models.CharField(max_length=15, unique=True)
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    month_covered = models.DateTimeField()
    date_released = models.DateTimeField()
    account_manager = models.ForeignKey(Account_manager, on_delete=models.CASCADE)
    rating = models.ManyToManyField(Rating, blank=True)
    
    def __str__(self):
        return str(self.cid)