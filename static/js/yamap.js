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

    let location = $('#location').find('.selected');
    unindexed_array.push({name: 'location', value: location.data('city_id')});
    let categories = '';
    $('.custom_multiply_select').find('.remove_categories').each(function (key, value) {
        categories += ($(this).data('categories_id')).toString() + ',';
    });
    indexed_array['categories'] = categories;

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
        ajax_get_events()   // Получение данных для карты
    }
    if (is_create === true || (is_edit === true)) {
        if (is_edit === true && geo_lat && geo_lng) {
            var coords = [parseFloat(geo_lat.replace(',', '.')), parseFloat(geo_lng.replace(',', '.'))];
            set_center_by_cords(coords);
            create_and_add_place_mark(coords, true);
        } else {
            set_center_by_city_name($('.custom_select_items').find('.selected').html());
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
function set_center_by_cords(cords) {
    myMap.setCenter(cords, 13);
}

function set_center_by_city_name(city_name) {
    ymaps.geocode(city_name, {
        results: 1
    }).then(function (res) {
        var firstGeoObject = res.geoObjects.get(0),
            coords = firstGeoObject.geometry.getCoordinates();
        myMap.setCenter(coords, 10);
    });
}

function add_bounds(bounds) {
    var coords;
    if (typeof bounds.lat !== 'number' && typeof bounds.lng !== 'number') {
        coords = [parseFloat(bounds.lat.replace(',', '.')), parseFloat(bounds.lng.replace(',', '.'))];
    } else {
        coords = [bounds.lat, bounds.lng]
    }
    myPlacemark = createPlacemark_event_map(coords, bounds);

    myPlacemark.events.add('click', function () {
        $.ajax({
            url: '/events/' + myPlacemark.properties._data.myid + '?is_card_on_event_map=True',
            type: 'GET',
            dataType: 'json',
            success: function (data) {
                if (data) {
                    $('.event_card').html(data)
                }
            }
        });
    });
    myCollection.add(myPlacemark);
    myPlacemark.geometry.setCoordinates(coords);
}

// Создание метки.
function createPlacemark(coords) {
    return new ymaps.Placemark(coords, {
    }, {
        preset: 'islands#violetDotIconWithCaption',
        draggable: true,
        iconColor: 'red'
    });
}

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
 * Ajax для формы EventForm (Редактирование)
 *
 */
$('body').on('click', '.submit_event_map_filter', function(e){
    ajax_get_events();
});


function ajax_get_events() {
    $.ajax({
        url: '/main_app/get_events_map',
        type: 'POST',
        data: get_form_with_custom_modules($('.event_map_filter_block')),
        dataType: 'json',
        success: function (data) {
            if (data) {
                myCollection.removeAll();
                set_center_by_city_name(data.user_city);
                let i;
                for (i = 0; i <  data.events.length; i++) {
                    add_bounds({
                        'name': data.events[i].name,
                        'lat': data.events[i].lat,
                        'lng': data.events[i].lng,
                        'id': data.events[i].id,
                    })
                }
                myMap.geoObjects.add(myCollection);
            }
        }
    });
}


