from django.contrib import messages
from django.contrib.auth.decorators import permission_required, login_required
from django.shortcuts import render

# Create your views here.
from settings.forms import SettingForm
from settings.models import Setting


@login_required
# @permission_required('settings.add_setting')
def setting(request):
    context = {}
    try:
        setting = Setting.objects.first()
        form = SettingForm(request.POST or None, instance=setting)
    except Setting.DoesNotExist:
        form = SettingForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            data = form.save(commit=False)
            data.user = request.user
            data.save()
            messages.success(request, 'Setting updated successfully.')

    context['form'] = form
    return render(request, 'settings/setting.html', context)
