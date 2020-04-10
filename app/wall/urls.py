from django.conf.urls import url
from . import views



urlpatterns = [
    url(r'^$', views.index),
    url(r'^create$', views.create),
    url(r'^login$', views.login),
    url(r'^show$', views.show),
    url(r'^destroy$', views.destroy),
    url(r'^create/message$', views.message),
    url(r'^create/comment$', views.comment),
    
]
