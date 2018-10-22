find_events();
/**
 * Лента активных событий
 *
 */
function find_events() {
    let url = '/main_app/active_user_events?id=' + id;
    $.ajax({
        url: url,
        type: 'POST',
        success: function (data) {
            if (data) {
                $('.content_paginator_active').html(data);
                let element = $('.infinite-container', '.content_paginator_active')[0], more = '.infinite-more-link_active';

                var infinite1 = new Waypoint.Infinite({
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


/**
 * Лента завершенных событий
 *
 */
$('.activate_panel3_events', '.nav-tabs').on('click', function () {
    let url = '/main_app/ended_user_events?id=' + id;
    $.ajax({
        url: url,
        type: 'POST',
        success: function (data) {
            if (data) {
                $('.content_paginator_ended').html(data);
                let element = $('.infinite-container', '.content_paginator_ended')[0], more = '.infinite-more-link_ended';
                var infinite2 = new Waypoint.Infinite({
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


/**
 * Лента моих событий
 *
 */
$('.activate_panel2_events', '.nav-tabs').on('click', function () {
    let url = '/main_app/user_events?id=' + id;
    $.ajax({
        url: url,
        type: 'POST',
        success: function (data) {
            if (data) {
                $('.content_paginator_user_events').html(data);
                let element = $('.infinite-container', '.content_paginator_user_events')[0], more = '.infinite-more-link_user_events';
                var infinite3 = new Waypoint.Infinite({
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
