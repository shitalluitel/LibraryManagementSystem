from django.conf.urls import url, include
from settings.views import settings as views

app_name = "settings"

urlpatterns = [
    url('^$', views.setting, name="setting"),
]
