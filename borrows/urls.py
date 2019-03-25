from django.conf.urls import url
from . import views

app_name = "borrows"

urlpatterns = [
    url(r'^$', views.list_borrow, name="list_borrow"),
    url(r'^approved/$', views.list_approved_borrow, name="list_approved_borrow"),
    url(r'^return/(?P<pk>\d+)/bookunit/$', views.return_bookunit, name="return_book"),
    url(r'^return/(?P<pk>\d+)/borrowed/bookunit/$', views.return_borrow_book, name="return_borrow_book"),
    url(r'^order/(?P<pk>\d+)/$', views.order_bookunit, name="order_bookunit"),
    url(r'^assign/(?P<pk>\d+)/$', views.assign_borrow_bookunit, name="assign_borrow_bookunit"),
    url(r'^cancel/request/(?P<pk>\d+)/$', views.cancel_request, name="cancel_request"),
    url(r'^get-student-detail/$', views.get_student, name="get_student"),
    url(r'^assign-book-to-student/$', views.assign_book_to_student, name="assign_book_to_student"),
    url(r'^assign-bookunit/$', views.assign_bookunit, name='assign_bookunit'),
    url(r'^history/$', views.view_borrow_history, name='view_borrow_hisory'),

]
