from django.contrib import admin
from users.models import *
# Register your models here.

class AppraiserListInline(admin.TabularInline):
    model = AppraiserList
    #readonly_fields = ('item_total',)

class PostAccount(admin.ModelAdmin):
    #list_display = ('is_active','user','provider','get_scorecards',)
    inlines = [
        AppraiserListInline,
    ]

    def get_scorecards(self, obj):
        return "\n".join([p.scorecard for p in obj.scorecard.all()])
admin.site.register(Account,PostAccount)
