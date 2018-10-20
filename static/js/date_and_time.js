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

// /**
//  * Получение фильтра на дату
//  * TODO Обдумать на досуге
//  *
//  */
// function get_date_to_filter_old(unindexed_array) {
//     var start_date, end_date,
//         date = $('#date').val(), now = new Date();
//     if (date === "0") {
//         // Показывать все
//         return unindexed_array
//     } else if (date === "1") {
//         // Получение клиентского сегодня и завтра
//         start_date = new Date();
//         end_date = new Date();
//         end_date.setDate(end_date.getDate()+1);
//         end_date.setHours(0);
//         end_date.setMinutes(0);
//         end_date.setSeconds(0);
//     } else if (date === "2") {
//         // Получение клиентского завтра и послезавтра   Не работает
//         start_date = new Date().setDate(now.getDate()+1);
//         start_date.setHours(0);
//         start_date.setMinutes(0);
//         start_date.setSeconds(0);
//         end_date = start_date.setDate(now.getDate()+1);
//     } else if (date === "3") {
//         // период - неделя
//         var startDay = 1, d = now.getDay();
//         start_date = new Date(now.valueOf() - (d<=0 ? 7-startDay:d-startDay)*86400000);
//         end_date = new Date(start_date.valueOf() + 6*86400000);
//     } else if (date === "4") {
//         // период - месяц
//         start_date = new Date(now.getFullYear(), now.getMonth(), 1);
//         end_date = new Date(now.getFullYear(), now.getMonth() + 1, 0);
//     } else if (date === "5") {
//         // период - следующий месяц
//         start_date = new Date(now.getFullYear(), now.getMonth() + 1, 1);
//         end_date = new Date(now.getFullYear(), now.getMonth() + 2, now.getDay()-1);
//     } else if (date === "6") {
//         // датапикер
//
//         end_date = new Date();
//         end_date.setDate(end_date.getDate()+1);
//         end_date.setHours(0);
//         end_date.setMinutes(0);
//         end_date.setSeconds(0);
//     }
//     debugger;
//     let result_start_date = start_date.getFullYear() + '-'+ addZero(start_date.getMonth()) + '-' + addZero(start_date.getDate())
//         + ' ' + addZero(start_date.getHours()) + ':' + addZero(start_date.getMinutes());
//     let result_end_date = end_date.getFullYear() + '-'+ addZero(end_date.getMonth()) + '-' + addZero(end_date.getDate())
//         + ' ' + addZero(end_date.getHours()) + ':' + addZero(end_date.getMinutes());
//
//     unindexed_array.push({name: 'start_time', value: result_start_date});
//     unindexed_array.push({name: 'end_time', value: result_end_date});
//     return unindexed_array
// }