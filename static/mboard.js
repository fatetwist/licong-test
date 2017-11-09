
$(document).ready(function(){
$("button.button_d").click(function () {
    var num = $('#num').text();
    num = parseInt(num) - 1;
    $('#num').text(num);

    var x = $(this).attr('id');
    $('div.mboard_div#'+x).remove();
    $.get('/dbdelete/'+x);
    }

)
    }) 