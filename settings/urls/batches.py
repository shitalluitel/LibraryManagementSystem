from django.conf.urls import url, include
from settings.views import batches

app_name = "batches"

urlpatterns = [
    url('^create/$', batches.create, name="create"),
    url('^create/json/$', batches.create_json, name="create_json"),
    url('^$', batches.list, name="list"),
    url('^json_list/$', batches.json_list, name="json_list"),
    url('^edit/(?P<pk>\d+)/$', batches.edit, name="edit"),
    url('^delete/(?P<pk>\d+)/$', batches.delete, name="delete"),
    url('^(?P<pk>\d+)/course/$', batches.create_course_batch, name='course_batch'),
    url('^(?P<pk>\d+)/batch-list/$', batches.get_batch_list, name='get_batch_list'),
]
