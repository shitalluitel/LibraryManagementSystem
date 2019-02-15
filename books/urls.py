from django.conf.urls import url
from . import views

app_name = "books"

urlpatterns = [
    url(r'^$', views.list_book, name="book_list"),
    url(r'^trash/$', views.book_trash, name="book_trash"),
    url('^create/json/$', views.create_json, name="create_json"),
    url(r'^json/list/$', views.json_list, name="json_list_book"),
    url(r'^json/trash/$', views.json_trash, name="json_trash_book"),
    url(r'^create/$', views.create_book, name="book_create"),
    url(r'^edit/(?P<pk>\d+)/$', views.edit_book, name="edit_book"),
    url(r'^delete/(?P<pk>\d+)/$', views.delete_book, name="delete_book"),
    url(r'^undo/(?P<pk>\d+)/$', views.undo_book, name="undo_book"),
    url(r'^book-units/(?P<pk>\d+)/$', views.list_book_unit, name="list_book_unit"),
    url(r'^book-units/json/(?P<pk>\d+)/$', views.list_book_unit_json, name="list_book_unit_json"),
    url(r'^create/book-units/(?P<pk>\d+)/$', views.create_book_units, name="create_book_units"),
    url(r'^json/create/book-units/(?P<pk>\d+)/$', views.create_book_units_json, name="create_book_units_json"),
    url(r'^delete/book-units/(?P<pk>\d+)/$', views.delete_book_units, name="delete_book_units"),
    # url(r'^order/(?P<pk>\d+)$', views.order_bookunit, name="order_bookunit"),
]
