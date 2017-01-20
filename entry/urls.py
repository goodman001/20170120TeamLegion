from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.entry_list, name= 'list' ),
    #url(r'^(?P<patient_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^add/', views.entry_create, name= 'create'),
    url(r'^(?P<id>\d+)/$', views.entry_detail, name='detail'),
]