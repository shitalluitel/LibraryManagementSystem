$('body').on('change', '#id_book_category', function () {
    var id = $(this).children('option:selected').val();
    $.ajax({
        url: '/books/get-bookunit-option/' + id + '/',
        error: function () {
            console.log("error");
        },
        success: function (data) {
            $('#id_book_unit').empty().append(data);
        },
        type: 'GET'
    });
});
