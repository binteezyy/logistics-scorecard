from django.db import models
from django.contrib.auth.models import User

from ldap3 import Server, Connection, ALL, SUBTREE, ALL_ATTRIBUTES
from django.conf import settings

from survey_app.models import *

class Template(models.Model):
    name = models.CharField(max_length=32)
    category = models.ManyToManyField(Category)
    def __str__(self):
        return f'{self.name}'

class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_manager_email = models.EmailField(blank=True)
    template = models.ForeignKey(Template, on_delete=models.CASCADE, null=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, null=True)
    manager = models.ForeignKey(Account_manager, on_delete=models.CASCADE, null=True)
    is_active = models.BooleanField(default=True)
    scorecard = models.ManyToManyField(Scorecard, through='AppraiserList')

    class Meta:
        unique_together = ('user','service',)
    def __str__(self):
        return f'{self.user} - {self.service}'
    def save(self, *args, **kwargs):
        userCN = 'CN=' + str(self.user.last_name) + '\, ' + str(self.user.first_name)
        server_url = settings.LDAP_AUTH_URL
        server = Server(server_url, get_info=ALL)

        connection_account = str(settings.LDAP_CN) + ',' + str(settings.LDAP_AUTH_SEARCH_BASE)
        connection_password = str(settings.LDAP_AUTH_CONNECTION_PASSWORD)

        conn = Connection(
        server,
        connection_account,
        connection_password,
        auto_bind=True)

        conn.search(
            search_base = str(userCN) + ',' + str(settings.LDAP_AUTH_SEARCH_BASE),
            search_filter = '(objectClass=user)',
            search_scope = SUBTREE,
            types_only=False,
            attributes=['manager'],
            get_operational_attributes=True,
            size_limit=1,
            )
        manager_dn = conn.response[0]['attributes']['manager']

        conn.search(
            search_base = manager_dn,
            search_filter = '(objectClass=user)',
            search_scope = SUBTREE,
            types_only=False,
            attributes=['mail'],
            get_operational_attributes=True,
            size_limit=1,
            )
        self.user_manager_email = conn.response[0]['attributes']['mail']
        super(Account, self).save(*args,**kwargs)

class AppraiserList(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    scorecard = models.ForeignKey(Scorecard, on_delete=models.CASCADE, null=True)
    is_sent_sc = models.BooleanField(default=False)
    is_notified = models.DateTimeField(null=True)
    feedback_sent = models.DateTimeField(null=True,blank=True)
    class Meta:
        unique_together = ('account','scorecard',)

    def __str__(self):
        return f'{self.account}'
