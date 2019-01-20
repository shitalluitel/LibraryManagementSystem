import json

from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from books.forms import BookForm
from books.models import Book


def home(request):
    messages.success(request, "Yes")
    return render(request, 'page.html')


def create_book(request):
    context = {}
    form = BookForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            book = form.save()
            messages.success(request, "Book {} successfully created.".format(book.name))
            return redirect('books:book_create')

    context['form'] = form
    return render(request, 'books/create.html', context)


def create_json(request):
    context = {}
    form = BookForm(None)
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            batch = form.save()
            messages.success(request, "Successfully created '{}' batch".format(batch.name))
            return redirect("courses:list")
        else:
            return create_book(request=request)
    context['form'] = form
    return render(request, 'books/_form.html', context)


def list_book(request):
    return render(request, 'books/list.html')


def json_list(request):
    datas = Book.objects.all()

    q_string = request.GET.get('search[value]')

    # for search action in datatables
    # start

    lookup = Q(name__icontains=q_string) | Q(author__icontains=q_string) | Q(
        edition__icontains=q_string) | Q(publisher__icontains=q_string)

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
