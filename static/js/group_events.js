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

                    let infinite1 = new Waypoint.Infinite({
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

        $.map(unindexed_array, function(n, i){
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
        let infinite_ = new Waypoint.Infinite({
            element: $('.infinite-container_groups')[0],
            more: '.infinite-more-link_groups',
            items: '.infinite-item_groups',
            reverse: false,
            post: true,
            filter: filter
        });
        return;
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
        let url = '/main_app/user_events?id=' + id;
        $.ajax({
            url: url,
            type: 'POST',
            success: function (data) {
                if (data) {
                    $('.content_paginator_user_events').html(data);
                    let element = $('.infinite-container', '.content_paginator_user_events')[0], more = '.infinite-more-link_user_events';
                    let infinite3 = new Waypoint.Infinite({
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
$('.cancel', '.sends').on('click', function () {
    let group_id = $('.select_roles').data('group_id'),
        user_id = $(this).closest('li').data('id'),
        url = 'cancel';
    ajax_to_cancel_or_accept_subscribers(group_id, user_id, url, $(this));
});

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
