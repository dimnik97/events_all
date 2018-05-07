$(document).ready(function() {
    $('#signup_form .next_step').on('click', function () {

        $form = $('#signup_form');
        $('label, input[type!="hidden"]', $form);

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
                    $('.next_step, .first_step', $form).hide();
                    $('.signup, .second_step, .prev_step', $form).show();
                    $('.second_step input', $form).attr('type', 'show');
                    return
                }
                else {

                    $form.prepend('<ul class="errorlist"><li></li></ul>');
                    $errorlist = $('.errorlist').find('li');
                    $errorlist.text(data.status);
                    // if(data.status === null) {
                    //     $errorlist.text('Заполните поле e-mail');
                    //     return
                    // }
                    // else {
                    //     $errorlist.text('Пользователь с таким e-mail уже существует');
                    //     return
                    // }
                }
            }
        });
    });


    $('#signup_form .prev_step').on('click', function () {
        $form = $('#signup_form');
        $('.second_step input', $form).attr('type', 'hiddden');
        $('.next_step, .first_step', $form).show();
        $('.signup, .second_step, .prev_step', $form).hide();
    })
});