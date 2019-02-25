from datetime import datetime
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

# Create your views here.
from books.models import BookUnit
from borrows.models import Borrow
from fines.models import Fine
from django.db.models import Sum


@login_required
def home_page(request):
    try:
        group = request.user.groups.get()
        group_name = group.name
    except:
        group_name = 'admin'

    if group_name.lower() == 'student':
        return student_dashboard(request=request)
    elif group_name.lower() == 'admin':
        # return redirect('student_dashboard')
        pass
    elif group_name.lower() == 'staff':
        return staff_dashboard(request=request)


def student_dashboard(request):
    user = request.user
    student = user.student
    context = {}
    total_fine = 0

    remaining_fine = student.fine
    borrowed_books = student.borrows.filter(status='approved')[:5]
    borrow_history = student.borrows.filter(status='returned')[:5]

    for data in borrowed_books:
        issued_date = data.issued_date
        today = datetime.now().date()

        fine_days = (today - issued_date).days - request.renew_days

        fine_amount = 0

        if fine_days > 0:
            fine_amount = fine_days * request.fine_amount

        total_fine = total_fine + fine_amount

    context['remaining_fine'] = remaining_fine
    context['borrowed_books_count'] = borrowed_books.count()
    context['borrowed_books'] = borrowed_books
    context['estimated_total_fine'] = total_fine
    context['borrowed_history'] = borrow_history

    return render(request, 'pages/_student_dashboard.html', context)


def staff_dashboard(request):
    user = request.user
    context = {}
    ordered_book_list = Borrow.objects.filter(status='ordered')
    ordered_books = ordered_book_list.count()
    no_of_books = BookUnit.objects.count()

    total_fine = Fine.objects.aggregate(Sum('amount'))['amount__sum']

    context['no_of_books'] = no_of_books
    context['ordered_books'] = ordered_books
    context['total_fine'] = total_fine
    context['borrowed_books'] = ordered_book_list
    return render(request, 'pages/_staff_dashboard.html', context)
