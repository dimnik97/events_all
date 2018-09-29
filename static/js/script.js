function SetTimeToUser(DateStr, div_id){
    var d = new Date(),
        timezone = d.getTimezoneOffset(),
        date = new Date(DateStr.replace(/(\d+)-(\d+)-(\d+)/, '$2/$3/$1')),
        x = new Date(+date - timezone * 6e4);
    $('.event_time','#'+div_id).text(x);
// document.write(date_with_timezone)
}
function SetTimeChats(DateStr, div_id){
    $('.date_create', div_id).text(time_(DateStr));
// document.write(date_with_timezone)
}
function SetTimeDialogs(DateStr, div_id){
    $('.date_create_dailogs', div_id).text(time_(DateStr));
// document.write(date_with_timezone)
}

/**
 * Дата серверная - в часовой пояс клиента
 *
 */
function time_(DateStr) {
    var x =  new Date((+DateStr.replace(',', '.')) * 1000),
        arr=[
            'Января',
            'Февраля',
            'Марта',
            'Апреля',
            'Мая',
            'Июня',
            'Июля',
            'Августа',
            'Сентября',
            'Ноября',
            'Декабря',
        ];

    var curr_date = x.getDate(),
        curr_month = arr[x.getMonth()],
        curr_year = x.getFullYear(),
        curr_hours = x.getHours(),
        curr_minutes = x.getMinutes();
    return curr_date + " " + curr_month + " " + curr_year + " " + curr_hours + ":" + curr_minutes;
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
    function draw_events(){
        debugger;
    }

    $('button.last_events').on('click', function(){
        $.ajax({
            type: "POST",
            url: "get_events/",
            data: {
                "last_events":1
            },
            success: function (data) {
                draw_events(data);
            },
            error: function(data) {
                // как то обработать ошибку
            }
        });
    });
    $('button.friends_events').on('click', function(){

    });
    $('button.closest_events').on('click', function(){

    });

    /**
     * Проброс токена CSRF во все запросы ajax
     *
     */
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

    /**
     * Отправка данных
     *
     */
    $('.signup', '#signup').on('click', function(event) {
        if ( validateForm() ) { // если есть ошибки возвращает true
            event.preventDefault();
            return
        }
        $('#signup').submit();
    });

    /**
     * Валидация второго шага регистрации
     *
     */
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

    /**
     * Переход на второй шаг регистрации
     *
     */
    $('.next_step').on('click', function(event){
        event.preventDefault();
        var $form = $('#signup');
        ajax_validate_first_step($form);
    });

    /**
     * Валидация первого шага регистрации
     *
     */
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

    /**
     * Возврат на первый шаг
     *
     */
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

    /**
     * функция для подписки/отписки на событие
     *
     */
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


    /**
     * Форма создания новостей
     *
     */
    $('#news_create_form').on('submit', function(event){
        event.preventDefault();
        debugger;
        var frm = $('#news_create_form'),
            formData = new FormData(frm.get(0));

        $.ajax({
            contentType: false, // важно - убираем форматирование данных по умолчанию
            processData: false,
            type: frm.attr('method'),
            url: frm.attr('action'),
            data: formData,
            success: function (data) {
                updated_news = $('ul.event_news', data);
                $('ul.event_news').replaceWith($(data).filter(".event_news"));
            },
            error: function(data) {
                // как то обработать ошибку
            }
        });
    });


    /**
     * Подписка на пользователей
     * Мод. Subscribers
     *
     */
    $('body').on('click', '.add_to_friend', function(){
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

    /**
     * функция для подписки/отписки на группу
     *
     */
    $('.subscribe_group').on('click', function(){
        var group_id = $(this).closest("div.group_item").data('group_id'),
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
                    if (atcion_type === 'add') {
                        $this.text('Выйти из группы');
                        $this.data('action', 'remove');
                    }
                    if (atcion_type === 'remove') {
                        $this.text('Вступить в группу');
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

    /**
     * Ajax для формы редактирования профиля
     *
     */
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

    /**
     * Обработка данных валидации
     *
     */
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

    /**
     * Показать подписчиков и подписки
     *
     */
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
                    element: $('.infinite-container')[0],
                    reverse: true
                });
            }
        });
    });


    /**
     * Смена аватара
     *
     */
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

    /**
     * Поиск подписчика
     *
     */
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


    /**
     * Перевод из подписчика в редактора
     *
     */
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

    /**
     * Перевод из редактора в подписчика
     *
     */
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

    /**
     * Удаление из подписчиков
     *
     * Удалять могут только админы
     *
     */
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


    /**
     * Удаление группы, диалог, обработчики
     *
     */
    $('.delete_group', '.tab-content').on('click', function () {
        $( "#dialog_confirm" ).dialog({
            title: 'Подтвердите действие',
            height: '100',
            width: '200',
            draggable: false,
            resizable: false,
            modal: true,
            autoOpen: false,
            buttons: [
                {
                    text: "Да",
                    icon: "ui-icon-heart",
                    click: function() {
                        delete_group();
                    }
                },
                {
                    text: "Нет",
                    icon: "ui-icon-heart",
                    click: function() {
                        $( this ).dialog( "close" );
                    }
                }
            ],
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
    });

    /**
     * Удаление группы
     *
     */
    function delete_group() {
        $.ajax({
            url: '/groups/delete_group',
            type: 'POST',
            data: {
                'group_id': $('.tab-content').data('group_id'),
            },
            success: function (data) {
                if (data == 200) {
                } else {
                    // TODO заполнить error
                }
            }
        });
    };


    /**
     * Отправка заявки на вступление в группу
     *
     */
    $('.invite_group').on('click', function() {
        $.ajax({
            url: '/groups/invite_group',
            type: 'POST',
            data: {
                'group_id': $(this).data('group_id'),
            },
            success: function (data) {
                if (data == 200) {

                } else {
                    // TODO заполнить error
                }
            }
        });
    });


    /**
     * Выделение сообщений
     *
     */
    $('body').on('click', '.message_block', function () {
        $('.message_block').removeClass('selected_message');
        $('.message_block').find('.additional_block').hide();
        if ($(this).hasClass('is_my')) {
            if ($(this).hasClass('selected_message')) {
                $(this).removeClass('selected_message');
                $(this).find('.additional_block').hide();
            } else {
                $(this).addClass('selected_message');
                $(this).find('.additional_block').show();
            }
        }
    });


    /**
     * Обработка редактирования сообщений
     *
     */
    $('body').on('click', '.edit_message', function () {
        var $message_block = $(this).closest('.message_block'),
            id_message = $message_block.attr('message_id'),
            message_text = $message_block.find('.message').text();
        $('#chat-message-input').val(message_text);
        $('#chat-message-input').addClass('edited_message');
        $('#chat-message-input').attr('message_id', id_message);
    });


    /**
     * Обработка удаления сообщений
     *
     */
    $('body').on('click', '.delete_message', function () {
        var message_id = $(this).closest('.message_block').attr('message_id');
        $.ajax({
            url: '/chats/delete_message',
            type: 'POST',
            dataType: 'json',
            data: {
                'message_id': message_id,
            },
            success: function (data) {
                if (data.status === 200) {
                    $('[message_id='+ message_id +']').find('.message', '.r_dialog_block').text('[Сообщение удалено]');
                } else {
                    // TODO заполнить error
                }
            }
        });
    });


    /**
     * Переход в определенный чат (Либо диалог, либо комната)
     *
     */
    $('#dialogs').on('click', '.dialog_last_info', function () {
        if ($(this).find('.chat_status').hasClass('blocked')) {
            return;
        }
        var url = '';
        if ($(this).data('chat_id'))
            url = 'dlg?peer=' + $(this).data('chat_id');
        else
            url = 'dlg?room=' + $(this).data('room_id');
        $('.dialogs').hide();
        $('.back_to_dialogs').on('click', function () {
            $('.infinite-container').empty();
            infinity_dialogs();
            $('.messages').remove();
            $('.dialogs').show();
            $('.back_to_dialogs').hide();
            $('.create_chat').show();
        });
        $.get(url, function(data) {
            $('.back_to_dialogs').show();
            $('.messages_wrapper').append(data);
            $('.create_chat').hide()
        });
    });

    /**
     * Обработка чекбоксов для получения подписчиков
     *
     * Как работает можно посмотреть на "Создании чатов"
     *
     */
    function add_to_chat($this) {
        if ($this.is(':checked')) {
            var username = $this.parent().find('.username').html(),
                user_id = '"' + $this.val() + '"',
                user_item = '<span class="inside_mark" data-id='+user_id+'>'+ username +'</span>',
                user = '<div class="user">'+ user_item +'<span data-id=' + user_id + ' class="delete_user">x</span></div>';
            $('.added_users').append(user);

            $('.user span.delete_user', '.added_users').off('click').on('click', function () {
                id = $(this).data('id');
                $('[name=checkbox_' + id + ']').attr('checked', false);
                $(this).closest('.user').remove();
            });
        } else {
            var id = $this.val();
            $('*[data-id='+ id +']', '.added_users').closest('.user').remove();
        }
    }


    /**
     * Добавить пользователей в чат, включает в себя:
     *
     * Получает список подписчиков, исключает тех, кто уже есть в чате
     * Навешивает обработчики на cancel
     * Обработчики на чекбоксы
     */
    $('body').on('click', '.add_to_chat', function () {
        debugger;
        $('.add_chat_wrapper').show();
        $('.add_to_chat').hide();
        $.ajax({
            url: '/profile/get_subscribers?action=checkbox',
            type: 'GET',
            success: function (data) {
                $('.add_chat_form_subscribers', '.add_chat_wrapper').html(data);
                $('.added_users').empty();
                $(':checkbox', '.add_chat_wrapper').off('click').on('click', function () {
                    add_to_chat($(this));
                });
                var obj = $('input[type=checkbox]', '.add_chat_form_subscribers'), iter = '', added_users = [];
                $('.message_block', '.form_to_messages').each(function (key, value) {
                    added_users.push(($(this).data('user_id')).toString());
                });
                obj.each(function (key, value) {
                    iter = $(this);
                    if (added_users.indexOf(iter.val()) !== -1) {
                        iter.attr('disabled', true);
                    }
                });
            }
        });

        $('.cancel', '.add_chat_wrapper').off('click').on('click', function () {
            $('.add_to_chat').show();
            $('.create_chat_wrapper').hide();
        });

        $('.submite', '.add_chat_wrapper').off('click').on('click', function () {
            var obj = $('.user', '.add_chat_wrapper'),
                added_users = '',
                room_id = $('.messages').data('room_id');

            obj.each(function (key, value) {
                added_users += ($(this).find('span').data('id')).toString() + ' ';
            });

            $.ajax({
                url: '/chats/add_user_to_room',
                type: 'POST',
                dataType: 'json',
                data: {
                    'room_id': room_id,
                    'added_users': added_users
                },
                success: function (data) {
                    if (data.status === 200) {
                        window.location.replace(data.room_url);
                    } else {
                        // TODO заполнить error
                    }
                }
            });
        });
    });

    /**
     * Выход из группы:
     *
     * На вход room_id
     * На выходе результат
     *
     */
    $('body').on('click', '.leave_room', function () {
        var room_id = $('.messages', '.messages_wrapper').data('room_id');
        $.ajax({
            url: '/chats/decline_room',
            type: 'POST',
            dataType: 'json',
            data: {
                'room_id': room_id
            },
            success: function (data) {
                if (data['status'] == 200) {
                    window.location.replace('/chats');
                }
            }
        });
    });

    /**
     * Удалить пользователя из чата:
     *
     * На вход room_id
     * На выходе результат в виде обьекта
     *
     */
    $('body').on('click', '.delete_from_chat', function () {
        $('.delete_from_chat_wrapper').show();
        $('.cancel', '.deleted_users').off('click').on('click', function () {
            $('.delete_from_chat_wrapper').hide();
        });

        $('.delete', '.delete_from_chat_wrapper').off('click').on('click',function () {
            var room_id = $('.messages', '.messages_wrapper').data('room_id'),
                peer_id = $(this).closest('span').data('id');
            $.ajax({
                url: '/chats/remove_user_from_room',
                type: 'POST',
                dataType: 'json',
                data: {
                    'room_id': room_id,
                    'user_id': peer_id
                },
                success: function (data) {
                    if (data['status'] === 200) {
                        window.location.replace(data.room_url);
                    }
                }
            });
        });

    });


    /**
     * Создать чат, включает в себя:
     *
     * Получает список подписчиков
     * Навешивает обработчики на cancel
     * Обработчики на чекбоксы
     * Обработчик на submite
     */
    $('.create_chat').on('click', function () {
        $('.create_chat_wrapper').show();
        $('.content_paginator_chat').hide();
        $('.find_dialogs').hide();
        $('.create_chat').hide();
        $.ajax({
            url: '/profile/get_subscribers?action=checkbox',
            type: 'GET',
            success: function (data) {
                $('.create_chat_form_subscribers', '.create_chat_wrapper').html(data);
                $('.added_users').empty();
                $(':checkbox', '.create_chat_wrapper').off('click').on('click', function () {
                    add_to_chat($(this));
                });
            }
        });
        $('.cancel', '.create_chat_wrapper').off('click').on('click', function () {
            $('.find_dialogs').show();
            $('.content_paginator_chat').show();
            $('.create_chat').show();
            $('.create_chat_wrapper').hide();
        });

        $('.submite', '.create_chat_wrapper').off('click').on('click', function () {
            var dialog_name = $('[name=dialog_name]').val(),
                obj = $('.user', '.added_users'),
                added_users = '';
            obj.each(function (key, value) {
                added_users += ($(this).find('span').data('id')).toString() + ' ';
            });
            $.ajax({
                url: '/chats/create_room',
                type: 'POST',
                dataType: 'json',
                data: {
                    'dialog_name': dialog_name,
                    'added_users': added_users
                },
                success: function (data) {
                    if (data.status === 200) {
                        window.location.replace(data.room_url);
                    } else {
                        // TODO заполнить error
                    }
                }
            });
        });
    });


    /**
     * Принять заявку на чат
     *
     */
    $('.content_paginator_chat').on('click', '.accept', function () {
        var room_id = $(this).closest('.dialog_last_info').data('room_id');
        $.ajax({
            url: '/chats/join_room',
            type: 'POST',
            dataType: 'json',
            data: {
                'room_id': room_id
            },
            success: function (data) {
                if (data.status === 200) {
                    window.location.replace(data.room_url);
                } else {
                    // TODO заполнить error
                }
            }
        });
    });


    /**
     * Отклонить заявку на чат
     *
     */
    $('.content_paginator_chat').on('click', '.decline', function () {
        var room_id = $(this).closest('.dialog_last_info').data('room_id');
        $.ajax({
            url: '/chats/decline_room',
            type: 'POST',
            dataType: 'json',
            data: {
                'room_id': room_id
            },
            success: function (data) {
                if (data.status === 200) {
                    window.location.replace(data.room_url);
                } else {
                    // TODO заполнить error
                }
            }
        });
    })

    /**
     * Поиск города в кастомном селекте
     *
     */
    $('.find_city', '.custom_select').on('input', function () {
        var city_name = $(this).val(),
            $this = $(this);
        $.ajax({
            url: '/cities_/find_city',
            type: 'POST',
            dataType: 'json',
            data: {
                'city_name': city_name
            },
            success: function (data) {
                $('.select_item', '.custom_select_items').remove();
                if (data === false) {
                    $('.custom_select_items').append("<span  class='select_item go_out' >Ничего не найдено</span>");
                    return;
                }
                data.forEach(function(data, i, arr) {
                    $('.custom_select_items').append("<span  class='select_item' data-city_id="+ data.pk +">" + data.fields.city + "</span>");
                });

                set_value_on_custom_select();
            }
        });
    });

    /**
     * Установка значения в кастомном селекте
     *
     */
    set_value_on_custom_select();
    function set_value_on_custom_select() {
        $('.select_item', '.custom_select_items').off('click').on('click', function () {
            $(this).parent().find('.select_item').removeClass('selected');
            if ($(this).hasClass('go_out'))
                return;
            $(this).addClass('selected');
            try {
                set_center_by_city_name($(this).html());
            } catch (err) {
            }
        })
    }






    /**
     * Ajax для формы EventForm (Создание)
     *
     */
    $('#event_form_create').on('submit', function(e){
        custom_save_event_form($('#event_form_create'), e, '/events/create')
    });

    /**
     * Ajax для формы EventForm (Редактирование)
     *
     */
    $('#event_form_edit').on('submit', function(e){
        custom_save_event_form($('#event_form_edit'), e, '/events/edit/' + $('#id_id').val())
    });

    /**
     * Ajax для формы EventForm
     *
     */
    function custom_save_event_form($form, e, url){
        e.preventDefault();
        let data = get_form_with_custom_modules($form);

        $.ajax({
            type: "POST",
            url: url,
            data: data,
            dataType: 'json',
            success: function(data) {
                if (data.status === 200) {
                    debugger;
                    window.location.replace('/events/' + data.url);
                } else {
                    ajax_validate_form_data($form, data);
                }
            }
        });
    };

    /**
     * Получение выбранного в кастомном селекте
     *
     */
    function get_value_from_custom_select(parent_selector) {
        return parent_selector.find('.selected');
    }
    /**
     * Получение отмеченного на карте маяка
     *
     */
    function get_geo_values(indexed_array, selector) {
        if (selector.html().length > 0) {
            indexed_array['geo_name'] = selector.html();
            indexed_array['lat'] = selector.data('lat');
            indexed_array['lng'] = selector.data('lng');
        }
        return indexed_array;
    }
    /**
     * Получение формы с кастомными модулями, например селект по городам
     *
     */
    function get_form_with_custom_modules($form) {
        let unindexed_array = $form.serializeArray(),
            indexed_array = {};

        let location = get_value_from_custom_select($('#location'));
        unindexed_array.push({name: 'location', value: location.data('city_id')});

        indexed_array = get_geo_values(indexed_array, $('.select_bounds_yamaps'));

        $.map(unindexed_array, function(n, i){
            indexed_array[n['name']] = n['value'];
        });

        return indexed_array;
    }
});
