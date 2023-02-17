# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import login
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, View, DeleteView
from django.views.generic.detail import SingleObjectTemplateResponseMixin

from accounts.forms import LoginForm
from accounts.models import UserAccount, OwnerRespondent


class SignUp(CreateView):
    account_fields = ['birthday', 'state']
    form_class = LoginForm
    success_url = reverse_lazy('accounts:account')
    template_name = 'registration/signup.html'

    def post(self, request, *args, **kwargs):
        account_data = {key: request.POST[key] for key in self.account_fields}
        form = self.get_form()

        if form.is_valid():
            self.form_valid(form)
            user = form.instance
            user.password = make_password(request.POST.get('password'))
            user.save()
            account_data.update({'user': user})
            UserAccount.objects.create(**account_data)
            login(self.request, user)

            return HttpResponseRedirect(redirect_to=self.success_url)
        else:
            self.object = None
            return self.form_invalid(form)


class AccountView(SingleObjectTemplateResponseMixin, View):
    queryset = UserAccount.objects.all()
    template_name = 'account.html'

    def get(self, request, *args, **kwargs):
        account = self.queryset.get(user=self.request.user)
        community = self.queryset.filter(state='o') if account.state == 's' else\
            self.queryset.filter(state='s')
        owner_community = OwnerRespondent.objects.filter(owner=request.user)
        subscriber_community = OwnerRespondent.objects.filter(subscriber=request.user)
        context = {
            'account': account,
            'community': community,
            'owner_community': owner_community,
            'subscriber_community': subscriber_community
        }
        return self.render_to_response(context)


class DeleteSubscriber(DeleteView):
    model = OwnerRespondent
    success_url = reverse_lazy('accounts:account')
    template_name = 'delete_subscribe.html'


class CreateSubscriber(CreateView):
    queryset = User.objects.all()
    success_url = reverse_lazy('accounts:account')
    template_name = 'new_subscribe.html'

    def get(self, request, *args, **kwargs):
        context = {
            'owner': request.user,
            'subscriber': self.queryset.get(pk=kwargs.get('pk'))
        }
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        subscriber = request.user
        owner = self.queryset.get(pk=request.POST.get('subscriber'))
        new_subscribe = OwnerRespondent(owner=owner, subscriber=subscriber)
        new_subscribe.save()
        return HttpResponseRedirect(redirect_to=self.success_url)