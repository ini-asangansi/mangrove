$(document).ready(function() {
    $("#error_table").hide();
    var uploader = new qq.FileUploader({
        // pass the dom node (ex. $(selector)[0] for jQuery users)
        element: document.getElementById('file_uploader'),
        // path to server-side upload script
        action: window.location.pathname,
        onComplete: function(id, fileName, responseJSON) {
            $('#message').remove();
            $('#error_tbody').html('');
            $("#error_table").hide();
            $("#data_sender_table tbody").html('');
            $.each(responseJSON.all_data, function(index, element) {
                $("#data_sender_table tbody").append("<tr><td>" + element.id + "</td><td>" + element.name + "</td><td>" + element.short_name + "</td><td>" + element.type + "</td><td>" + element.location + "</td><td>" + element.description + "</td><td>" + element.mobile_number + "</td></tr>")
            });
            if (responseJSON.success == true) {
                $('<span id="message" class="success_message">' + responseJSON.message + '</span>').insertAfter($('#file-uploader'));

            }
            else {
                $('#error_tbody').html('');
                $("#error_table").show();
                $('<span id="message" class="error_message">' + responseJSON.message + '</span>').insertAfter($('#file-uploader'));
                $.each(responseJSON.failure_imports, function(index, element) {
                    $("#error_table table tbody").append("<tr><td>" + element.row_num + "</td><td>" + JSON.stringify(element.row) + "</td><td>"
                            + element.error + "</td></tr>")
                });
                $("#error_table").show();
            }

        }
    });


});