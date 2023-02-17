# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
from datetime import datetime

from django.contrib.auth.models import User
from django.db.models import QuerySet
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, CreateView, ListView, DeleteView, View, DetailView
from django.utils.translation import ugettext as _

from accounts.models import OwnerRespondent, UserAccount
from MailGaner.settings import DEFAULT_DOMAIN, DEFAULT_DOMAIN_IP
from service.forms import MailingForm, MailingSettingsForm
from service.models import Mailing, MailingSettings
from service.tasks import send_mailing


class InitialView(TemplateView):
    template_name = 'index.html'


class HomeView(TemplateView):
    template_name = 'home.html'


class CreateMailing(CreateView):
    form_class = MailingForm
    success_url = reverse_lazy('accounts:account')
    queryset = Mailing.objects.all()
    template_name = 'create_mail.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(user=request.user)
        context = {'form': form}
        return self.render_to_response(context=context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(user=request.user, data=request.POST)
        if form.is_valid():
            saving = form.save(commit=False)
            saving.user = request.user
            saving.save()
            control_url = '{}{}'.format(DEFAULT_DOMAIN[:-1], reverse_lazy('sender:check_open',
                                                                        args=[saving.id]))
            control_link_url = '{}{}'.format(DEFAULT_DOMAIN[:-1], reverse_lazy('sender:check_open_link',
                                                                            args=[saving.id, 200]))
            control_pixel = '<img src={} style="width: 1px; height: 1px; border: none">'.format(
                control_url)
            answer_link = '<a class="link-answer" href="{}" style="height: 40px; ' \
                        'width: 100px; border: green solid 2px;' \
                        'border-radius: 3px; text-align: center;' \
                        'padding: 5px; font-size: 16px;">Спасибо</a>'.format(control_link_url)
            saving.body += control_pixel
            saving.body += answer_link
            saving.save()
            return HttpResponseRedirect(redirect_to=self.success_url)
        else:
            self.object = None
            return self.form_invalid(form)


class OwnerMailing(ListView):
    queryset = Mailing.objects.all()
    template_name = 'all_owner_mail.html'

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset().filter(user=request.user)
        settings = MailingSettings.objects.filter(
            mailing__in=[obj.id for obj in self.object_list]
        ).order_by('id')

        allow_empty = self.get_allow_empty()

        if not allow_empty:
            if self.get_paginate_by(self.object_list) is not None and hasattr(self.object_list, 'exists'):
                is_empty = not self.object_list.exists()
            else:
                is_empty = len(self.object_list) == 0
            if is_empty:
                raise Http404(_("Empty list and '%(class_name)s.allow_empty' is False.") % {
                    'class_name': self.__class__.__name__,
                })
        context = self.get_context_data()
        context.update({"settings": settings})
        return self.render_to_response(context)


class DeleteMailing(DeleteView):
    model = Mailing
    success_url = reverse_lazy('sender:all_mail')
    template_name = 'mailing_confirm_delete.html'


class SendMailing(View):
    success_url = reverse_lazy('sender:all_mail')

    def get(self, request, *args, **kwargs):
        parameters = {
            'owner': request.user.pk,
            'mailing': kwargs.get('pk')
        }
        send_mailing.delay(parameters)
        return HttpResponseRedirect(redirect_to=self.success_url)


class CheckOpenMailing(View):
    queryset = Mailing.objects.all()

    def get(self, request, *args, **kwargs):
        not_checked_url = '{}{}'.format(DEFAULT_DOMAIN[:-1], reverse_lazy('sender:all_mail'))
        script_dir = os.path.split(os.path.dirname(os.path.abspath(__file__)))[0]
        image_data = open(os.path.join(script_dir, 'static/any/pixel.png'), 'rb').read()
        mailing = self.queryset.get(pk=kwargs.get('pk'))
        if mailing and (request.META.get('HTTP_REFERER') != not_checked_url):
            mailing.opened += 1
            mailing.save()
        if kwargs.get('link'):
            return HttpResponse('Спасибо, что пользуетесь нашим сервисом!', status=200)

        return HttpResponse(image_data, content_type="image/png")


class MailingSettingsView(DetailView):
    queryset = MailingSettings.objects.all()
    form_class = MailingSettingsForm
    success_url = reverse_lazy('sender:all_mail')
    template_name = 'mailing_settings.html'

    def get(self, request, *args, **kwargs):
        users = User.objects.filter(id__in=[
            resp.subscriber.id for resp in OwnerRespondent.objects.filter(owner=request.user)
        ])
        form = self.form_class(users=users)
        context = {'form': form, 'mailing': Mailing.objects.get(pk=kwargs.get('pk'))}
        return self.render_to_response(context=context)

    def post(self, request, *args, **kwargs):
        mailing = Mailing.objects.get(pk=kwargs.get('pk'))
        form = self.form_class(users=User.objects.all(), data=request.POST)
        if form.is_valid():
            saving = form.save(commit=False)
            saving.mailing = mailing
            saving.save()
            parameters = {
                'owner': request.user.pk,
                'respondent': saving.send_to.pk if saving.send_to else None,
                'mailing': saving.mailing.pk
            }
            if not saving.send_via and not saving.send_in and not saving.send_by_birthday:
                send_mailing.delay(parameters)
            else:
                if saving.send_via:
                    send_mailing.apply_async(args=(parameters, ), countdown=saving.send_via * 60)
                if saving.send_in:
                    send_mailing.apply_async(args=(parameters, ), eta=saving.send_in)
                if saving.send_by_birthday:
                    if saving.send_to:
                        send_date = UserAccount.objects.get(user_id=saving.send_to.id).birthday
                        send_date = datetime(datetime.today().year, send_date.month, send_date.day)
                        send_mailing.apply_async(args=(parameters, ), eta=send_date)
                    else:
                        send_dates = [
                            (datetime(datetime.today().year, acc.birthday.month, acc.birthday.day), acc.user.id) for acc in UserAccount.objects.filter(
                                user_id__in=[
                                    resp.subscriber.id for resp in OwnerRespondent.objects.filter(
                                        owner=request.user
                                    )
                                ]
                            )
                        ]
                        for send_data in send_dates:
                            parameters['respondent'] = send_data[1]
                            send_mailing.apply_async(args=(parameters, ), eta=send_data[0])

        return HttpResponseRedirect(redirect_to=self.success_url)


class DeleteMailingSettings(DeleteView):
    model = MailingSettings
    success_url = reverse_lazy('sender:all_mail')
    template_name = 'settings_confirm_delete.html'