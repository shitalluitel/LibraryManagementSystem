from django.conf.urls import url, include
from settings.views import courses

app_name = "courses"

urlpatterns = [
    url('^create/$', courses.create, name="create"),
    url('^create/json/$', courses.create_json, name="create_json"),
    url('^$', courses.list, name="list"),
    url('^json_list/$', courses.json_list, name="json_list"),
    url('^edit/(?P<pk>\d+)/$', courses.edit, name="edit"),
    url('^delete/(?P<pk>\d+)/$', courses.delete, name="delete"),
]
