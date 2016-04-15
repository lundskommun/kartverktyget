from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

import survey.urls
from crawls import settings

urlpatterns = [
    url(r'^ping$', 'survey.views.ping'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^s/', include(survey.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

