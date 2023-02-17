# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from service.models import Mailing, MailingSettings

admin.site.register(Mailing)
admin.site.register(MailingSettings)