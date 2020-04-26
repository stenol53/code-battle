from django.urls import path

from . import views

urlpatterns = [
    path('',views.index,name = 'index'),
    path("<int:id>/",views.open_battle,name = 'openbattle'),
    path('user_validate/',views.user_validate,name = 'validate'),
]