from django.conf.urls import url
from . import views

# app_name = "pages"

urlpatterns = [
    url(r'^$', views.home_page, name="home"),
    url(r'^notifications/list/$', views.notification_list, name="notification_list"),
    url(r'^notifications/mark-all-as-read/$', views.mark_all_as_read, name="mark_all_as_read"),
    # url(r'^student-dashboard/$', views.student_dashboard, name="student_dashboard"),
]
