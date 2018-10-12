
find_events();
/**
 * Лента активных событий
 *
 */
function find_events() {
    var url = '/main_app/active_user_events?id=' + id;
    $.ajax({
        url: url,
        type: 'POST',
        success: function (data) {
            if (data) {
                $('.content_paginator_active').html(data);
                events_waypoints_init($('.content_paginator_active')[0], '.infinite-more-link_active');
            } else {
                // TODO заполнить error
            }
        }
    });
}

/**
 * Инициализация плагина инфинити скролла, что-то вроде дата тейбла
 *
 */
function events_waypoints_init(element, more) {
    var infinite_ = new Waypoint.Infinite({
        element: element,
        more: more,
        items: '.event_item',
        reverse: false,
        post: true
    });
    return;
}