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

$('body').on('change', '#id_course', function () {
    var id = $(this).children('option:selected').val();
    if (id != '') {
        $.ajax({
            url: '/batches/' + id + '/batch-list/',
            error: function () {
                console.log("error");
            },
            success: function (data) {
                $('#id_batch').empty().append(data);
            },
            type: 'GET'
        });
    } else {
        $('#id_batch').empty().append("<option value='' selected>Select Batch</option>");
    }
});

$('body').on('change', '#id_batch', function () {
    var batch = $(this).children('option:selected').val();
    var course = $('#id_course').children('option:selected').val();
    if (batch != '') {
        $.ajax({
            url: '/students/get-student-option/?batch=' + batch + '&course=' + course,
            error: function () {
                console.log("error");
            },
            success: function (data) {
                $('#id_student').empty().append(data);
                console.log(data);
            },
            type: 'GET'
        });
    } else {
        $('#id_student').empty().append("<option value='' selected>Select Student</option>");
    }
});


