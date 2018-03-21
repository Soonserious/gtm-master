$(document).ready(function() {
    {# $('input[value="1"]').attr("checked", true); #}
    $('#submit_success_label').hide();
});

$('#ocean_test_form').submit(function(event) {
    event.preventDefault();
    console.log("form submitted!")
    $.ajax({
        url: $(this).attr('action'),
        type: $(this).attr('method'),
        data: $(this).serialize(),
        success: function(json) {
            $('#ocean_test_submit').hide();
            console.log(json);
            $('#submit_success_label').show();
            console.log("success");
        },
        error: function(xhr,errmsg,err) {
            $('#submit_success_label').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                    " <a href='#' class='close'>&times;</a></div>");
            console.log(xhr.status + ": " + xhr.responseText);
        }
    });
});