if (type === 'detail') {
    find_events();

    /**
     * Лента активных событий
     *
     */
    function find_events() {
        let url = '/main_app/get_group_events?id=' + id;
        $.ajax({
            url: url,
            type: 'POST',
            success: function (data) {
                if (data) {
                    $('.content_paginator').html(data);
                    let element = $('.infinite-container', '.content_paginator')[0], more = '.infinite-more-link';

                    new Waypoint.Infinite({
                        element: element,
                        more: more,
                        items: '.event_item',
                        reverse: false,
                        post: true
                    });
                } else {
                    // TODO заполнить error
                }
            }
        });
    }
} else if (type === 'all') {
    /**
     * Запрос на получение данных (изначальное)
     *
     */
    $(document).ready(function() {
        $.ajax({
            url: $('.content_paginator_groups').data('url'),
            async: false,
            success: function (data) {
                $('.infinite-container_groups').append(data);
                waypoints_init();
            }
        });
    });

    /**
     * Получение параметров фильтрации для POST запроса
     *
     */
    function get_filter(selector) {
        let unindexed_array = $('.'+selector).serializeArray(),
            indexed_array = {};

        $.map(unindexed_array, function(n){
            indexed_array[n['name']] = n['value'];
        });
        return indexed_array;
    }

    $('.groups_filter', '.tab-content').on('submit', function (e) {
        e.preventDefault();  // Отмена стандартного обработчика сабмита
    });
    /**
     * Инициализация плагина инфинити скролла, что-то вроде дата тейбла
     *
     */
    function waypoints_init(filter) {
        new Waypoint.Infinite({
            element: $('.infinite-container_groups')[0],
            more: '.infinite-more-link_groups',
            items: '.infinite-item_groups',
            reverse: false,
            post: true,
            filter: filter
        });
    }

    /**
     * Поиск группы по вводимому тексту
     *
     */
    $('.find_groups').on('input', function () {
        find_groups()
    });

    /**
     * Поиск группы (При нажатии чекбокса "Все")
     *
     */
    $('.all_groups').on('change', function () {
        find_groups()
    });

    function find_groups() {
        let url = $('.content_paginator_groups').data('url');
        $.ajax({
            url: url,
            type: 'POST',
            data: get_filter('groups_filter'),
            success: function (data) {
                if (data) {
                    $('.infinite-container_groups').html(data);
                    waypoints_init(get_filter('groups_filter'));
                } else {
                    // TODO заполнить error
                }
            }
        });
    }

    /**
     * Лента приглашений и заявок
     *
     */
    $('.activate_panel2_groups', '.nav-tabs').on('click', function () {
        let url = $('.content_paginator_invite', '#panel2').data('url');
        $.ajax({
            url: url,
            type: 'POST',
            success: function (data) {
                if (data) {
                    $('.content_paginator_invite').html(data);
                    let element = $('.infinite-container_invite', '.content_paginator_invite')[0],
                        more = '.infinite-more-link_invite';
                    new Waypoint.Infinite({
                        element: element,
                        more: more,
                        items: '.infinite-item_invite',
                        reverse: false,
                        post: true
                    });
                } else {
                    // TODO заполнить error
                }
            }
        });
    });
}

/**
 * Предупреждение
 *
 */
$('#id_type', '#groups_form').on('change', function () {
    open_dialog();
    if ($(this).val() === '1') {
        status = 'открытыми'
    } else {
        status = 'закрытыми'
    }
    $( "#dialog_confirm" ).html('Все события этой группы будут считаться ' + status)
});

/**
 * Завяка успешно отправлена
 *
 */
$('.send_an_application').on('click', function () {
    let group_id = $(this).data('group_id');
    $.ajax({
        url: '/groups/send_an_application',
        type: 'POST',
        data: {
            'group_id': group_id
        },
        success: function (data) {
            if (data === '200') {
                open_dialog();
                $( "#dialog_confirm" ).html('Заявка успешно отправлена');
                $('.send_an_application').remove();
            } else {
                // TODO заполнить error
            }
        }
    });
});

/**
 * Открытие диалогового окна
 *
 */
function open_dialog() {
    $( "#dialog_confirm" ).dialog({
        title: 'Предупреждение',
        height: '100',
        width: '200',
        draggable: false,
        resizable: false,
        modal: true,
        autoOpen: false,
        buttons: [
            {
                text: "ОК",
                icon: "ui-icon-heart",
                click: function() {
                    $( this ).dialog( "close" );
                }
            },
        ],
    }).dialog('open');
}


/**
 * Отменить заявку
 *
 */
$('.accept', '.sends').on('click', function () {
    let group_id = $('.select_roles').data('group_id'),
        user_id = $(this).closest('li').data('id'),
        url = 'accept';
    ajax_to_cancel_or_accept_subscribers(group_id, user_id, url, $(this));
});

/**
 * Отменить заявку
 *
 */
f();
function f() {
    $('.cancel', '.sends, .invited').off('click').on('click', function () {
        let group_id = $('.select_roles').data('group_id'),
            user_id = $(this).closest('li').data('id'),
            url = 'cancel';
        ajax_to_cancel_or_accept_subscribers(group_id, user_id, url, $(this));
    });
}

/**
 * Ajax для всего этого
 *
 */
function ajax_to_cancel_or_accept_subscribers(group_id, user_id, url, button) {
    $.ajax({
        url: '/groups/' + url,
        type: 'POST',
        data: {
            'group_id': group_id,
            'user_id': user_id
        },
        success: function (data) {
            if (data === '200') {
                if (url === 'accept') {
                    $('.right_side_select_roles').append(button.closest('li').clone());
                    let li = $('li:last', '.right_side_select_roles');
                    li.find('.accept').remove();
                    li.find('.cancel').remove();
                    li.append('<button class="add_to_editor">Добавить редактора</button> ' +
                        '<button class="delete">Удалить из группы</button>');
                    button.closest('li').remove();
                } else if (url === 'cancel') {
                    button.closest('li').remove();
                }
            } else {
                // TODO заполнить error
            }
        }
    });
}


/**
 * Сбор данных и отправка ajax-ом запросов на добавление в группу
 *
 */
$('.send_invitation', '.add_users_autocomplete').off('click').on('click', function () {
    let obj = $('.user', '.added_users'),
        added_users = '',
        group_id = $('.select_roles').data('group_id');

    obj.each(function () {
        added_users += ($(this).find('span').data('id')).toString() + ' ';
    });

    $.ajax({
        url: '/groups/invite',
        type: 'POST',
        dataType: 'json',
        data: {
            'added_users': added_users,
            'group_id': group_id
        },
        success: function (data) {
            if (data.status === 200) {
                let arr = data.added_array.split(' ');
                arr.pop();
                let user_id = '', user_name = '';
                for (let i = 0; i < arr.length; i++) {
                    user_id = arr[i];
                    user_name = $('[data-id='+user_id+']', '.added_users').html()
                    $('.invited').append('<li data-id="'+user_id+'"> ' + user_name +
                        ' <button class="cancel">Отменить приглашение</button>' +
                        '</li>')
                }
                f();
            } else {
                // TODO заполнить error
            }
        }
    });
});



