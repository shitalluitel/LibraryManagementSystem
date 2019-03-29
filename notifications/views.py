from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
from notifications.models import Notification

@login_required
def notifications(request):
    user = request.user
    context = {}

    notifications = Notification.objects.filter(user=user)

    context['notifications'] = notifications
    return render(request, 'notifications/list.html', context)
