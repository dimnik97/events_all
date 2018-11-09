ymaps.ready(init);
var myMap, myPlacemark;
var myCollection;

// TODO дубл script.js
/**
 * Получение формы с кастомными модулями, например селект по городам
 *
 */
function get_form_with_custom_modules($form) {
    let unindexed_array = $form.serializeArray(),
        indexed_array = {};
    let location = $('#select-state').val() || '';
    indexed_array['location'] = location;

    if (typeof $('#select-tools').val() !== 'undefined')
        indexed_array['categories_'] = $('#select-tools').val().join(',');

    $.map(unindexed_array, function(n, i){
        indexed_array[n['name']] = n['value'];
    });

    let url = new URL(window.location.href),
        group_id = url.searchParams.get("group_id");
    if (group_id !== null || group_id !== '' ) {
        indexed_array['group_id'] = group_id;
    }

    return indexed_array;
}

function init() {
    myMap = new ymaps.Map('map', {
        center: [55.753994, 37.622093],
        zoom: 10,
        controls: []
    });
    myCollection = new ymaps.GeoObjectCollection();

    if (event_map === true) {
        set_center_by_city_name(city);
        ajax_get_events() ;  // Получение данных для карты
    }
    if (is_create === true || (is_edit === true)) {
        if (is_edit === true && geo_lat && geo_lng) {
            var coords = [parseFloat(geo_lat.replace(',', '.')), parseFloat(geo_lng.replace(',', '.'))];
            set_center_by_cords(coords);
            create_and_add_place_mark(coords, true);
        } else {
            set_center_by_city_name(city);
        }

        myMap.events.add('click', function (e) {
            var coords = e.get('coords');

            if (myPlacemark) {
                myPlacemark.geometry.setCoordinates(coords);
            }
            else {
                myPlacemark = createPlacemark(coords);
                myMap.geoObjects.add(myPlacemark);
                myPlacemark.events.add('dragend', function () {
                    getAddress(myPlacemark.geometry.getCoordinates());
                });
            }
            getAddress(coords);
        });

        // Определяем адрес по координатам (обратное геокодирование).
        function getAddress(coords) {
            myPlacemark.properties.set('iconCaption', 'поиск...');
            ymaps.geocode(coords).then(function (res) {
                var firstGeoObject = res.geoObjects.get(0), $data_span = $('.select_bounds_yamaps');

                $data_span.html(firstGeoObject.getAddressLine());
                $data_span.attr('data-lat', coords[0]);
                $data_span.attr('data-lng', coords[1]);
                myPlacemark.properties
                    .set({
                        iconCaption: [
                            firstGeoObject.getLocalities().length ? firstGeoObject.getLocalities() : firstGeoObject.getAdministrativeAreas(),
                            firstGeoObject.getThoroughfare() || firstGeoObject.getPremise()
                        ].filter(Boolean).join(', '),
                        // balloonContent: $('#id_name').val()
                    });
            });
        }
    } else if (is_view === true) {
        var coords = [parseFloat(geo_lat.replace(',', '.')), parseFloat(geo_lng.replace(',', '.'))];
        set_center_by_cords(coords);
        create_and_add_place_mark(coords, false);
    }

    function create_and_add_place_mark(coords, draggable) {
        myPlacemark = createPlacemark(coords);
        myPlacemark.geometry.setCoordinates(coords);

        ymaps.geocode(coords).then(function (res) {
            var firstGeoObject = res.geoObjects.get(0);
            myPlacemark.properties
                .set({
                    // iconCaption: $('.event_item').data('name'),
                    // balloonContent: $('.event_item').data('name'),
                });
            myPlacemark.options.set({draggable: draggable})
        });
        myMap.geoObjects.add(myPlacemark);
    }
}

/**
 * Выставляем центр карты по координатам
 *
 */
function set_center_by_cords(cords) {
    myMap.setCenter(cords, 13);
}

/**
 * Выставляем центр карты по имени города
 *
 */
function set_center_by_city_name(city_name) {
    ymaps.geocode(city_name, {
        results: 1
    }).then(function (res) {
        var firstGeoObject = res.geoObjects.get(0),
            coords = firstGeoObject.geometry.getCoordinates();
        myMap.setCenter(coords, 10);
    });
}

/**
 * Добавление точки, вешаем события при клике
 *
 */
function add_bounds(bounds) {
    var coords;
    if (typeof bounds.lat !== 'number' && typeof bounds.lng !== 'number') {
        coords = [parseFloat(bounds.lat.replace(',', '.')), parseFloat(bounds.lng.replace(',', '.'))];
    } else {
        coords = [bounds.lat, bounds.lng]
    }
    myPlacemark = createPlacemark_event_map(coords, bounds);

    myPlacemark.events.add('click', function (e) {
        $.ajax({
            url: '/events/' + e.get('target').properties.get('myid') + '?is_card_on_event_map=True',
            type: 'GET',
            dataType: 'json',
            success: function (data) {
                if (data) {
                    $('.event_card').html(data).show();
                }
            }
        });
    });
    myCollection.add(myPlacemark);
    myPlacemark.geometry.setCoordinates(coords);
}


/**
 * Создание метки карты
 *
 */
// Создание метки.
function createPlacemark(coords) {
    return new ymaps.Placemark(coords, {
    }, {
        preset: 'islands#violetDotIconWithCaption',
        draggable: true,
        iconColor: 'red'
    });
}

/**
 * Создание метки карты с id
 *
 */
function createPlacemark_event_map(coords, bounds) {
    return new ymaps.Placemark(coords, {
        myid: bounds.id,
    }, {
        preset: 'islands#violetDotIconWithCaption',
        draggable: false,
        iconColor: 'red'
    });
}

/**
 * Обработчик клика по фильтру
 *
 */
$('body').on('click', '.submit_event_map_filter', function(e){
    ajax_get_events();
});

/**
 * Ajax для формы EventForm (Редактирование)
 *
 */
function ajax_get_events() {
    $.ajax({
        url: '/main_app/get_events_map',
        type: 'POST',
        dataType: 'json',
        data: get_form_with_custom_modules($('.event_map_filter_block')),
        success: function (data) {
            if (data) {
                myCollection.removeAll();
                let i;
                for (i = 0; i <  data.length; i++) {
                    add_bounds({
                        'name': data[i].name,
                        'lat': data[i].lat,
                        'lng': data[i].lng,
                        'id': data[i].id,
                    })
                }
                myMap.geoObjects.add(myCollection);
            }
        }
    });
}


