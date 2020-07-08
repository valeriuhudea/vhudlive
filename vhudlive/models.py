import uuid
import decimal
from datetime import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.contrib import admin

STORAGE_OPT = (
        ('DEFAULT', _('DEFAULT')),
        ('PRO', _('PRO')),
        ('UNLIMITED', _('UNLIMITED'))
    )

class Storage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=20, unique=True, blank=False, default='Vhud Name')
    type = models.CharField(max_length=14, choices=STORAGE_OPT, default='DEFAULT')
    active = models.BooleanField(default=True)
    owner = models.ForeignKey('auth.User', related_name='owner', on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True, null=True)
    updated_date = models.DateTimeField(auto_now=True, null=True)

    def __unicode__(self):
        return list(self.name, self.type, self.created_date, self.updated_date, self.owner)

    class Meta:
        ordering = ['created_date']


class Data(models.Model):
    data_of = models.ForeignKey(Storage, on_delete=models.CASCADE, related_name='data_of', null=True, blank=True)
    name = models.CharField(max_length=20, blank=False, unique=True, default='Data #1')
    details = models.TextField(null=True, blank=True)
    updated_date = models.DateField(auto_now=True, null=True)
    units = models.IntegerField(default=0)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['updated_date']

    def __unicode__(self):
        return list(self.name, self.details, self.updated_date, self.units, self.active)


