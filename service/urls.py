from django.conf.urls import url, include

from service.views import HomeView, CreateMailing, OwnerMailing, \
    DeleteMailing, SendMailing, CheckOpenMailing, MailingSettingsView, DeleteMailingSettings

app_name = 'sender'

urlpatterns = [
    url(r'^home/', HomeView.as_view(), name="home"),
    url(r'^mail/create/', CreateMailing.as_view(), name='create_mail'),
    url(r'^mail/all/', OwnerMailing.as_view(), name='all_mail'),
    url(r'^mail/delete/(?P<pk>[\w]+)/$', DeleteMailing.as_view(), name='delete'),
    url(r'^mail/send/(?P<pk>[\w]+)/$', SendMailing.as_view(), name='send'),
    url(r'^mail/open/(?P<pk>[\w]+)/$', CheckOpenMailing.as_view(), name='check_open'),
    url(r'^mail/open/(?P<pk>[\w]+)/(?P<link>[\w]+)/$', CheckOpenMailing.as_view(), name='check_open_link'),
    url(r'^mail/settings/(?P<pk>[\w]+)/$', MailingSettingsView.as_view(), name='settings'),
    url(r'^settings/delete/(?P<pk>[\w]+)/$', DeleteMailingSettings.as_view(), name='delete_settings'),
]