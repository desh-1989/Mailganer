# -*- coding: utf-8 -*-

from celery import shared_task
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives, get_connection

from accounts.models import OwnerRespondent
from MailGaner.settings import EMAIL_HOST_USER, DEFAULT_DOMAIN
from service.models import Mailing


@shared_task
def send_mailing(parameters):
    send_data = []
    user_from = User.objects.get(pk=parameters.get('owner'))
    if parameters.get('respondent'):
        users_to = [User.objects.get(pk=parameters.get('respondent'))]
    else:
        users_to = OwnerRespondent.objects.filter(owner=user_from)
    mailing = Mailing.objects.get(pk=parameters.get('mailing'))
    for recipient in users_to:
        if issubclass(recipient.__class__, User):
            name_ = recipient.first_name
            email_ = recipient.email
        else:
            name_ = recipient.subscriber.first_name
            email_ = recipient.subscriber.email
        html_msg = mailing.body.replace(
                '{user}', name_
            ).replace(
                '{owner}', user_from.first_name
            ).replace('src="/', 'src="{}'.format(DEFAULT_DOMAIN))
        single_data = EmailMultiAlternatives(
            mailing.title,
            html_msg,
            EMAIL_HOST_USER,
            [email_, ]
        )
        single_data.attach_alternative(html_msg, 'text/html')
        send_data.append(single_data)
    connection = get_connection()
    connection.send_messages(send_data)