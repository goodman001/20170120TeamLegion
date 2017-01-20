from django.conf.urls import url
from . import views

urlpatterns = [
    # /doctors/
    url(r'^$', views.index, name= 'docindex' ),
    
    # register 
    url(r'^regpage/$',views.regpage,name = "doctorregpage"),

    url(r'^regstore/$',views.reg_store,name = "doctorregstore"),
    #login
    url(r'^logincheck/$',views.logincheck,name = "doctorlogincheck"),
    
    url(r'^mainpage/(\d+)/$',views.mainpage,name = "doctormainpage"),
  
    url(r'^updatepage/$',views.updatepage,name = "doctorupdatepage"),

    url(r'^addpage/$',views.addpage,name = "doctoraddpage"),
   
    url(r'^logoff/$',views.logoff,name = "doctorlogoff"), 

    # /doctors/222             :: Where 222 is a doctor ID
    url(r'^(?P<doctor_id>[0-9]+)/$', views.detail, name= 'detail'),

    # /doctors/create
    url(r'^add/(\d+)/$', views.add, name= 'doc_add'),

    # /doctors/update
    url(r'^update/$', views.update, name= 'doc_update'),

    # /doctors/delete
    url(r'^delete/(\d+)/$', views.delete, name= 'doc_delete'),
	
	# /doctors/view
    url(r'^view_pic/(\d+)/$', views.view_pic, name= 'doc_view'),

]
