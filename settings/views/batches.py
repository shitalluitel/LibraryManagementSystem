import json

from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import transaction, IntegrityError
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse

from settings.models import Batch, CourseBatch
from settings.forms import BatchForm, CourseBatchCreateForm


def create(request):
    context = {}
    form = BatchForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            try:
                with transaction.atomic():
                    batch = form.save()
                    # messages.success(request, "Successfully created '{}' batch".format(batch.name))
                    return redirect("batches:course_batch", pk=batch.id)
            except IntegrityError:
                messages.error(request, 'Unable to save this record.')
                return redirect('batches:create')

    context['form'] = form
    return render(request, 'batches/create.html', context)


def create_json(request):
    context = {}
    form = BatchForm(None)
    if request.method == 'POST':
        form = BatchForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    batch = form.save()
                    # messages.success(request, "Successfully created '{}' batch".format(batch.name))
                    return redirect("batches:course_batch", pk=batch.id)
            except IntegrityError:
                messages.error(request, 'Unable to save this record.')
                return redirect('batches:create')
        else:
            return create(request=request)
    context['form'] = form
    return render(request, 'batches/_form.html', context)


def edit(request, pk):
    context = {}
    try:
        data = Batch.objects.get(id=pk)
    except Batch.DoesNotExist:
        messages.warning(request, 'Unable to find data that you have requested.')
        return redirect("batches:list")

    form = BatchForm(request.POST or None, instance=data)

    if request.method == "POST":
        if form.is_valid():
            batch = form.save()
            messages.success(request, "Successfully updated '{}' batch".format(batch.name))
            return redirect("batches:list")

    context['form'] = form
    return render(request, 'batches/create.html', context)


def list(request):
    # context = {}
    # datas = Batch.objects.all()
    # context['datas'] = datas
    return render(request, 'batches/list.html')


def json_list(request):
    datas = Batch.objects.all()

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
            data = Batch.objects.get(pk=pk)
            data.delete()
            # data.is_deleted = False
            # data.save()
        except Batch.DoesNotExist:
            messages.error(request, "Unable to find data that you have requested.")
            return redirect('batches:list')

        messages.success(request, "Successfully deleted {}.".format(data.name))
        return redirect('batches:list')

    context['next'] = reverse('batches:list')
    context['page_name'] = "Batch"
    return render(request, 'snippets/delete.html', context)


def create_course_batch(request, pk):
    form = CourseBatchCreateForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            try:
                with transaction.atomic():
                    for course in form.cleaned_data.get('course'):
                        course_batch = CourseBatch()
                        course_batch.course = course
                        course_batch.batch_id = pk
                        course_batch.save()
                    return redirect('batches:list')
            except IntegrityError:
                print('integrity error')
                return redirect('batches:course_batch', pk=pk)

    return render(request, 'batches/course_batch_create.html', {'form': form})


def get_batch_list(request, pk):
    batch = Batch.objects.filter(course__id=pk)
    empty_label = "Batch"
    return render(request, 'snippets/option.html', {'datas': batch, 'empty_label': empty_label})
