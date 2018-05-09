$(document).ready(function() {
    // Валидация первого шага регистрации
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
                    $('.second_step input[type=hidden]').each(function() {
                        $(this).attr('type', 'show');
                    });
                    $('#id_birth_date').datepicker({
                        dateFormat: "dd.mm.yy"
                    });
                    return
                }
                else {
                    $form.prepend('<ul class="errorlist"><li></li></ul>');
                    $errorlist = $('.errorlist').find('li');
                    $errorlist.text(data.status);
                }
            }
        });
    });

<<<<<<< HEAD
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


=======
    $('#signup_form .prev_step').on('click', function () {
        $form = $('#signup_form');
        $('.second_step input[type=show]').each(function() {
            $(this).attr('type', 'hidden');
        });
        $('.next_step, .first_step', $form).show();
        $('.signup, .second_step, .prev_step', $form).hide();
    });

    $('.show_or_hide_pass', '#signup_form').on('mousedown', function () {
        $('#id_password1', $(this).parent()).attr('type','text');
    });

    $('.show_or_hide_pass', '#signup_form').on('mouseup', function () {
        $('#id_password1', $(this).parent()).attr('type','password');
    });

    $('.signup', '#signup_form').on('click', function(event) {
        if ( validateForm() ) { // если есть ошибки возвращает true
            event.preventDefault();
            return
        }
        $('#signup_form').submit();
    });

    function validateForm() {
        $form = $('#signup_form');
        $form.find('.errorlist').remove();
        $form.prepend('<ul class="errorlist"><li></li></ul>');
        $errorlist = $('.errorlist').find('li');
        $('input', $form).removeClass('invalide');

        var first_name  = $('#id_first_name'),
            last_name  = $('#id_last_name'),
            phone = $("#id_phone"),
            birth_date = $('#id_birth_date'),
            f_first_name = false,
            f_last_name = false,
            f_phone = false,
            f_birth_date = false,
            f_sex = false;

        if ( first_name.val().length < 1 ) {
            $errorlist.text('Поле имя не заполнено');
            first_name.addClass('invalide');
            f_first_name = true;
        }
        if ( last_name.val().length < 1 ) {
            $errorlist.text('Поле фамилии не заполнено');
            last_name.addClass('invalide');
            f_last_name = true;
        }
        if ( phone.val().length < 1 ) {
            $errorlist.text('Поле телефон не заполнено');
            phone.addClass('invalide');
            f_phone = true;
        } else {
            if ( !$.isNumeric(phone.val())) {
                $errorlist.text('Некорректный номер телефона');
                phone.addClass('invalide');
                f_phone = true;
            }
        }
        if ( birth_date.val().length < 1 ) {
            $errorlist.text('Поле дата рождения не заполнено');
            birth_date.addClass('invalide');
            f_birth_date = true;
        }
        if ( $('input[name=gender]:checked').val() == null) {
            $('input[name=gender]').addClass('invalide');
            f_sex = true;
        }

        return (f_first_name ||
            f_last_name ||
            f_phone ||
            f_birth_date ||
            f_sex);
    }
>>>>>>> e37b78319d6bd3996b7a0729297e2f8a74e3a0ab

});