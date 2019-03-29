from django.contrib import messages
from django.contrib.auth.decorators import permission_required, login_required
from django.db import transaction, IntegrityError
from django.forms import modelformset_factory
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from routines.forms import RoutineDataForm, RoutineCourseBatchForm
from routines.models import Routine


@permission_required('routines.add_routine', raise_exception=True)
def routine_create(request):
    context = {}

    modelfromset = modelformset_factory(Routine, form=RoutineDataForm)
    form = modelfromset(request.POST or None, queryset=Routine.objects.none(), prefix='routine')

    course_form = RoutineCourseBatchForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid() and course_form.is_valid():
            try:
                with transaction.atomic():
                    course_data = course_form.cleaned_data
                    course = course_data.get('course')
                    batch = course_data.get('batches')
                    sem = course_data.get('semester')

                    for data in form.forms:
                        routine = data.save(commit=False)
                        print(routine.time_from)
                        routine.course = course
                        routine.batches = batch
                        routine.semester = sem
                        routine.save()

                    messages.success(request, 'Successfully created routine.')
                    return redirect('routines:create')
            except IntegrityError as e:
                print(e)
                messages.error(request, e)

    context['formset'] = form
    context['form'] = course_form
    return render(request, 'routines/create.html', context)


@login_required
def routine_list(request):
    context = {}
    form = RoutineCourseBatchForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            data = form.cleaned_data
            course = data.get('course')
            batch = data.get('batches')
            sem = data.get('semester')

            routine = Routine.objects.filter(course=course, batches=batch, semester=sem, is_deleted=False)

            context['datas'] = routine
            context['form'] = form
            return render(request, 'routines/list.html', context)
    context['form'] = form
    return render(request, 'routines/list.html', context)


@permission_required('routines.change_routine', raise_exception=True)
def routine_edit(request):
    context = {}

    query_data = request.GET
    course = query_data.get('course')
    batch = query_data.get('batch')
    sem = query_data.get('sem')

    datas = Routine.objects.filter(course=course, batches=batch, semester=sem, is_deleted=False)

    count = datas.count()

    if count > 0:
        modelfromset = modelformset_factory(Routine, form=RoutineDataForm, extra=0)
        form = modelfromset(request.POST or None,
                            queryset=datas, prefix='routine')

        course_form = RoutineCourseBatchForm(data=request.POST or None,
                                             instance=datas.first())

        if request.method == "POST":
            if form.is_valid() and course_form.is_valid():
                try:
                    with transaction.atomic():
                        course_data = course_form.cleaned_data
                        course = course_data.get('course')
                        batch = course_data.get('batches')
                        sem = course_data.get('semester')

                        for data in form.forms:
                            if len(data.cleaned_data.values()) > 0:
                                if data.cleaned_data['id']:
                                    routine_data = data.cleaned_data['id']
                                    routine_data.day = data.cleaned_data['day']
                                    routine_data.time_from = data.cleaned_data['time_from']
                                    routine_data.time_to = data.cleaned_data['time_to']
                                    routine_data.teacher = data.cleaned_data['teacher']
                                    routine_data.subject = data.cleaned_data['subject']
                                    routine_data.course = course
                                    routine_data.batches = batch
                                    routine_data.semester = sem
                                    routine_data.save()
                                else:
                                    routine_data = data.save(commit=False)
                                    routine_data.course = course
                                    routine_data.batches = batch
                                    routine_data.semester = sem
                                    routine_data.save()

                        messages.success(request, 'Successfully created routine.')
                        return redirect('routines:create')
                except IntegrityError as e:
                    print(e)
                    messages.error(request, e)
    else:
        messages.error(request, "Unable to find routine to edit.")
        return redirect('routines:list')

    context['course'] = course
    context['batch'] = batch
    context['sem'] = sem

    context['formset'] = form
    context['form'] = course_form
    return render(request, 'routines/edit.html', context)


@permission_required('routines.delete_routine', raise_exception=True)
def routine_delete(request):
    context = {}

    query_data = request.GET
    course = query_data.get('course')
    batch = query_data.get('batch')
    sem = query_data.get('sem')

    datas = Routine.objects.filter(course=course, batches=batch, semester=sem)

    try:
        with transaction.atomic():
            for data in datas:
                data.is_deleted = True
                data.save()
    except IntegrityError as e:
        messages.error(request, e)

    return redirect('routines:list')


@permission_required('routines.delete_routine', raise_exception=True)
def unit_routine_delete(request, pk):
    next = request.GET.get('next')
    try:
        data = Routine.objects.get(pk=pk)
        data.delete()
    except Exception as e:
        print(e)
        # return HttpResponse({'error': e}, content_type='application/json', status=204)
    return redirect(next)

    # return HttpResponse({'message': 'Successfully Deleted.'}, content_type='application/json', status=200)
