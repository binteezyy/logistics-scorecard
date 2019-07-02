from django.contrib import admin
from users.models import *
# Register your models here.

class AppraiserListInline(admin.TabularInline):
    model = AppraiserList
    #readonly_fields = ('item_total',)

class PostAccount(admin.ModelAdmin):
    list_display = ('user','service','manager')
    inlines = [
        AppraiserListInline,
    ]

admin.site.register(Account,PostAccount)
admin.site.register(Template)
