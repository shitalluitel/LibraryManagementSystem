from django.conf.urls import url
from . import views

app_name = "routines"

urlpatterns = [
    url(r'^create/$', views.routine_create, name="create"),
    url(r'^edit/$', views.routine_edit, name="edit"),
    url(r'^list/$', views.routine_list, name="list"),
    url(r'^delete/$', views.routine_delete, name="delete"),
    url(r'^formset-data-delete/(?P<pk>\d+)/$', views.unit_routine_delete, name="unit_routine_delete"),

]
