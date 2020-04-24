from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views

urlpatterns = [
    path('', views.events, name = 'events'),
    path('<int:event_id>/', views.event_details, name = 'event_details')

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()

# if settings.DEBUG:
#     urlpatterns += staticfiles_urlpatterns() + static(
#         settings.MEDIA_URL, document_root = settings.MEDIA_ROOT
#     )