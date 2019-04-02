import json

from django.contrib import messages
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.models import Group
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from notifications.signals import notify

from notices.forms import NoticeForm
from notices.models import Notice


@permission_required('notices.add_notice', raise_exception=True)
def notice_upload(request):
    context = {}
    form = NoticeForm()
    if request.method == "POST":
        form = NoticeForm(request.POST or None)
        if form.is_valid():
            notice = form.save(commit=False)
            notice.save()

            group = Group.objects.get(name__icontains='student')

            notify.send(sender=request.user, recipient=group,
                        verb=notice.title,
                        description=notice.title
                        )

            messages.success(request, "Successfully uploaded notice.")
            return redirect('notices:notice_upload')
    context['form'] = form
    return render(request, 'notices/upload.html', context)


@permission_required('notices.change_notice', raise_exception=True)
def notice_update(request, pk):
    context = {}
    next = request.GET.get('next')

    try:
        data = Notice.objects.get(pk=pk)
    except:
        messages.error(request, "Unable to find notice.")
        return redirect(next)

    form = NoticeForm(instance=data)
    if request.method == "POST":
        form = NoticeForm(request.POST or None, instance=data)
        if form.is_valid():
            notice = form.save(commit=False)
            notice.save()

            messages.success(request, "Successfully uploaded notice.")
            return redirect('notices:notice_update', pk=notice.pk)
    context['form'] = form
    return render(request, 'notices/upload.html', context)


@login_required
def notice_home(request):
    return render(request, 'notices/notice_home.html')


@login_required
def notice_list(request):
    context = {}

    # type = request.GET.get('type')
    # type = type.capitalize()

    notice = Notice.objects.filter(is_deleted=False)

    context['datas'] = notice
    context['type'] = type
    # context['next'] = reverse('notices:notice_list') + '?type=' + type

    return render(request, 'notices/notice_list.html', context)


@permission_required('notices.delete_notice', raise_exception=True)
def notice_delete(request, pk):
    next = request.GET.get('next')

    try:
        notice = Notice.objects.get(pk=pk)
        notice.is_deleted = True
        messages.success(request, "Successfully deleted the notice.")
    except Exception as e:
        messages.error(request, e)

    return redirect(next)


@login_required
def notice_detail(request, pk):
    next = request.GET.get('next')

    try:
        data = Notice.objects.get(pk=pk)
        resopnse_data = {'title': data.title, 'notice': data.notice}
    except Notice.DoesNotExist as e:
        resopnse_data = {'error': 'Doesnot Exist'}
        # return HttpResponse(json.dumps(resopnse_data), content_type='application/json', status=404)

    return HttpResponse(json.dumps(resopnse_data), content_type='application/json', status=200)
