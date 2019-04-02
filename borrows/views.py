import json

from django.contrib import messages
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.models import Group, User
from django.db import transaction
from django.db.models import Q, Count
from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse
from datetime import datetime
# Create your views here.
from notifications.signals import notify

from books.models import BookUnit
from borrows.forms import SelectStudentForm, AssignBookForm
from borrows.models import Borrow
from fines.models import Fine
from students.models import Student


@transaction.atomic
@permission_required('books.order_bookunit', raise_exception=True)
def order_bookunit(request, pk):
    student = request.user.student
    borrow = student.borrows.filter(Q(status='approved') | Q(status='pending')).count()

    if borrow < request.books_allowed:
        try:
            data = BookUnit.objects.get(id=pk)
        except BookUnit.DoesNotExist:
            messages.warning(request, 'Unable to order book.')
            return redirect("books:list_book_unit", pk=data.book.id)

        if data.is_available:
            data.status = 'pending'
            data.save()

            borrow = Borrow()
            borrow.student = student
            borrow.book_unit = data
            borrow.status = 'pending'
            borrow.save()

            group = Group.objects.get(name__icontains='staff')

            notify.send(sender=request.user, recipient=group,
                        verb='Book order by ' + request.user.get_full_name(),
                        description="Book with Acc. No. {} has been ordered by {}.".format(data.acc_no,
                                                                                           request.user.get_full_name()))

            return redirect("books:list_book_unit", pk=data.book.id)

        messages.error(request, 'This unit of book is unavailable. Please try again later.')
    else:
        messages.warning(request, 'Book unit threshold reached.')
        return redirect('books:book_list')
    return redirect("books:list_book_unit", pk=data.book.id)


@permission_required('borrows.view_borrow', raise_exception=True)
def list_borrow(request):
    context = {}
    datas = Borrow.objects.filter(status='pending')

    context['datas'] = datas
    context['approved'] = False
    return render(request, 'borrows/list.html', context)


@permission_required('borrows.view_borrow', raise_exception=True)
def list_approved_borrow(request):
    context = {}
    datas = Borrow.objects.filter(status='approved')

    context['datas'] = datas
    context['approved'] = True
    return render(request, 'borrows/list.html', context)


@transaction.atomic
@permission_required('books.assign_bookunit', raise_exception=True)
def assign_borrow_bookunit(request, pk):
    try:
        data = Borrow.objects.get(id=pk)
    except Borrow.DoesNotExist:
        messages.error(request, 'Unable to find data.')
        return render('books:')

    data.status = 'approved'
    data.user = request.user
    data.issued_date = datetime.now()
    data.save()

    book = data.book_unit
    book.status = 'booked'
    book.save()

    messages.success(request, 'Successfully approved book unit {} to {}.'.format(book.book_code, data.student))
    return redirect('borrows:list_borrow')


@transaction.atomic
@permission_required('books.assign_bookunit', raise_exception=True)
def cancel_request(request, pk):
    try:
        data = Borrow.objects.get(id=pk)
    except Borrow.DoesNotExist:
        messages.error(request, 'Unable to find data.')
        return render('books:')

    data.status = 'cancelled'
    data.user = request.user
    data.issued_date = datetime.now()
    data.save()

    book = data.book_unit
    book.status = 'available'
    book.save()

    notify.send(sender=request.user, recipient=data.student.user,
                verb='Book order cancelled',
                description="Your Order of book with Acc. No. {} has been cancelled by {}.".format(data.book_unit.acc_no,
                                                                                                   request.user.get_full_name()))

    messages.success(request, 'Successfully cancelled')
    return redirect('borrows:list_borrow')


@transaction.atomic
@permission_required('books.assign_bookunit', raise_exception=True)
def return_borrow_book(request, pk):
    context = {}
    try:
        data = Borrow.objects.get(pk=pk, status='approved')
    except:
        messages.error(request, 'Unable to find data.')
        return redirect('borrows:list_approved_borrow')

    if request.method == "POST":
        book = data.book_unit
        book.status = 'available'
        book.save()

        issued_date = data.issued_date
        # return_date = data.return_date
        today = datetime.now().date()

        fine_days = (today - issued_date).days - request.renew_days

        fine_amount = 0

        if fine_days > 0:
            fine_amount = fine_days * request.fine_amount

        data.return_date = today
        data.status = 'returned'
        data.save()

        fine, created = Fine.objects.get_or_create(student=data.student)

        if created:
            fine.amount = fine_amount
        else:
            fine.amount = fine.amount + fine_amount

        fine.save()

        messages.success(request, 'Book Returned Successfully.')
        return redirect('borrows:list_approved_borrow')

    context['data'] = data
    context['next'] = reverse('borrows:list_approved_borrow')
    return render(request, 'borrows/detail.html', context)


@transaction.atomic
@permission_required('books.assign_bookunit', raise_exception=True)
def return_bookunit(request, pk):
    context = {}
    try:
        book = BookUnit.objects.get(id=pk)
    except BookUnit.DoesNotExist:
        messages.error(request, "Unable to fine data")
        return redirect('books:list_book_unit')

    data = book.borrows.filter(status='approved').first()

    if request.method == "POST":
        book.status = 'available'
        book.save()

        issued_date = data.issued_date
        # return_date = data.return_date
        today = datetime.now().date()

        fine_days = (today - issued_date).days - request.renew_days
        fine_amount = 0

        if fine_days > 0:
            fine_amount = fine_days * request.fine_amount

        fine, created = Fine.objects.get_or_create(student=data.student)

        if created:
            fine.amount = fine_amount
        else:
            fine.amount = fine.amount + fine_amount

        fine.save()

        data.return_date = today
        data.status = 'returned'
        data.save()

        messages.success(request, 'Book Returned Successfully.')
        return redirect('books:list_book_unit', pk=book.book_id)

    context['data'] = data
    context['next'] = reverse('books:list_book_unit', kwargs={'pk': book.book_id})
    return render(request, 'borrows/detail.html', context)


def select_student(request):
    pass


@permission_required('students.view_student')
def get_student(request):
    context = {}
    form = SelectStudentForm(request.POST or None)
    book = request.GET.get('book')

    if request.method == 'POST':
        if book:
            if form.is_valid():
                roll_no = form.cleaned_data.get('student')
                try:
                    data = Student.objects.get(roll_no__iexact=roll_no)
                except Student.DoesNotExist:
                    messages.error(request, 'Unable to find student.')
                    return redirect('borrows:get_student')

                borrows = data.borrows.filter(Q(status='approved'))
                book_count = borrows.count()

                if book_count < 3:
                    fine = Fine.objects.filter(student=data).first()
                    if fine:
                        total_fine = fine.amount
                    else:
                        total_fine = 0
                    context['data'] = data
                    context['borrow_details'] = borrows
                    context['remaining_fine'] = total_fine
                    context['form'] = form
                    return render(request, 'borrows/view_detail_student.html', context)
                messages.warning(request, 'Book threshold reached.')
        else:
            messages.warning(request, "Please select book first.")
            return redirect('books:book_list')

    context['form'] = form
    return render(request, 'borrows/view_student.html', context)


@transaction.atomic
@permission_required('books.assign_bookunit')
def assign_book_to_student(request):
    book = request.GET.get('book')
    student = request.GET.get('student')

    try:
        book_data = BookUnit.objects.get(acc_no__iexact=book, status='available')
    except BookUnit.DoesNotExist:
        messages.warning(request, 'Book not found.')
        return redirect('books:book_list')

    try:
        student_data = Student.objects.get(roll_no__iexact=student)
        book_count = student_data.borrows.filter(status='approved').count()
    except Student.DoesNotExist:
        messages.warning(request, 'Student not found.')
        return redirect('books:book_list')

    if book_count < request.books_allowed:
        book_data.status = 'booked'
        book_data.save()

        borrow = Borrow()
        borrow.student = student_data
        borrow.book_unit = book_data
        borrow.user = request.user
        borrow.issued_date = datetime.now()
        borrow.status = 'approved'
        borrow.save()
        messages.success(request, '{} assigned to {}.'.format(book_data, student))
    else:
        messages.warning(request, 'Book threshold reached.')

    return redirect('books:book_list')


@transaction.atomic
@permission_required('books.assign_bookunit')
def assign_bookunit(request):
    context = {}
    form = AssignBookForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid:
            data = form.data
            book_id = data.get('book_unit')
            roll_no = data.get('student')
            try:
                book_unit = BookUnit.objects.get(id=int(book_id))
            except BookUnit.DoesNotExist:
                messages.error(request, 'Unable to find book.')
                return redirect('borrows:assign_bookunit')
            try:
                student = Student.objects.get(roll_no__iexact=roll_no)
                book_count = student.borrows.filter(status='approved').count()
            except Student.DoesNotExist:
                messages.error(request, 'Unable to find student.')
                return redirect('borrows:assign_bookunit')

            if book_count < request.books_allowed:
                book_unit.status = 'booked'
                book_unit.save()

                borrow = Borrow()
                borrow.student = student
                borrow.book_unit = book_unit
                borrow.user = request.user
                borrow.issued_date = datetime.now()
                borrow.return_date = datetime.now()
                borrow.status = 'approved'
                borrow.save()

                messages.success(request, '{} assigned to {}.'.format(book_unit, student))
                return redirect('borrows:assign_bookunit')
            else:
                messages.warning(request, 'Book threshold reached.')

    context['form'] = form
    return render(request, 'borrows/assign_bookunit.html', context)


# @permission_required('borrows.view_history')
@login_required
def view_borrow_history(request):
    context = {}
    student = request.user.student
    status = request.GET.get('status')

    history = None
    if status == 'approved':
        history = Borrow.objects.filter(student=student, status='approved')
        context['history'] = False
    elif not status:
        history = Borrow.objects.filter(student=student, status='returned')
        context['history'] = True

    context['datas'] = history
    context['remaining_fine'] = Fine.objects.filter(student=student).first()
    return render(request, 'borrows/history.html', context)


@login_required
def display_pie_chart(request):
    fieldname = 'book_unit__book__name'
    borrows = Borrow.objects.filter(Q(status='returned') | Q(status='approved')).values(fieldname).order_by(
        fieldname).annotate(
        count=Count(fieldname))[:10]
    labels = []
    data = []
    return_data = {}
    json_array = []
    for borrow in borrows:
        labels.append(borrow.get('book_unit__book__name'))
        data.append(borrow.get('count'))

    return_data['data'] = data
    return_data['labels'] = labels
    # json_array.append(return_data)
    json_data = json.dumps(return_data)
    return HttpResponse(json_data, content_type='application/json')
