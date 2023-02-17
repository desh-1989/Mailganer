# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from accounts.models import UserAccount, OwnerRespondent

admin.site.register(UserAccount)
admin.site.register(OwnerRespondent)