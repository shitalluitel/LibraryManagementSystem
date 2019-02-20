from django.conf.urls import url
from . import views

app_name = "fines"

urlpatterns = [
    url(r'^pay-amount/(?P<roll_no>[\w-]+)/$', views.pay_fine, name="pay_fine"),
    url(r'^student-pay-amount/$', views.get_student_fine, name="get_student_fine"),
]
