# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.db.models import CASCADE
from django.utils.encoding import python_2_unicode_compatible

from accounts.models import OwnerRespondent


@python_2_unicode_compatible
class Mailing(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE)
    title = models.CharField(max_length=50, verbose_name='Тема сообщения')
    body = RichTextUploadingField(verbose_name="Текст сообщения")
    opened = models.SmallIntegerField(default=0, verbose_name="Просмотрено")

    def __str__(self):
        return self.title


@python_2_unicode_compatible
class MailingSettings(models.Model):
    mailing = models.ForeignKey(Mailing, on_delete=CASCADE, verbose_name="Рассылка")
    send_via = models.SmallIntegerField(default=None, null=True, blank=True, verbose_name="Отправить через, мин")
    send_in = models.DateTimeField(default=None, null=True, blank=True, verbose_name="Отправить в")
    send_by_birthday = models.BooleanField(default=False, verbose_name="Отправить в день рождения")
    send_to = models.ForeignKey(User, null=True, blank=True, on_delete=CASCADE, verbose_name="Отправить подписчику")

    def __str__(self):
        return self.mailing.title