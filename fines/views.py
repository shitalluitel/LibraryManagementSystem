from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import permission_required, login_required
from django.shortcuts import render, redirect

# Create your views here.
from borrows.models import Borrow
from fines.forms import FineStudentForm, FineForm
from fines.models import Fine
from students.models import Student


@permission_required('fines.change_fine', raise_exception=True)
def get_student_fine(request):
    context = {}
    student_form = FineStudentForm(request.POST or None)

    if request.method == 'POST':
        if student_form.is_valid():
            roll_no = student_form.cleaned_data.get('student')
            return redirect('fines:pay_fine', roll_no=roll_no)

    context['student_form'] = student_form
    return render(request, 'fines/get_student_fine.html', context)


@permission_required('fines.change_fine', raise_exception=True)
def pay_fine(request, roll_no):
    context = {}
    try:
        student = Student.objects.get(roll_no__iexact=roll_no)
    except Student.DoesNotExist:
        messages.error(request, 'Unable to find the student with this roll no.')
        return redirect('fines:get_student_fine')

    try:
        fine = Fine.objects.get(student=student)
    except Fine.DoesNotExist:
        messages.error(request, "Student doesn't have any fine amount.")
        return redirect('fines:get_student_fine')

    if not fine.amount <= 0:
        fine_form = FineForm(request.POST or None, instance=fine)

        if request.method == "POST":
            if fine_form.is_valid():
                pay_amount = fine_form.cleaned_data.get('pay_amount')
                fine.amount = fine.amount - pay_amount
                fine.save()

                messages.success(request, 'Successfully paid. Remaining fine is Rs. {}.'.format(fine.amount))
                return redirect('fines:get_student_fine')

        context['fine_form'] = fine_form
        context['student'] = student
    else:
        messages.error(request, "Student doesn't have any fine amount.")
        return redirect('fines:get_student_fine')

    return render(request, 'fines/pay_fine.html', context)


@login_required
def list_fine(request):
    context = {}
    borrows = Borrow.objects.filter(status='approved')
    total_fine = 0

    for data in borrows:
        issued_date = data.issued_date
        today = datetime.now().date()

        fine_days = (today - issued_date).days - request.renew_days

        fine_amount = 0

        if fine_days > 0:
            fine_amount = fine_days * request.fine_amount

        total_fine = total_fine + fine_amount

    context['borrows'] = borrows
    context['total_fine'] = total_fine
    return render(request, 'fines/list_fine.html', context)
