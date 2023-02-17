from ckeditor_uploader import views
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache

from service.views import InitialView, HomeView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', InitialView.as_view(), name="initial"),
    url(r'^accounts/', include('accounts.urls', namespace='accounts')),
    url(r'^service/', include('service.urls', namespace='service')),
    url(r'^ckeditor/upload/', login_required(views.upload), name='ckeditor_upload'),
    url(r'^ckeditor/browse/', never_cache(login_required(views.browse)), name='ckeditor_browse')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)