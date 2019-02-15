from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.db import transaction
from django.shortcuts import render, redirect
from datetime import datetime
# Create your views here.
from books.models import BookUnit
from borrows.models import Borrow


@transaction.atomic
@permission_required('books.order_bookunit', raise_exception=True)
def order_bookunit(request, pk):
    try:
        data = BookUnit.objects.get(id=pk)
    except BookUnit.DoesNotExist:
        messages.warning(request, 'Unable to order book.')
        return redirect("books:list_book_unit", pk=data.book.id)
    if data.is_available:
        data.status = 'pending'
        data.save()

        borrow = Borrow()
        student = request.user.students.first()
        borrow.student = student
        borrow.book_unit = data
        borrow.status = 'pending'
        borrow.save()

        return redirect("books:list_book_unit", pk=data.book.id)

    messages.error(request, 'This unit of book is unavailable. Please try again later.')
    return redirect("books:list_book_unit", pk=data.book.id)


@permission_required('borrows.view_borrow', raise_exception=True)
def list_borrow(request):
    context = {}
    datas = Borrow.objects.filter(status='pending')

    context['datas'] = datas

    return render(request, 'borrows/list.html', context)


@transaction.atomic
@permission_required('books.assign_bookunit', raise_exception=True)
def assign_bookunit(request, pk):
    try:
        data = Borrow.objects.get(id=pk)
    except Borrow.DoesNotExist:
        messages.error(request, 'Unable to find data.')
        return render('books:')

    data.status = 'approved'
    data.issued_date = datetime.now()
    data.save()

    book = data.book_unit
    book.status = 'booked'
    book.save()

    messages.success(request, 'Successfully assigned')
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
    data.issued_date = datetime.now()
    data.save()

    book = data.book_unit
    book.status = 'available'
    book.save()

    messages.success(request, 'Successfully assigned')
    return redirect('borrows:list_borrow')
