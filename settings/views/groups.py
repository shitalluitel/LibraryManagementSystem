from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect, reverse

from settings.forms.groups import GroupsCreate


@login_required
@permission_required('settings.add_group')
def create_group(request):
    context = {}
    form = GroupsCreate(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            permissions = form.cleaned_data.get('permission')
            group = form.save()
            for permission in permissions:
                group.permissions.add(permission)

            messages.success(request, 'Successfully created group with name {}.'.format(group.name))
            return redirect('groups:list_group')

    context['form'] = form
    return render(request, 'groups/create.html', context)


@login_required
@permission_required('settings.add_group')
def list_group(request):
    context = {}

    # data = None
    # if request.user.is_authenticated():
    data = Group.objects.all()

    context['datas'] = data

    return render(request, 'groups/list.html', context)


@login_required
@permission_required('settings.change_group')
def edit_group(request, pk):
    context = {}
    try:
        group = Group.objects.get(pk=pk)
        group_permissions = group.permissions.all()

    except Group.DoesNotExist:
        messages.warning(request, 'Unable to find group with this name.')
        return redirect(request.path)

    form = GroupsCreate(request.POST or None, instance=group)
    if request.method == 'POST':
        if form.is_valid():
            permissions = form.cleaned_data.get('permission')
            group = form.save()
            for permission in group_permissions:
                if not permission in permissions:
                    group.permissions.remove(permission)

            for permission in permissions:
                if not permission in group_permissions:
                    group.permissions.add(permission)

            messages.success(request, 'Successfully updated group with name {}.'.format(group.name))
            return redirect('groups:list_group')

    context['form'] = form
    return render(request, 'groups/create.html', context)
