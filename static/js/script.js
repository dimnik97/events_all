$(document).ready(function() {
    function SetTimeToUser(DateStr){
        debugger;
        var d = new Date();
        var timezone = d.getTimezoneOffset();
        var date = new Date(DateStr.replace(/(\d+)-(\d+)-(\d+)/, '$2/$3/$1'));
        var date_with_timezone = new Date(+date - timezone * 6e4);
        document.write(date_with_timezone)
    }

    // Проброс токена CSRF во все запросы ajax
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            function getCookie(name) {
                var cookieValue = null;
                if (document.cookie && document.cookie != '') {
                    var cookies = document.cookie.split(';');
                    for (var i = 0; i < cookies.length; i++) {
                        var cookie = jQuery.trim(cookies[i]);
                        if (cookie.substring(0, name.length + 1) == (name + '=')) {
                            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                            break;
                        }
                    }
                }
                return cookieValue;
            }

            if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                // Only send the token to relative URLs i.e. locally.
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }
        }
    });

    // Валидация второго шага регистрации
    $('.signup', '#signup').on('click', function(event) {
        if ( validateForm() ) { // если есть ошибки возвращает true
            event.preventDefault();
            return
        }
        $('#signup').submit();
    });

    function validateForm() {
        $form = $('#signup');
        $('.invalid-feedback', $form).remove();
        $('input', $form).removeClass('is-invalid');

        var first_name  = $('#id_first_name'),
            last_name  = $('#id_last_name'),
            phone = $("#id_phone"),
            f_first_name = false,
            f_last_name = false,
            f_phone = false,
            f_sex = false;

        if ( first_name.val().length < 1 ) {
            first_name.after('<div class="invalid-feedback"> ' + 'Поле имя не заполнено' + '</div>');
            first_name.addClass('is-invalid');
            f_first_name = true;
        }
        if ( last_name.val().length < 1 ) {
            last_name.after('<div class="invalid-feedback"> ' + 'Поле фамилии не заполнено' + '</div>');
            last_name.addClass('is-invalid');
            f_last_name = true;
        }
        if ( phone.val().length < 1 ) {
            phone.after('<div class="invalid-feedback"> ' + 'Поле телефон не заполнено' + '</div>');
            phone.addClass('is-invalid');
            f_phone = true;
        } else {
            if ( !$.isNumeric(phone.val())) {
                phone.after('<div class="invalid-feedback"> ' + 'Некорректный номер телефона' + '</div>');
                phone.addClass('is-invalid');
                f_phone = true;
            }
        }

        return (f_first_name ||
            f_last_name ||
            f_phone ||
            f_sex);
    }

    $('.next_step').on('click', function(event){
        event.preventDefault();
        $form = $('#signup');
        ajax_validate_first_step($form);
    });

    // Валидация первого шага регистрации
    function ajax_validate_first_step(form) {
        $.ajax({
            url : "/main_app/signup_check/",
            type : "POST",
            data : form.serialize(),
            success : function(json) {
                $('input').removeClass('is-invalid');
                $('.invalid-feedback').remove();

                if (json.email !== undefined) {
                    $('#id_email').addClass('is-invalid');
                    $('#id_email').after('<div class="invalid-feedback"> ' + json.email + '</div>');
                }
                if (json.password1 !== undefined) {
                    $('#id_password1').addClass('is-invalid');
                    $('#id_password1').after('<div class="invalid-feedback"> ' + json.password1.split("'")[1] + '</div>');
                }
                else {
                    $('.field_d_none').addClass('form-group').removeClass('field_d_none');
                    $('.first_step, .next_step').hide();
                    $('.prev_step, .signup').show();
                }
            },
            error : function(xhr,errmsg,err) {
                $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                    " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });
    };

    // Возврат на первый шаг
    $('.prev_step').on('click', function () {
        $form = $('#signup');
        $('.form-group', $form).addClass('field_d_none').removeClass('form-group');
        $('.next_step, .first_step', $form).show();
        $('.signup, .second_step, .prev_step', $form).hide();
    });

    $('.show_or_hide_pass', '#signup_form').on('mousedown', function () {
        $('#id_password1', $(this).parent()).attr('type','text');
    });

    $('.show_or_hide_pass', '#signup_form').on('mouseup', function () {
        $('#id_password1', $(this).parent()).attr('type','password');
    });

    // функция для подписки/отписки на событие
    $('.subscribe_event').on('click', function(){
        var event_id = $(this).closest("div.event_item").data('event_id'),
            atcion_type = $(this).data('action'),
            $this = $(this);
        $.ajax({
            type: "POST",
            url: "/main_app/subscribe_event/",
            data:{
                'event_id': event_id,
                'action': atcion_type
            },
            dataType: 'json',
            success: function(data){
                if (data) {
                    if (atcion_type == 'subscribe') {
                        $this.text('Отписаться');
                        $this.data('action', 'unsubscribe');
                    }
                    else {
                        $this.text('Пойти');
                        $this.data('action', 'subscribe');
                    }
                }

            }
        });
    });
    // $('.subscribe_event').on('click', function(){
    //     $this = $(this);
    //
    //     $.ajax({
    //         type: "POST",
    //         url: "/events/edit/",
    //         data:{
    //
    //         },
    //         dataType: 'json',
    //         success: function(data){
    //             if (data) {
    //
    //             }
    //
    //         }
    //     });
    // });

// Подписка на пользователей
// Мод. Subscribers
    $('.add_to_friend').on('click', function(){
        var user_id = $(this).data('user_id'),
            action = $(this).data('action'),
            $this = $(this);
        $.ajax({
            type: "POST",
            url: "/profile/add_or_remove_friends/",
            data:{
                'user_id': user_id,
                'action': action
            },
            dataType: 'json',
            success: function(data) {
                if (data) {
                    if (action == 'add') {
                        $this.text('отписаться');
                        $this.data('action', 'remove');
                    }
                    else {
                        $this.text('Подписаться');
                        $this.data('action', 'add');
                    }
                }
            }
        });
    });

    $('#main_info').on('submit', function(e){
        ajax_validate_form($('#main_info'), e)
    });

    $('#settings').on('submit', function(e){
        ajax_validate_form($('#settings'), e)
    });

    // Ajax для форм
    function ajax_validate_form($form, e){
        e.preventDefault();
        var data = $form.serialize();

        $.ajax({
            type: "POST",
            url: "/profile/edit",
            data: data,
            dataType: 'json',
            success: function(data) {
                ajax_validate_form_data($form, data);
            }
        });
    };

    // Обработка данных валидации
    function ajax_validate_form_data($form, data) {
        $('input').removeClass('is-invalid');
        $('.invalid-feedback').remove();
        if (data != '200') {
            var errors = data;
            for (var i = 0; i < errors.length; i++) {
                var $field = $form.find(errors[i].key);
                $field.addClass('is-invalid');
                $field.after('<div class="invalid-feedback"> ' + errors[i].desc + '</div>');
            }
        }
    }

    $('.all_subscribers').on('click', function () {
        $('.infinite-more-link').attr('href', '/profile/get_subscribers?page=1');
        var infinite = new Waypoint.Infinite({
            element: $('.infinite-container')[0],
            onBeforePageLoad: function () {
            },
            onAfterPageLoad: function ($items) {
                $('.infinite-more-link').attr('href', '/profile/get_subscribers?page='+2);
            }
        });
        // $.ajax({
        //     type: "POST",
        //     url: "/profile/get_subscribers",
        //     dataType: 'json',
        //     success: function(data) {
        //         debugger;
        //         $('.infinite-more-link').attr('href', '/profile/get_subscribers?page='+data.pk);
        //         $('.infinite-container').append(data);
        //     }
        // });

        // $( "#dialog" ).dialog({
        //     title: 'Подписчики',
        //     height: '700',
        //     width: '500',
        //     draggable: false,
        //     resizable: false,
        //     modal: true,
        //     autoOpen: false,
        //     position: {
        //         my: 'center',
        //         at: 'center',
        //         collision: 'fit',
        //         using: function(pos) {
        //             var topOffset = $(this).css(pos).offset().top;
        //             if (topOffset < 0) {
        //                 $(this).css('top', pos.top - topOffset);
        //             }
        //         }
        //     },
        // }).dialog('open');
    });
});