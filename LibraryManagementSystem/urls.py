"""LibraryManagementSystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from borrows.views import display_pie_chart

urlpatterns = [
                  url(r'^admin/', admin.site.urls),
                  url(r'^', include('pages.urls')),
                  url(r'^batches/', include('settings.urls.batches')),
                  url(r'^books/', include('books.urls')),
                  url(r'^borrows/', include('borrows.urls')),
                  url(r'^courses/', include('settings.urls.courses')),

                  url(r'^ckeditor/', include('ckeditor_uploader.urls')),

                  url(r'^fines/', include('fines.urls')),
                  url(r'^files/', include('files.urls')),
                  url(r'^get-chart-data/$', display_pie_chart, name='get_chart_data'),
                  url(r'^groups/', include('settings.urls.groups')),

                  url('^inbox/notifications/', include('notifications.urls', namespace='notifications')),

                  url(r'^notices/', include('notices.urls')),
                  url(r'^reports/', include('reports.urls')),
                  url(r'^routines/', include('routines.urls')),
                  url(r'^settings/', include('settings.urls.settings')),
                  url(r'^students/', include('students.urls')),
                  url(r'^users/', include('users.urls')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'LibraryManagementSystem.views.handler404'
handler500 = 'LibraryManagementSystem.views.handler500'
