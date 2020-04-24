from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views
from .views import accept_event, deny_event, get_events_api

urlpatterns = [
    path('', views.events, name = 'events'),
    # path('accept/',views.event_accept,name = 'accept'),
    path('<int:event_id>/', views.event_details, name = 'event_details'),
    path('accept/',accept_event, name = 'accept'),
    path('deny/',deny_event,name = 'deny'),
    path('api/',get_events_api,name = 'api'),
]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns() + static(
        settings.MEDIA_URL, document_root = settings.MEDIA_ROOT
    )
