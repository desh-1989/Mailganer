from django.conf.urls import url, include

from accounts.views import SignUp, AccountView, DeleteSubscriber, CreateSubscriber

app_name = 'accounts'

urlpatterns = [
    url('', include('django.contrib.auth.urls')),
    url(r'^signup/', SignUp.as_view(), name='signup'),
    url(r'^account/', AccountView.as_view(), name='account'),
    url(r'^delete/subscriber/(?P<pk>[\w]+)/$', DeleteSubscriber.as_view(), name='delete_subscriber'),
    url(r'^create/subscriber/(?P<pk>[\w]+)/$', CreateSubscriber.as_view(), name='create_subscriber')
]