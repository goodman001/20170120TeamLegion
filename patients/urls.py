from django.conf.urls import url
from . import views

urlpatterns = [
    # /patients/
    url(r'^$', views.index, name= 'index' ),

    # /patients/324             :: Where 324 is a Patient ID
    url(r'^(?P<patient_id>[0-9]+)/$', views.detail, name= 'detail'),

    # /patients/create
    url(r'^create/', views.create, name= 'create'),

    # /patients/update
    url(r'^update/', views.update, name= 'update'),

    # /patients/delete
    url(r'^delete/', views.delete, name= 'delete'),
    url(r'^regpage/$',views.regpage,name = "patientregpage"),
    url(r'^regstore/$',views.reg_store,name = "patientregstore"),
    url(r'^logincheck/$',views.logincheck,name = "patientlogincheck"),

    url(r'^mainpage/(\d+)/$',views.mainpage,name = "patientmainpage"),
    url(r'^logoff/$',views.logoff,name = "patientlogoff"),

]
