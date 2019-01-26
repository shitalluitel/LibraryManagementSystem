# from users.models import User
from django.db import transaction, IntegrityError
from django.shortcuts import render, redirect
from users import forms
from django.contrib import messages
from settings.models import WardNumber, WardStaff

# from users.models import USER_ROLES
from users.decorators import admin_required
from users.models import User


@admin_required
def ward_user_register(request):
    context = {}
    # try:
    #     ward = WardNumber.objects.get(pk=pk, is_deleted=False)
    #     context['ward'] = ward
    # except WardNumber.DoesNotExist:
    #     messages.error(request, 'Ward Number Not Found')
    #     return redirect('wards:list')

    form = forms.WardUserRegisterForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            try:
                with transaction.atomic():
                    user = form.save(commit=False)
                    user.save()

                    ward_user = WardStaff()
                    ward_user.user = user
                    ward_user.ward_number = form.cleaned_data.get('ward')
                    ward_user.save()

                    messages.success(request, 'User Created Successfully')
                    return redirect('users:ward_users')
            except IntegrityError:
                print("Integrity error")
        else:
            print(form.errors)

    context['form'] = form
    return render(request, 'ward_users/ward_user_register.html', context)


@admin_required
def ward_users(request):
    context = {}

    ward_no = request.GET.get('ward')

    if ward_no:
        users = WardStaff.objects.filter(ward_number=ward_no)
    else:
        users = WardStaff.objects.all()

    context['users'] = users

    return render(request, 'ward_users/ward_users.html', context)


@admin_required
def ward_user_detail(request, pk):
    context = {}

    try:
        data = User.objects.get(pk=pk)
    except:
        messages.error(request, "User doesnot exist.")
        return redirect('users:ward_users')

    form = forms.WardUserEditForm(request.POST or None, instance=data)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "User successfully edited.")
            return redirect("users:ward_users")

    context['form'] = form
    context['data'] = data
    return render(request, 'ward_users/ward_user_details.html', context)


@admin_required
def deactivate_user(request, pk):
    try:
        user = User.objects.get(pk=pk, is_deleted=False)

    except:
        messages.error(request, "Unable to find user.")
        return redirect('users:ward_users')

    user.is_deleted = True
    user.save()
    return redirect('users:ward_users')


@admin_required
def activate_user(request, pk):
    try:
        user = User.objects.get(pk=pk, is_deleted=True)

    except:
        messages.error(request, "Unable to find user.")
        return redirect('users:ward_users')

    user.is_deleted = False
    user.save()
    return redirect('users:ward_users')


@admin_required
def ward_user_change_password(request, pk):
    try:
        user = User.objects.get(pk=pk, is_deleted=False)
    except:
        messages.error(request, 'User not found.')
        return redirect('users:ward_users')

    form = forms.WardUserPasswordChangeForm(data=request.POST or None, user=user)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Password changed successfully")
            return redirect('users:ward_users')

    context = {
        'form': form
    }
    return render(request, 'users/change_password.html', context)

    pass
