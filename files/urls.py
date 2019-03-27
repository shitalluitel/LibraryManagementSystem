from django.conf.urls import url
from . import views

app_name = "files"

urlpatterns = [
    url(r'^upload/$', views.file_upload, name="file_upload"),
    url(r'^home/$', views.file_home, name="file_home"),
    url(r'^list/$', views.file_list, name="file_list"),
    url(r'^delete/(?P<pk>\d+)/$', views.file_delete, name="file_delete"),
]
