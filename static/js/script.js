function SetTimeToUser(DateStr, div_id){
    let d = new Date(),
        timezone = d.getTimezoneOffset(),
        date = new Date(DateStr.replace(/(\d+)-(\d+)-(\d+)/, '$2/$3/$1')),
        x = new Date(+date - timezone * 6e4);
    $('.event_time','#'+div_id).text(x);
}
/**
 * Дата серверная - в часовой пояс клиента
 *
 */
function time_(DateStr) {
    let x =  new Date((+DateStr.replace(',', '.')) * 1000),

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
            'Октября',
            'Ноября',
            'Декабря',
        ];

    let curr_date = x.getDate(),
        curr_month = arr[x.getMonth() ],
        curr_year = x.getFullYear(),
        curr_hours = x.getHours(),

        curr_minutes = x.getMinutes();
    return curr_date + " " + curr_month + " " + curr_year + " " + curr_hours + ":" + curr_minutes;
}


function SetTimeToUser_js_str(DateStr){
    let d = new Date();
    let timezone = d.getTimezoneOffset();
    let date = new Date(DateStr.replace(/(\d+)-(\d+)-(\d+)/, '$2/$3/$1'));
    let date_with_timezone = new Date(+date - timezone * 6e4);


    let strdate = date_with_timezone.getFullYear()+'-'+
        GetCorrectNumber(date_with_timezone.getMonth(), 1) +'-'+
        GetCorrectNumber(date_with_timezone.getDate()) +' '+
        GetCorrectNumber(date_with_timezone.getHours()) +':' +
        GetCorrectNumber(date_with_timezone.getMinutes());
    strdate = strdate.substring(0, strdate.length-1) + "0";

    return strdate;
// document.write(date_with_timezone)
}

function SetTimeToServer(DateStr){

    let d = new Date();
    let timezone = d.getTimezoneOffset();
    let date = new Date(DateStr.replace(/(\d+)-(\d+)-(\d+)/, '$2/$3/$1'));
    let date_with_timezone = new Date(+date + timezone * 6e4);
    let minutes;
    if (date_with_timezone.getMinutes() < 10) {
        minutes = '0'+ date_with_timezone.getMinutes();
    } else {
        minutes = date_with_timezone.getMinutes();
    }

    let str_date = date_with_timezone.getFullYear()+'-'+
        GetCorrectNumber(date_with_timezone.getMonth(), 1) +'-'+
        GetCorrectNumber(date_with_timezone.getDate()) +' '+
        GetCorrectNumber(date_with_timezone.getHours()) +':' +
        GetCorrectNumber(date_with_timezone.getMinutes());
    return str_date;
}


function SetTimeChats(DateStr, div_id) {
    $('.date_create', div_id).text(time_(DateStr));
}
function SetTimeDialogs(DateStr, div_id) {
    $('.date_create_dailogs', div_id).text(time_(DateStr));
}

// метод для корректного преобразования даты в строку
// Number - число, котороре нужно преобразовать, добавть 0, если оно меньше 10
// is_month - флаг месяца, js по умолчанию возвращает месяц от 0 до 11
// is_min - флаг минут, округление до 00/10/20/30/40/50 минут в меньшую сторону
function GetCorrectNumber(Number, is_month=0, is_min = 0){
    let correct_date;

    if(is_month === 1){
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
    var $body = $('body');
    /**
     * Отправка данных
     *
     */
    $('.signup', '#signup').on('click', function(event) {
        if ( validateForm() ) { // если есть ошибки возвращает true
            return
        }
        $('#signup').submit();
    });

    /**
     * Валидация второго шага регистрации
     *
     */
    function validateForm() {
        let $form = $('#signup');
        $('.invalid-feedback', $form).remove();
        $('input', $form).removeClass('is-invalid');

        let first_name  = $('#id_first_name'),
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
    }

    /**
     * Возврат на первый шаг
     *
     */
    $('.prev_step').on('click', function () {
        var $form = $('#signup');
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
    $body.on('click', '.subscribe_event',  function(){
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
                if (parseInt(data) === 200) {
                    if (atcion_type === 'subscribe') {
                        $this.text('Отписаться');
                        $this.data('action', 'unsubscribe');
                    }
                    else {
                        $this.text('Пойти');
                        $this.data('action', 'subscribe');
                    }
                } else if (parseInt(data) === 401) {
                    window.location.replace('/accounts/login/?next=');
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
        $('.error_news').html();
        $('#id_event_id').val($('.event_item').data('event_id'));
        let frm = $('#news_create_form'),
            formData = new FormData(frm.get(0));
        $.ajax({
            contentType: false, // важно - убираем форматирование данных по умолчанию
            processData: false,
            type: frm.attr('method'),
            url: frm.attr('action'),
            data: formData,
            dataType: 'json',
            success: function (data) {
                if (data.status === 201) {
                    $('.event_news').prepend(data.text);
                    $('#id_text', '.news-form').val('');
                } else if (data.status === 100) {
                    $('#id_news', '.news-form').val('');
                    $('#id_text', '.news-form').val('');
                    let $li = $('[data-id='+data.id+']');
                    $li.find('.text').html(data.text.replace(/\n/g, "<br />"));
                } else {
                    $('.error_news').html(data.text)
                }
            },
            error: function(data) {

            }
        });
    });


    /**
     * Подписка на пользователей
     * Мод. Subscribers
     *
     */
    $body.on('click', '.add_to_friend', function(){
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

    $('#edit_profile_form').on('click', function(e){
        e.preventDefault();
        ajax_validate_form($('#main_info'), e)
    });

    $('#settings').on('click', function(e){
        e.preventDefault();
        ajax_validate_form($('#settings'), e)
    });

    /**
     * Ajax для формы редактирования профиля
     *
     */
    function ajax_validate_form($form, e){
        let data = $form.serialize();

        $.ajax({
            type: "POST",
            url: "/profile/edit",
            data: data,
            dataType: 'json',
            success: function(data) {
                ajax_validate_form_data($form, data);
            }
        });
    }

    /**
     * Обработка данных валидации
     *
     */
    function ajax_validate_form_data($form, data) {
        $('input').removeClass('is-invalid');
        $('.invalid-feedback').remove();
        if (data !== '200') {
            let errors = data;
            for (let i = 0; i < errors.length; i++) {
                let $field = $form.find(errors[i].key);
                $field.addClass('is-invalid');
                $field.after('<div class="invalid-feedback">' + errors[i].desc + '</div>');
            }
        }
    }

    /**
     * Показать подписчиков и подписки
     *
     */
    $('.all_subscribers, .all_followers').on('click', function () {
        custom_dialogs({});

        let url = $(this).data('url');
        $.ajax({
            url: url,
            success: function (data) {
                $('.content_paginator').html(data);
                new Waypoint.Infinite({
                    element: $('.infinite-container')[0],
                    reverse: true
                });
            }
        });
    });

    /**
     * Смена аватара или миниатюры
     *
     */
    $('.change_avatar, .change_mini').on('click', function () {
        let url = $(this).data('url'),
            title = $(this).html();

        let beforeClose_ = function(){
            $('.help_image_div').imgAreaSelect({
                remove: true
            });
            $('#output_image').imgAreaSelect({
                remove: true
            });
        };

        custom_dialogs({selector: $( "#dialog_img" ), title: title, beforeClose_: beforeClose_});

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
        let $select_roles = $('.select_roles');
        $.ajax({
            url: '/groups/find_subscribers',
            type: 'POST',
            data: {
                'value': $(this).val(),
                'group_id': $select_roles.data('group_id'),
            },
            success: function (data) {
                if (data) {
                    let r_side = $('.right_side_select_roles', $select_roles).empty();
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
    $('.select_roles').on('click', '.add_to_editor',  function () {
        let $this = $(this);
        $.ajax({
            url: '/groups/add_to_editor',
            type: 'POST',
            data: {
                'user': $(this).parent('li').data('id'),
                'group_id': $('.select_roles').data('group_id'),
            },
            success: function (data) {
                if (data === 200) {
                    $this.text('Разжаловать');
                    $this.addClass('add_to_subscriber').removeClass('add_to_editor');
                    $('.left_side_select_roles').append($this.closest('li'));
                } else {
                    // TODO заполнить error
                }
            }
        });
    });

    /**
     * Перевод из редактора в подписчика
     *
     */
    $('.select_roles').on('click', '.add_to_subscriber', function () {
        let $this = $(this);
        $.ajax({
            url: '/groups/add_to_subscribers',
            type: 'POST',
            data: {
                'user': $(this).parent('li').data('id'),
                'group_id': $('.select_roles').data('group_id'),
            },
            success: function (data) {
                if (data === 200) {
                    $this.text('Добавить редактора');
                    $this.addClass('add_to_editor').removeClass('add_to_subscriber');
                    $('.right_side_select_roles').append($this.closest('li'));
                } else {
                    // TODO заполнить error
                }
            }
        });
    });

    /**
     * Удаление из подписчиков
     *
     * Удалять могут только админы
     *
     */
    $('.delete', '.select_roles').on('click', function () {
        let $this = $(this);
        $.ajax({
            url: '/groups/delete_subscribers',
            type: 'POST',
            data: {
                'user': $(this).parent('li').data('id'),
                'group_id': $('.select_roles').data('group_id'),
            },
            success: function (data) {
                if (data === 200) {
                    $this.closest('li').remove();
                } else {
                    // TODO заполнить error
                }
            }
        });
    });



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
                    let topOffset = $(this).css(pos).offset().top;
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
                if (data === 200) {
                } else {
                    // TODO заполнить error
                }
            }
        });
    }


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
                if (data === 200) {

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
    $body.on('click', '.message_block', function () {
        let $message_block = $('.message_block');
        $message_block.removeClass('selected_message');
        $message_block.find('.additional_block').hide();
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
    $body.on('click', '.edit_message', function () {
        let $message_block = $(this).closest('.message_block'),
            id_message = $message_block.attr('message_id'),
            message_text = $message_block.find('.message').text(),
            $input = $('#chat-message-input');
        $input.val(message_text);
        $input.addClass('edited_message');
        $input.attr('message_id', id_message);
    });


    /**
     * Обработка удаления сообщений
     *
     */
    $body.on('click', '.delete_message', function () {
        let message_id = $(this).closest('.message_block').attr('message_id');
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
        let url = '';
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
            let username = $this.parent().find('.username').html(),
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
            let id = $this.val();
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
    $body.on('click', '.add_to_chat', function () {
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
                let obj = $('input[type=checkbox]', '.add_chat_form_subscribers'), iter = '', added_users = [];
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
            let obj = $('.user', '.add_chat_wrapper'),
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
    $body.on('click', '.leave_room', function () {
        var room_id = $('.messages', '.messages_wrapper').data('room_id');
        $.ajax({
            url: '/chats/decline_room',
            type: 'POST',
            dataType: 'json',
            data: {
                'room_id': room_id
            },
            success: function (data) {
                if (data['status'] === 200) {
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
    $body.on('click', '.delete_from_chat', function () {
        $('.delete_from_chat_wrapper').show();
        $('.cancel', '.deleted_users').off('click').on('click', function () {
            $('.delete_from_chat_wrapper').hide();
        });

        $('.delete', '.delete_from_chat_wrapper').off('click').on('click',function () {
            let room_id = $('.messages', '.messages_wrapper').data('room_id'),
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
            let dialog_name = $('[name=dialog_name]').val(),
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
        let room_id = $(this).closest('.dialog_last_info').data('room_id');
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
        let room_id = $(this).closest('.dialog_last_info').data('room_id');
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
    });

    /**
     * Поиск города в кастомном селекте
     *
     */
    $('.custom_select').on('input', '.find_city', function () {
        let city_name = $(this).val();
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
                data.forEach(function(data) {
                    $('.custom_select_items').append("<span  class='select_item' data-city_id="+ data.pk +">" + data.fields.city + "</span>");
                });
            }
        });
    });

    /**
     * Установка значения в кастомном селекте
     *
     */
    $('.custom_select_items').off('click').on('click', '.select_item', function () {
        $(this).parent().find('.select_item').removeClass('selected');
        if ($(this).hasClass('go_out'))
            return;
        $(this).addClass('selected');
        $('[name="select_city"]', '.custom_select').val($(this).html());
    });

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
                    window.location.replace('/events/' + data.url);
                } else {
                    if (data.status === 400) {
                        $('#'+data.wrong_field).addClass('is-invalid');
                    }
                    ajax_validate_form_data($form, data);
                }
            }
        });
    }

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
        let categories = '';
        $('.custom_multiply_select').find('.remove_categories').each(function (key, value) {
            categories += ($(this).data('categories_id')).toString() + ',';
        });
        indexed_array['categories'] = categories;

        indexed_array = get_geo_values(indexed_array, $('.select_bounds_yamaps'));

        $.map(unindexed_array, function(n, i){
            indexed_array[n['name']] = n['value'];
        });

        let url = new URL(window.location.href),
            group_id = url.searchParams.get("group_id");
        if (group_id !== null || group_id !== '' ) {
            indexed_array['group_id'] = group_id;
        }

        return indexed_array;
    }


    $('.auth_block_header .popup_header_menu_down').on('click', function(){
        $(this).hide();
        $('.popup_header_menu_up').show();
        $('.popup_menu_block').show();

    });

    $('.auth_block_header .popup_header_menu_up').on('click', function(){
        $(this).hide();
        $('.popup_header_menu_down').show();
        $('.popup_menu_block').hide();
    });

    /**
     * Кастомный мультиселект
     *
     */
    $('.custom_multiply_select_items').on('click', '.multiply_select_item', function () {
        if ($('.remove_categories').length < 3) {
            $('.custom_multiply_select').append('<span class="remove_categories" data-categories_id="' +
                $(this).data('categories_id') + '" data-categories_description="'+ $(this).data('categories_description') +'">'+ $(this).html() + ' </span>');
            $(this).remove();

            // Добавить проверку на редактирование
            var categories = [];
            $('.custom_multiply_select').find('.remove_categories').each(function (key, value) {
                var $selector = $('.column_'+ (key + 1), '.recommend_image_block'), this_category;

                if ($selector.attr('category_name') !== $(this).data('categories_description')) {
                    var is_new = true;
                    $selector.attr('category_name', $(this).data('categories_description'));
                    $selector.css('display', 'block');
                }

                let category = $(this).data('categories_description');
                if (category && category !== '') {
                    categories += category + ',';
                    this_category = category;
                }
                if (is_new) {
                    $.ajax({
                        type: "POST",
                        url: '/events/get_images_by_categories',
                        data: {
                            'categories': this_category
                        },
                        dataType: 'json',
                        success: function(data) {
                            $selector.show();
                            $('.category_name_column_'+ (key + 1), '.recommend_image_block').html(category);
                            for (let i = 0; i < data.length; i ++) {
                                $selector.append('<div class="rec_im"><img src="/' + data[i] + '"></div>');
                            }
                        }
                    });
                }
            });
            let category_array = categories.split(',');

            set_default_image_to_event(category_array)
        }
    });

    /**
     * Динамическая подгрузка дефолтных картинок для событий
     *
     */
    $('.custom_multiply_select').on('click', '.remove_categories', function () {
        $('.custom_multiply_select_items').append('<span class="multiply_select_item" data-categories_id="'+
            $(this).data('categories_id') + '" data-categories_description="'+ $(this).data('categories_description') +'">'+ $(this).html()+'</span>');
        $(this).remove();

        // Добавить проверку на редактирование
        let categories = [];
        $('.custom_multiply_select').find('.remove_categories').each(function (key, value) {
            let $selector = $('.column_'+ (key + 1), '.recommend_image_block'), this_category;
            if ($selector.attr('category_name') !== $(this).data('categories_description')) {
                var is_new = true;
            }

            let category = $(this).data('categories_description');
            if (category && category !== '') {
                categories += category + ',';
                this_category = category;
            }
            if (is_new) {
                let x = $('[category_name = ' + this_category + ']').html();
                $('.column_'+ (key + 1), '.recommend_image_block').html(x);
                $selector.attr('category_name', $(this).data('categories_description'));
            }
        });

        if (categories.length === 0) {
            $('.recommend_img', '.recommend_image_block').each(function () {
                $(this).attr('category_name', '');
                $(this).attr('image_name', '');
                $(this).css('display', 'none');
                $(this).find('.rec_im').remove();
            });
            $('.event_avatar').attr('src', '/media/avatar_event_default/default.png');
            return
        } else {
            let category_array = categories.split(','), flag, i = 1, j = 0, category_array_ = category_array.slice();

            for (i; i < 4; i++) {  // Нумерация с единицы
                flag = false;
                let $selector = $('.column_' + i, '.recommend_image_block');
                for (j = 0; j < category_array.length; j++) {
                    if ($selector.attr('category_name') === category_array[j]) {
                        delete category_array[j];
                        flag = true;
                    }
                }
                if (flag === false) {
                    $selector.attr('category_name', '');
                    $selector.attr('image_name', '');
                    $selector.css('display', 'none');
                    $selector.find('.rec_im').remove();
                }
            }

            set_default_image_to_event(category_array_)
        }
    });

    function set_default_image_to_event(category_array) {
        let json = {}, image_name = '';
        for (let i = 0; i < category_array.length; i++) {
            if (category_array[i] !== '') {
                image_name = $('[category_name = ' + category_array[i] + ']').attr('category_name');
                json[category_array[i]] = image_name;
            }
        }
        $.ajax({
            type: "POST",
            url: '/events/change_default_image',
            data: {
                'json': JSON.stringify(json)
            },
            dataType: 'json',
            success: function(data) {
                $('.event_avatar').attr('src', '/media/avatar_event_default/'+ data.image);
                $('.recommend_img', '.recommend_image_block').each(function (key, value) {
                    $(this).attr('image_name', data.image_names[key]);
                });
            }
        });
    }


    /**
     * Подписчики события
     *
     */
    // TODO ПЕРЕДЕЛАТь
    $('.see_all_event_subscribers').on('click', function () {
        $( "#dialog" ).dialog({
            title: 'Подписчики события',
            height: '400',
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
                    let topOffset = $(this).css(pos).offset().top;
                    if (topOffset < 0) {
                        $(this).css('top', pos.top - topOffset);
                    }
                }
            },
            open: function () {
                $('.black_bg').show();
            },
            close: function(){
                $('.black_bg').hide();
            }
        }).dialog('open');

        let url = $(this).data('url');
        $.ajax({
            url: url,
            success: function (data) {
                $('.content_paginator').html(data);
                new Waypoint.Infinite({
                    element: $('.infinite-container')[0],
                    reverse: true
                });
            }
        });
    });

    /**
     * удаление события
     *
     */
    $('.restore_or_delete_event').off('click').on('click', function () {
        let $this = $(this);
        let buttons = [
            {
                text: "Да",
                icon: "ui-icon-heart",
                click: function() {
                    delete_event($this);
                }
            },
            {
                text: "Нет",
                icon: "ui-icon-heart",
                click: function() {
                    $(this).dialog( "close" );
                }
            }
        ];
        custom_dialogs({selector: $( "#dialog_confirm" ), title: 'Подтвердите действие', width: '200', height: '100',
            buttons: buttons});
    });

    /**
     * Удаление события
     *
     */
    function delete_event($button) {
        $.ajax({
            url: '/events/delete_event',
            type: 'POST',
            data: {
                'event_id': $('#dialog_confirm').data('event_id'),
                'is_restore':  $button.data('is_restore')
            },
            success: function (data) {
                if (data === 200) {
                } else {
                    // TODO заполнить error
                }
            }
        });
    }


    /**
     * удаление новости
     *
     */
    $('.event_news').on('click', '.delete_news', function () {
        let $this = $(this),
            buttons = [
                {
                    text: "Да",
                    icon: "ui-icon-heart",
                    click: function() {
                        delete_event_news($this);
                        $( this ).dialog( "close" );
                    }
                },
                {
                    text: "Нет",
                    icon: "ui-icon-heart",
                    click: function() {
                        $( this ).dialog( "close" );
                    }
                }
            ];
        custom_dialogs({selector: $( "#dialog_confirm" ), title: 'Подтвердите действие', width: '200', height: '100',
            buttons: buttons});
    });

    /**
     * Удаление новости (метод ajax)
     * @$button - кнопка удаления на элементе
     *
     */
    function delete_event_news($button) {
        $.ajax({
            url: '/events/delete_event_news',
            type: 'POST',
            data: {
                'event_id': $('#dialog_confirm').data('event_id'),
                'news_id':  $button.closest('li').data('id')
            },
            success: function (data) {
                if (data === "200") {
                    $('[data-id='+$button.closest('li').data('id')+']').remove();
                } else {
                    // TODO заполнить error
                }
            }
        });
    }

    /**
     * Редактирование новости, обработчик кнопк
     *
     */
    $('.event_news').on('click', '.edit_news', function () {
        let $news = $(this).closest('li'), news_id = $news.data('id');
        $('#id_text', '.news-form').val($('div.text', $news).html().replace(/<br\s*[\/]?>/gi, "\n")); // выставляем \n вместо br
        $('#id_news', '.news-form').val(news_id);
    });

    $('.load_events', '.load_events_container').on('click', function () {
        let url = '/main_app/get_new_events/',
            last_update = $('.event_item:first', '.infinite-container').data('last_update');
        $.ajax({
            url: url,
            type: 'POST',
            data: get_event_filter('event_filter_block', last_update),
            success: function (data) {
                if (data) {
                    let parent = $('.content_paginator_events');
                    $(data).find('.event_item').each(function () {
                        let id  = $(this).data('event_id');
                        $('[data-event_id = "'+id+'"]', parent).remove();
                        $('.infinite-container', parent).prepend($(this))

                    });
                } else {
                    // TODO заполнить error
                }
            }
        });
    });

    $('#date', '.event_filter_block').on('change', function () {
        if (parseInt($(this).val()) === 6) {
            $('#date').closest('div').append('<input class="date_filter" name="date_filter">')
            $('.date_filter').datetimepicker({
                timepicker:false,
                format:'Y-m-d'
            });
        } else {
            $('.date_filter').remove();
        }
    });

    $body.on('click', '[data-like="like"]', function () {
        let $this = $(this),
            event_id = $this.closest('.event_item_block').data('event_id');
        $.ajax({
            url: '/events/like',
            type: 'POST',
            data: {
                'event_id': event_id
            },
            dataType: 'json',
            success: function (data) {
                if (data === 200) {
                    $this.attr('data-like', 'unlike');
                    $this.attr('src', '/static/img/star.svg');   // TODO Убрать хардкод

                    let count = parseInt($this.siblings('.like_count').html());
                    $this.siblings('.like_count').html(count + 1);
                } else if (data === 400) {
                    window.location.replace('/accounts/login/?next=');
                }
            }
        });
    });


    $body.on('click', '[data-like="unlike"]', function () {
        let $this = $(this),
            event_id = $this.closest('.event_item_block').data('event_id');
        $.ajax({
            url: '/events/unlike',
            type: 'POST',
            data: {
                'event_id': event_id
            },
            dataType: 'json',
            success: function (data) {
                if (data === 200) {
                    $this.attr('data-like', 'like');
                    $this.attr('src', '/static/img/star_empty.svg');   // TODO Убрать хардкод

                    let count = parseInt($this.siblings('.like_count').html());
                    $this.siblings('.like_count').html(count - 1);
                } else if (data === 400) {
                    window.location.replace('/accounts/login/?next=');
                }
            }
        });
    });


    /**
     * Показать приглашенных или с запросом на подписку
     *
     */
    $('.event_send, .event_invite').on('click', function () {
        custom_dialogs({});

        let url = $(this).data('url');
        $.ajax({
            url: url,
            success: function (data) {
                $('.content_paginator', '#dialog').html(data);
                debugger;
                new Waypoint.Infinite({
                    element: $('.infinite-container', '.content_paginator')[0],
                    reverse: true
                });
            }
        });
    });

    function custom_dialogs(option) {
        let $selector = option.selector || $('#dialog'); // если  0,"", false то присвоит 200
        let title = option.title || 'Подписчики';
        let height = option.height || '700';
        let width = option.width || '500';
        let beforeClose_ = option.beforeClose_ || '';
        let buttons = option.buttons || '';

        $selector.dialog({
            title: title,
            height: height,
            width: width,
            draggable: false,
            resizable: false,
            modal: true,
            autoOpen: false,
            beforeClose: beforeClose_,
            close: function() {
                $('.content_paginator', '#dialog').empty();
            },
            buttons: buttons,
            position: {
                my: 'center',
                at: 'center',
                collision: 'fit',
                using: function(pos) {
                    let topOffset = $(this).css(pos).offset().top;
                    if (topOffset < 0) {
                        $(this).css('top', pos.top - topOffset);
                    }
                }
            },
        }).dialog('open');
    }

});
