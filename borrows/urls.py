from django.conf.urls import url
from . import views

app_name = "borrows"

urlpatterns = [
    url(r'^$', views.list_borrow, name="list_borrow"),
    url(r'^order/(?P<pk>\d+)$', views.order_bookunit, name="order_bookunit"),
    url(r'^assign/(?P<pk>\d+)$', views.assign_bookunit, name="assign_bookunit"),
    url(r'^cancel/request/(?P<pk>\d+)$', views.cancel_request, name="cancel_request"),
]
