function SetTimeToUser(DateStr, div_id){
    var d = new Date();
    var timezone = d.getTimezoneOffset();
    var date = new Date(DateStr.replace(/(\d+)-(\d+)-(\d+)/, '$2/$3/$1'));
    var date_with_timezone = new Date(+date - timezone * 6e4);
    $('.event_time','#'+div_id).text(date_with_timezone);
// document.write(date_with_timezone)
}


function SetTimeToUser_js_str(DateStr){
    var d = new Date();
    var timezone = d.getTimezoneOffset();
    var date = new Date(DateStr.replace(/(\d+)-(\d+)-(\d+)/, '$2/$3/$1'));
    var date_with_timezone = new Date(+date - timezone * 6e4);


    var strdate = date_with_timezone.getFullYear()+'-'+
        GetCorrectNumber(date_with_timezone.getMonth(), 1) +'-'+
        GetCorrectNumber(date_with_timezone.getDate()) +' '+
        GetCorrectNumber(date_with_timezone.getHours()) +':' +
        GetCorrectNumber(date_with_timezone.getMinutes());
    strdate = strdate.substring(0, strdate.length-1) + "0";

    return strdate;
// document.write(date_with_timezone)
}

function SetTimeToServer(DateStr){

    var d = new Date();
    var timezone = d.getTimezoneOffset();
    var date = new Date(DateStr.replace(/(\d+)-(\d+)-(\d+)/, '$2/$3/$1'));
    var date_with_timezone = new Date(+date + timezone * 6e4);
    var minutes;
    if(date_with_timezone.getMinutes() < 10){
        minutes = '0'+ date_with_timezone.getMinutes();
    }else{
        minutes = date_with_timezone.getMinutes();
    }


    var str_date = date_with_timezone.getFullYear()+'-'+
        GetCorrectNumber(date_with_timezone.getMonth(), 1) +'-'+
        GetCorrectNumber(date_with_timezone.getDate()) +' '+
        GetCorrectNumber(date_with_timezone.getHours()) +':' +
        GetCorrectNumber(date_with_timezone.getMinutes());



    return str_date;
}

// метод для корректного преобразования даты в строку
// Number - число, котороре нужно преобразовать, добавть 0, если оно меньше 10
// is_month - флаг месяца, js по умолчанию возвращает месяц от 0 до 11
// is_min - флаг минут, округление до 00/10/20/30/40/50 минут в меньшую сторону
function GetCorrectNumber(Number, is_month=0, is_min = 0){
    var correct_date;

    if(is_month == 1){
        Number += 1;
    }

    if(Number < 10){
        correct_date = '0'+ Number;
    }else{
        correct_date = Number;
    }


    return correct_date;
}



$(document).ready(function() {


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
                    " <a href='#' class='close'>&times;</a></div>");
                console.log(xhr.status + ": " + xhr.responseText);
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

    // Подписка на пользователей
    // Мод. Subscribers
    $('.add_to_friend').on('click', function(){
        var user_id = $(this).data('user_id'),
            action = $(this).data('action'),
            $this = $(this);
        $.ajax({
            type: "POST",
            url: "/profile/subscribe",
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

    // функция для подписки/отписки на группу
    $('.subscribe_group').on('click', function(){
        var group_id = $(this).closest('div.group_item').data('group_item'),
            atcion_type = $(this).data('action'),
            $this = $(this);
        $.ajax({
            type: "POST",
            url: "/groups/subscribe_group/",
            data:{
                'group_id': group_id,
                'action': atcion_type
            },
            dataType: 'json',
            success: function(data){
                if (data) {
                    if (atcion_type == 'add') {
                        $this.text('Вступить в группу');
                        $this.data('action', 'remove');
                    }
                    if (atcion_type == 'remove') {
                        $this.text('Выйти из группы');
                        $this.data('action', 'add');
                    }
                }

            }
        });
    });

    $('#edit_profile_form').on('submit', function(e){
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

    // Подписки и подписчики
    $('.all_subscribers, .all_followers').on('click', function () {
        $( "#dialog" ).dialog({
            title: 'Подписчики',
            height: '700',
            width: '500',
            draggable: false,
            resizable: false,
            modal: true,
            autoOpen: false,
            position: {
                my: 'center',
                at: 'center',
                collision: 'fit',
                using: function(pos) {
                    var topOffset = $(this).css(pos).offset().top;
                    if (topOffset < 0) {
                        $(this).css('top', pos.top - topOffset);
                    }
                }
            },
        }).dialog('open');

        var url = $(this).data('url');
        $.ajax({
            url: url,
            success: function (data) {
                $('.content_paginator').html(data);
                var infinite = new Waypoint.Infinite({
                    element: $('.infinite-container')[0]
                });
            }
        });
    });

    $('.change_avatar, .change_mini').on('click', function () {
        var url = $(this).data('url'),
            title = $(this).html();

        $( "#dialog_img" ).dialog({
            title: title,
            height: '700',
            width: '700',
            draggable: false,
            resizable: false,
            modal: true,
            autoOpen: false,
            beforeClose: function(){
                $('.help_image_div').imgAreaSelect({
                    remove: true
                });
                $('#output_image').imgAreaSelect({
                    remove: true
                });
            },
            position: {
                my: 'center',
                at: 'center',
                collision: 'fit',
                using: function(pos) {
                    var topOffset = $(this).css(pos).offset().top;
                    if (topOffset < 0) {
                        $(this).css('top', pos.top - topOffset);
                    }
                }
            },
        }).dialog('open');

        $.ajax({
            url: url,
            type: 'GET',
            success: function (data) {
                $( "#dialog_img" ).html(data);
            }
        });
    });

    $('.find_subscribers').on('input', function () {
        $.ajax({
            url: '/groups/find_subscribers',
            type: 'POST',
            data: {
                'value': $(this).val(),
                'group_id': $('.select_roles').data('group_id'),
            },
            success: function (data) {
                if (data) {
                    var r_side = $('.right_side_select_roles', '.select_roles').empty();
                    r_side.append(data);
                } else {
                    // TODO заполнить error
                }
            }
        });
    });

    function add_to_editor() {
        $('.add_to_editor').off('click').on('click', function () {
            var $this = $(this);
            $.ajax({
                url: '/groups/add_to_editor',
                type: 'POST',
                data: {
                    'user': $(this).parent('li').data('id'),
                    'group_id': $('.select_roles').data('group_id'),
                },
                success: function (data) {
                    if (data == 200) {
                        $this.text('Разжаловать');
                        $this.addClass('add_to_subscriber').removeClass('add_to_editor');
                        $('.left_side_select_roles').append($this.closest('li'));
                        add_to_subscriber();
                    } else {
                        // TODO заполнить error
                    }
                }
            });
        });
    }

    function add_to_subscriber() {
        $('.add_to_subscriber').off('click').on('click', function () {
            var $this = $(this);
            $.ajax({
                url: '/groups/add_to_subscribers',
                type: 'POST',
                data: {
                    'user': $(this).parent('li').data('id'),
                    'group_id': $('.select_roles').data('group_id'),
                },
                success: function (data) {
                    if (data == 200) {
                        $this.text('Добавить редактора');
                        $this.addClass('add_to_editor').removeClass('add_to_subscriber');
                        $('.right_side_select_roles').append($this.closest('li'));
                        add_to_editor();
                    } else {
                        // TODO заполнить error
                    }
                }
            });
        });
    }

    $('.delete', '.select_roles').on('click', function () {
        var $this = $(this);
        $.ajax({
            url: '/groups/delete_subscribers',
            type: 'POST',
            data: {
                'user': $(this).parent('li').data('id'),
                'group_id': $('.select_roles').data('group_id'),
            },
            success: function (data) {
                if (data == 200) {
                    $this.closest('li').remove();
                } else {
                    // TODO заполнить error
                }
            }
        });
    });

    add_to_editor();
    add_to_subscriber();
});