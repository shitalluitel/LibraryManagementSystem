from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.models import Group
from django.db import IntegrityError, transaction
from django.forms import modelformset_factory
from django.shortcuts import render, redirect, reverse

# Create your views here.
from settings.models import CourseBatch
from students.forms import CreateChoiceForm, StudentCreateForm
from students.models import Student


@login_required
@permission_required('students.add_student', raise_exception=True)
def create_student(request):
    context = {}

    form = CreateChoiceForm(request.POST or None)
    modelfromset = modelformset_factory(Student, form=StudentCreateForm)
    student_formset = modelfromset(request.POST or None, request.FILES or None, queryset=Student.objects.none(),
                                   prefix='student')
    # form = StudentCreateForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid() and student_formset.is_valid():
            try:
                with transaction.atomic():
                    course = form.cleaned_data.get('course')
                    batch = form.cleaned_data.get('batch')
                    course_batch = CourseBatch.objects.get(course=course, batch=batch)

                    for student_form in student_formset.forms:
                        student = student_form.save(commit=False)
                        student.course_batch = course_batch
                        student.save()

                        user = student.user
                        group = Group.objects.get(name__iexact='student')
                        user.groups.add(group)
                    return redirect('students:create_student')
            except IntegrityError():
                pass

        else:
            print("{}, {}".format(form.errors, student_formset.errors))

    context['form'] = form
    context['formset'] = student_formset
    return render(request, 'students/create.html', context)


@login_required
@permission_required('students.view_student', raise_exception=True)
def list_student(request):
    context = {}
    form = CreateChoiceForm(request.POST or None)
    context['form'] = form
    if request.method == 'POST':
        if form.is_valid():
            data = form.cleaned_data
            course = data.get('course')
            batch = data.get('batch')
            print(type(course))
            print(type(batch))
            student = Student.objects.filter(course_batch__batch=batch, course_batch__course_id=course)
            context['datas'] = student
            return render(request, 'students/list_student.html', context)

    return render(request, 'students/select_course_batch.html', context)


@login_required
@permission_required('students.view_student', raise_exception=True)
def json_list_student(request):
    data = request.POST
    print(data.get('course'))
    print(data.get('batch'))
    pass

# @login_required
# @permission_required('students.view_student', raise_exception=True)
# def detail_student(request, pk):
#     try:
#         data = Student.objects.get()
