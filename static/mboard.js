
function setBtn(){
$("button.button_d").click(function () {
    var num = $('#num').text();
    num = parseInt(num) - 1;
    $('#num').text(num);

    var x = $(this).attr('id');
    $('div.mboard_div#'+x).remove();
    $.get('/dbdelete/'+x);
    }

)}


function getMessage(){
    var Message = $.ajax({url:"/Message_get",async:false});
    var res = eval(Message.responseText);
    $('#num').text(res.length);
    $('div#YES').empty();
    for(var l=res.length,i=l-1;i>-1;i--){

            var name = res[i]['name'];
            var id = res[i]['id'];
            var time = res[i]['time'];
            var content = res[i]['content'];
            htmlTxt = "<div class='mboard_div' id='"+ id + "'>" +"<hr>"+
                name +"   " +time + "<br>"+
                    "<div class='mboard_content'>" +
                content+"</div>" +
                "<button style='float:right;margin-top:-15px;' class='button_d' id='"+id+"'>删除此条</button>" +
                "</div>";
            $('div#YES').append(htmlTxt);





    }


}