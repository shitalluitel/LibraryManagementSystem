from django.forms import modelformset_factory
from django.shortcuts import render, redirect, reverse

# Create your views here.
from settings.models import CourseBatch
from students.forms import CreateChoiceForm, StudentCreateForm
from students.models import Student


#
# def create_choice(request):
#     context = {}
#     form = CreateChoiceForm(request.POST or None)
#
#     if request.method == "POST":
#         if form.is_valid():
#             course = form.cleaned_data.get('course')
#             batch = form.cleaned_data.get('batch')
#             course_batch = CourseBatch.objects.get(course=course, batch=batch)
#             print(course_batch)
#             pass
#
#     context['form'] = form
#     return render(request, 'students/select_course_batch.html', context)


def create_student(request):
    context = {}

    form = CreateChoiceForm(request.POST or None)
    modelfromset = modelformset_factory(Student, form=StudentCreateForm)
    student_formset = modelfromset(request.POST or None, request.FILES or None, queryset=Student.objects.none(),
                                   prefix='student')
    # form = StudentCreateForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid() and student_formset.is_valid():
            course = form.cleaned_data.get('course')
            batch = form.cleaned_data.get('batch')
            course_batch = CourseBatch.objects.get(course=course, batch=batch)

            for student_form in student_formset.forms:
                student = student_form.save(commit=False)
                student.course_batch = course_batch
                student.save()

            return redirect('students:create_student')
        else:
            print("{}, {}".format(form.errors, student_formset.errors))

    context['form'] = form
    context['formset'] = student_formset
    return render(request, 'students/create.html', context)


def list_student(request):
    context = {}
    form = CreateChoiceForm(request.POST or None)
    context['form'] = form

    return render(request, 'students/list_student.html', context)


def json_list_student(request):
    data = request.POST
    print(data.get('course'))
    print(data.get('batch'))
    pass
