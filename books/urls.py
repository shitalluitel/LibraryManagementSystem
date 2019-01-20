from django.conf.urls import url
from . import views

app_name = "books"

urlpatterns = [
    url(r'^$', views.list_book, name="book_list"),
    url('^create/json/$', views.create_json, name="create_json"),
    url(r'^json/list/$', views.json_list, name="json_list_book"),
    url(r'^create/$', views.create_book, name="book_create"),
]
