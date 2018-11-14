$(document).ready(function() {

    /**
     * Для первой подгрузки подписок пользователя
     *
     */
    $.ajax({
        url: $('.content_paginator_subscribers', '.tab-content').data('url'),
        async: false,
        type: 'GET',
        success: function (data) {
            $('.infinite-container_subscribers').append(data);
            waypoints_init();
        }
    });
    /**
     * Поиск группы по вводимому тексту
     *
     */
    $('.find_users').on('input', function () {
        find_users()
    });

    /**
     * Ajax для вкладок
     *
     */
    $('.activate_panel2_users, .activate_panel3_users', '.nav-tabs').on('click', function () {
        let panel_id = $(this).find('a').attr('href'),
            $panel = $(panel_id);
        if ($(this).hasClass('active'))
            return false;
        $('.find_users').val('');
        let url = $('.content_pag', $panel).data('url');

        $.ajax({
            url: url,
            async: false,
            type: 'GET',
            success: function (data) {
                $('.infinite_cont', $panel).html(data);
                waypoints_init($('.content_pag', $panel), {});
            }
        });
    });

    /**
     * Ajax для поиска, один метод на 3 функции
     *
     */
    function find_users() {
        let filter = {
                'search': true,
                'value': $('.find_users', '.users_filter').val()
            },
            $tab = $('.tab-pane.active', '.tab-content'),
            url = $('.content_pag', $tab).data('url');
        $.ajax({
            url: url,
            type: 'POST',
            data: filter,
            success: function (data) {
                if (data) {
                    $('.infinite_cont', $tab).html(data);
                    let container = $('.content_pag', $tab);
                    waypoints_init(container ,filter);
                } else {
                    $('.infinite_cont', $tab).html('');
                }
            }
        });
    }
    /**
     * Инициализация плагина инфинити скролла, что-то вроде дата тейбла
     *
     */
    function waypoints_init($container, filter) {
        $container = $container || $('.content_paginator_subscribers', '.tab-content');
        new Waypoint.Infinite({
            element: $('.infinite_cont', $container)[0],
            more: $('.infinite-more-link_users', $container)[0],
            items: '.infinite-item',
            reverse: false,
            post: true,
            filter: filter,
            more_by_class: true,
        });
    }
});