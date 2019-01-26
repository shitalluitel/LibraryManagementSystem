$('body').on('click', '.delete-form', function () {
    btn = $(this);
    prefix = btn.attr('id');
    var total = parseInt($('#id_' + prefix + '-TOTAL_FORMS').val());
    if (total > 0) {
        btn.closest('div').remove();
        var forms = $('.delete-form');
        $('#id_' + prefix + '-TOTAL_FORMS').val(forms.length);
        for (var i = 0, formCount = forms.length; i < formCount; i++) {
            $(forms.get(i)).find(':input').each(function () {
                updateElementIndex(this, prefix, i);
            });
        }
    }
    return false;
    // form.remove();
});