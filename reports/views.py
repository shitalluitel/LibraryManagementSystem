from django.contrib import messages
from django.shortcuts import render, redirect

# Create your views here.
from LibraryManagementSystem.utils import render_pdf
from borrows.models import Borrow
from reports.forms import BookReportForm, StudentReportForm


def report_home(request):
    return render(request, 'reports/report_home.html')


def book_order_report(request):
    context = {}
    form = BookReportForm(data=request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            form_data = form.data
            start_date = form_data.get('start_date')
            end_date = form_data.get('end_date')
            status = form_data.get('status')

            datas = Borrow.objects.all()

            if start_date and end_date:
                datas = datas.filter(created_at__range=[start_date, end_date])
                form.start_date = start_date
                form.end_date = end_date

            if status:
                datas = datas.filter(status=status)
                form.status = status

            form = BookReportForm(initial={
                'start_date': start_date,
                'end_date': end_date,
                'status': status,
            }, auto_id=False)
            context['datas'] = datas

    print(form)
    context['form'] = form
    return render(request, 'reports/book_order_report.html', context)


def student_report(request):
    context = {}
    forms = StudentReportForm(request.POST or None)
    context['forms'] = forms
    if request.method == 'POST':
        if forms.is_valid():
            form_data = forms.data

            course = form_data.get('course')
            batch = form_data.get('batch')
            student = form_data.get('student')

            datas = Borrow.objects.filter(status="returned")
            context['batch'] = False
            context['student'] = False
            if course:
                datas = datas.filter(student__course_batch__course_id=course)

            if batch:
                datas = datas.filter(student__course_batch__batch_id=batch)
                batch = datas.first()
                context['batch'] = batch.student.course_batch.batch_id

            if student:
                datas = datas.filter(student__roll_no=student)
                data = datas.first()
                context['student'] = data.student.roll_no

            context['datas'] = datas
        print(forms.errors)
    return render(request, 'reports/student_report.html', context)


def export_pdf(request):
    context = {}
    type_of_pdf = request.GET.get('type')

    if type_of_pdf.lower() == "books":
        form_data = request.POST
        print(form_data)
        start_date = form_data.get('start_date')
        end_date = form_data.get('end_date')
        status = form_data.get('status')

        datas = Borrow.objects.filter(status="returned")

        file_name = "date_filter_report"

        if start_date and end_date:
            datas = datas.filter(created_at__range=[start_date, end_date])
            file_name = start_date + "_to_" + end_date
        if status:
            datas = datas.filter(status=status)
            file_name = file_name + "_" + status

        options = {
            'quiet': '',
            'page-size': 'A4',
            'orientation': 'Portrait',
            'margin-top': '0.6in',
            'margin-right': '0.6in',
            'margin-bottom': '0.6in',
            'margin-left': '0.6in',
            'encoding': 'UTF-8',
        }
        context['datas'] = datas
        context['title'] = 'Date Filter Report'
        context['sub_title'] = file_name.replace('_', " ").capitalize()
        file_name = file_name + ".pdf"
        return render_pdf('reports/student_report_pdf.html', context, file_name, options)

    elif type_of_pdf.lower() == 'student':
        student_data = request.POST
        course = student_data.get('course')
        batch = student_data.get('batch')
        student = student_data.get('student')

        datas = Borrow.objects.filter(status="returned")
        file_name = "student_report"
        if course:
            datas = datas.filter(student__course_batch__course_id=course)
            file_name = datas.first().student.course_batch.course.name + "_report"

        if batch:
            datas = datas.filter(student__course_batch__batch_id=batch)
            file_name = datas.first().student.course_batch.batch.name + "_report"

        if student:
            datas = datas.filter(student__roll_no=student)
            file_name = datas.first().student.roll_no + "_report"

        options = {
            'quiet': '',
            'page-size': 'A4',
            'orientation': 'Portrait',
            'margin-top': '0.6in',
            'margin-right': '0.6in',
            'margin-bottom': '0.6in',
            'margin-left': '0.6in',
            'encoding': 'UTF-8',
        }
        context['datas'] = datas
        context['title'] = "Student's Report"
        context['sub_title'] = file_name.replace('_', " ").capitalize()
        file_name = file_name + ".pdf"
        return render_pdf('reports/student_report_pdf.html', context, file_name, options)
    else:
        messages.error(request, 'Unable to generate report. Please try it again.')

    return redirect('reports:home')
