from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^rvalidate$', views.rvalidate),
    url(r'^travels$', views.travels),
    url(r'^lvalidate$', views.lvalidate),
    url(r'^success$', views.success),
    url(r'^destination/(?P<id>\d+)$', views.destination),
    url(r'^add$', views.add),
    url(r'^delete/(?P<id>\d+)$', views.delete),
    url(r'^logout$', views.logout),
    url(r'^join/(?P<id>\d+)$', views.join),
]
