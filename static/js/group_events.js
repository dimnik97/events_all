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