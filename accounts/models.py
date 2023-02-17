# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from django.db.models import CASCADE
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class UserAccount(models.Model):
    STATE_CHOICE = (
        ('o', 'owner'),
        ('s', 'subscriber')
    )

    user = models.OneToOneField(User, on_delete=CASCADE, verbose_name="Пользователь")
    birthday = models.DateField(verbose_name="Дата рождения")
    state = models.CharField(max_length=20, choices=STATE_CHOICE, verbose_name="Статус")
    company = models.CharField(max_length=20, null=True, blank=True, verbose_name="Организация")
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, verbose_name="Аватар")

    def __str__(self):
        return '{} {}'.format(self.user.last_name, self.user.first_name)


@python_2_unicode_compatible
class OwnerRespondent(models.Model):
    owner = models.ForeignKey(User, on_delete=CASCADE, related_name='rel_to')
    subscriber = models.ForeignKey(User, on_delete=CASCADE, related_name='rel_from')

    def __str__(self):
        return '{} signed {}'.format(self.subscriber, self.owner)