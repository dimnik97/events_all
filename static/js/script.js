$(document).ready(function() {
    $('#signup_form .next_step').on('click', function () {

        $form = $('#signup_form');
        $values = $form.serialize();
        $form.find('.errorlist').remove();

        $.ajax({
            type: "POST",
            url: "/main_app/signup_check/",
            data:{
                "data": $values,
            },
            dataType: 'json',
            success: function(data){
                if(data.status == false) {
                    $('.next_step', $form).hide();
                    $('.signup', $form).show();
                    return
                }
                else {
                    $form.prepend('<ul class="errorlist"><li></li></ul>');
                    $errorlist = $('.errorlist').find('li');
                    if(data.status === null) {
                        $errorlist.text('Заполните поле e-mail');
                        return
                    }
                    else {
                        $errorlist.text('Пользователь с таким e-mail уже существует');
                        return
                    }
                }
            }
        });
    });

    debugger;
    $('button.subscribe_event').on('click', function(){
        debugger;
        $.ajax({
            type: "POST",
            url: "/main_app/subscribe_event/",
            data:{

            },
            dataType: 'json',
            success: function(data){

            }
        });

    });



});