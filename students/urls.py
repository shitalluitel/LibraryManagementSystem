from django.conf.urls import url
from . import views

app_name = "students"

urlpatterns = [
    # url(r'^choose/course-batch/$', views.create_choice, name="create_choice"),
    url(r'^create/$', views.create_student, name="create_student"),
    url(r'^$', views.list_student, name="list_student"),
    # url(r'^create/$', views.create_student, name="create_student"),
]
