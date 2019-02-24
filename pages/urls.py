from django.conf.urls import url
from . import views

# app_name = "pages"

urlpatterns = [
    url(r'^$', views.home_page, name="home"),
    # url(r'^student-dashboard/$', views.student_dashboard, name="student_dashboard"),
]
