import json

from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse
from settings.models import Course
from settings.forms import CourseForm


def create(request):
    context = {}
    form = CourseForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            batch = form.save()
            messages.success(request, "Successfully created '{}' batch".format(batch.name))
            return redirect("courses:create")

    context['form'] = form
    return render(request, 'courses/create.html', context)


def create_json(request):
    context = {}
    form = CourseForm(None)
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            batch = form.save()
            messages.success(request, "Successfully created '{}' batch".format(batch.name))
            return redirect("courses:list")
        else:
            return create(request=request)
    context['form'] = form
    return render(request, 'courses/_form.html', context)


def edit(request, pk):
    context = {}
    try:
        data = Course.objects.get(id=pk)
    except Course.DoesNotExist:
        messages.warning(request, 'Unable to find data that you have requested.')
        return redirect("courses:list")

    form = CourseForm(request.POST or None, instance=data)

    if request.method == "POST":
        if form.is_valid():
            batch = form.save()
            messages.success(request, "Successfully updated '{}' batch".format(batch.name))
            return redirect("courses:list")

    context['form'] = form
    return render(request, 'courses/create.html', context)


def list(request):
    context = {}
    datas = Course.objects.all()
    context['datas'] = datas
    return render(request, 'courses/list.html', context)


def json_list(request):
    datas = Course.objects.all()

    q_string = request.GET.get('search[value]')

    # for search action in datatables
    # start

    lookup = Q(name__icontains=q_string) | Q(code__icontains=q_string)
    if not q_string is None:
        datas = datas.filter(lookup)

    # ends

    datas = datas.serialize()
    dict_data = json.loads(datas)

    # for pagination
    # start

    length = int(request.GET.get("length"))
    start = int(request.GET.get("start"))
    dict_data = dict_data[start: start + length]

    # ends

    context = {'data': dict_data}
    json_datas = json.dumps(context)
    return HttpResponse(json_datas, content_type='application/json', status=200)


def delete(request, pk):
    context = {}
    if request.method == "POST":
        try:
            data = Course.objects.get(pk=pk)
            data.delete()
            # data.is_deleted = False
            # data.save()
        except Course.DoesNotExist:
            messages.error(request, "Unable to find data that you have requested.")
            return redirect('courses:list')

        messages.success(request, "Successfully deleted {}.".format(data.name))
        return redirect('courses:list')

    context['next'] = reverse('courses:list')
    context['page_name'] = "Courses"
    return render(request, 'snippets/delete.html', context)
