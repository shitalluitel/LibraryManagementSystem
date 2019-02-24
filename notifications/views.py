from django.shortcuts import render

# Create your views here.
from notifications.models import Notification


def notifications(request):
    user = request.user
    context = {}

    notifications = Notification.objects.filter(user=user)

    context['notifications'] = notifications
    return render(request, 'notifications/list.html', context)
