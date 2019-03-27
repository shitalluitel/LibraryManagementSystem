from django.contrib import messages
from django.contrib.auth.decorators import permission_required, login_required
from django.shortcuts import render, redirect

# Create your views here.
from files.forms import FileForm
from files.models import File


# @permission_required('files.add_file')
def file_upload(request):
    context = {}
    form = FileForm()
    if request.method == "POST":
        form = FileForm(request.POST or None, files=request.FILES)
        if form.is_valid():
            file = form.save(commit=False)
            file.save()

            messages.success(request, "Successfully uploaded file.")
            return redirect('files:file_upload')
    context['form'] = form
    return render(request, 'files/upload.html', context)


# @permission_required('files.add_file')
def file_home(request):
    return render(request, 'files/file_home.html')


def file_list(request):
    context = {}

    type = request.GET.get('type')
    type = type.capitalize()

    file = File.objects.filter(type=type, is_deleted=False)

    context['datas'] = file
    context['type'] = type
    return render(request, 'files/file_list.html', context)


def file_delete(request, pk):
    next = request.GET.get('next')

    try:
        file = File.objects.get(pk=pk)
        file.is_deleted = True
        messages.success(request, "Successfully deleted the file.")
    except Exception as e:
        messages.error(request, e)

    return redirect(next)
