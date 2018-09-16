
infinity_dialogs();

$('.find_dialogs').on('input', function () {
    infinity_dialogs($(this).val());
});

function infinity_dialogs(filter = null) {
    var url = $('.get_dialogs', '.dialogs').data('url');
    if (filter)
        url = url + '?name=' + filter;
    $.ajax({
        url: url,
        success: function (data) {
            $('.content_paginator_chat').html(data);
            var infinite = new Waypoint.Infinite({
                element: $('.infinite-container')[0]
            });
        }
    });
}

function request_dialog(url, url_type) {
    var url_ = 'dlg?' + url_type + '=' + url;

    $('.dialogs').hide();
    $('.back_to_dialogs').on('click', function () {
        $('.messages').remove();
        $('.dialogs').show();
        $('.back_to_dialogs').hide();
    });
    $.get(url_, function (data) {
        $('.back_to_dialogs').show();
        $('.messages_wrapper').append(data);
    });
}