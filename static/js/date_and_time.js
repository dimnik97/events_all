var arr=[
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
// Принимает на вход дату в формате ISO  example: "2018-10-14T12:54:32.001485+00:00"
function transform_event_date_start_end(iso_date_start, iso_date_end=null, event_id) {
    var date_start = new Date(iso_date_start), result_time = '', result_date = '';
    result_time = 'c ' + addZero(date_start.getHours()) + ':' + addZero(date_start.getMinutes());
    result_date = date_start.getDate() + ' ';
    var date_end = new Date(iso_date_end);
    result_time = result_time + ' до ' + addZero(date_end.getHours()) + ':' + addZero(date_end.getMinutes());

    if (date_start.getDate() !== date_end.getDate()) {
        result_date = result_date + '-' + date_end.getDate();
    }

    if (arr[date_start.getMonth()] === arr[date_end.getMonth()]) {
        result_date = result_date + arr[date_start.getMonth()];
    } else {
        result_date = result_date + ' ' + arr[date_start.getMonth()] + ' -' + arr[date_end.getMonth()];
    }

    let $parent = $('[data-event_id="'+event_id+'"]');
    $('.event_time', $parent).html(result_time);
    $('.event_date', $parent).html(result_date);
}


function transform_news_date(iso_date, news_id) {
    let date_start = new Date(iso_date), result;
    result = date_start.getDate() + ' ' + arr[date_start.getMonth()] +
        ' ' + addZero(date_start.getHours()) + ':' + addZero(date_start.getMinutes());
    let $parent = $('li[data-id="'+news_id+'"]');
    $('.news_date', $parent).html(result);
}

function addZero(i) {
    if (i < 10) {
        i = "0" + i;
    }
    return i;
}
