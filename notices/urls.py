from django.conf.urls import url
from . import views

app_name = "notices"

urlpatterns = [
    url(r'^upload/$', views.notice_upload, name="notice_upload"),
    url(r'^update/(?P<pk>\d+)$', views.notice_update, name="notice_update"),
    url(r'^home/$', views.notice_home, name="notice_home"),
    url(r'^list/$', views.notice_list, name="notice_list"),
    url(r'^delete/(?P<pk>\d+)/$', views.notice_delete, name="notice_delete"),
    url(r'^detail/(?P<pk>\d+)/$', views.notice_detail, name="notice_detail"),
]
