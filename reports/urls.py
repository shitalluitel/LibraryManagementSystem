from django.conf.urls import url
from . import views

app_name = "reports"

urlpatterns = [
    url(r'^$', views.report_home, name="home"),
    url(r'^book-order/$', views.book_order_report, name="book_order_report"),
    url(r'^student/$', views.student_report, name="student_report"),
    url(r'^export-to-pdf/$', views.export_pdf, name="export_to_pdf"),
]
