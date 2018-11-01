$(document).ready(function() {

    $.ajax({
        url: $('.content_paginator_users').data('url'),
        async: false,
        success: function (data) {
            $('.infinite-container_users').append(data);
            waypoints_init();
        }
    });
    /**
     * Поиск группы по вводимому тексту
     *
     */
    $('.find_groups').on('input', function () {
        find_groups()
    });

    function find_users() {
        let url = $('.content_paginator_users').data('url');
        $.ajax({
            url: url,
            type: 'POST',
            data: get_filter('users_filter'),
            success: function (data) {
                debugger;
                if (data) {
                    $('.infinite-container_users').html(data);
                    waypoints_init(get_filter('users_filter'));
                } else {
                    // TODO заполнить error
                }
            }
        });
    }
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


    /**
     * Инициализация плагина инфинити скролла, что-то вроде дата тейбла
     *
     */
    function waypoints_init(filter) {
        new Waypoint.Infinite({
            element: $('.infinite-container_users')[0],
            more: '.infinite-more-link_users',
            items: '.infinite-item',
            reverse: false,
            post: true,
            filter: filter
        });
    }
});