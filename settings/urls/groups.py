from django.conf.urls import url, include
from settings.views import groups

app_name = "groups"

urlpatterns = [
    url('^create/$', groups.create_group, name="create_group"),
    url('^edit/(?P<pk>\d+)/$', groups.edit_group, name="edit_group"),
    url('^$', groups.list_group, name="list_group"),
]
