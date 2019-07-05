from django.contrib import admin
from survey_app.models import *
from django import forms
from users.models import *
from django.contrib import admin


# def get_unselected_questions():
#     selected_q =[]
#     all_qlist = []
#     categories = Category.objects.all()
#     all_q = Question.objects.all()
#     for each in categories:
#         print(each.category_name)
#         for every in each.questions.all():
#             selected_q.append(every.id)
#     for each in all_q:
#         all_qlist.append(each.id)
#     unselected = list(set(all_qlist) - set(selected_q))
#     q_unselected = Question.objects.filter(pk__in=unselected)
#     return q_unselected

# get_unselected_questions()

# class CategoryForm(forms.ModelForm):
#     questions = forms.ModelMultipleChoiceField(queryset=get_unselected_questions()) 
#     class Meta:
#         model = Category
#         exclude=[]
#         # widget = {
#         #     'questions': forms.Select(),    
#         # }
         
      

# class CategoryAdmin(admin.ModelAdmin):
#     form = CategoryForm
# # Register your models here.

admin.site.register(Category)
admin.site.register(Question)
admin.site.register(Account_manager)
admin.site.register(Scorecard)
admin.site.register(Provider)
admin.site.register(Rating)
admin.site.register(Service)
admin.site.register(Feedback)
