ymaps.ready(init);
var myMap, myPlacemark;

function init() {
    myMap = new ymaps.Map('map', {
        center: [55.753994, 37.622093],
        zoom: 10
    });

    if (is_create === true || (is_edit === true)) {
        if (is_edit === true) {
            var coords = [parseFloat(geo_lat.replace(',', '.')), parseFloat(geo_lng.replace(',', '.'))];
            set_center_by_cords(coords);
            create_and_add_place_mark(coords, true);
        } else {
            set_center_by_city_name($('.custom_select_items').find('.selected').html());
        }

            debugger;
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
                        balloonContent: $('#id_name').val()
                    });
            });
        }
    } else if (is_view === true) {
        var coords = [parseFloat(geo_lat.replace(',', '.')), parseFloat(geo_lng.replace(',', '.'))];
        set_center_by_cords(coords);
        create_and_add_place_mark(coords, false);
    }

    // Создание метки.
    function createPlacemark(coords) {
        return new ymaps.Placemark(coords, {
            iconCaption: 'поиск...'
        }, {
            preset: 'islands#violetDotIconWithCaption',
            draggable: true,
            iconColor: 'red'
        });
    }

    function create_and_add_place_mark(coords, draggable) {
        myPlacemark = createPlacemark(coords);
        myPlacemark.geometry.setCoordinates(coords);

        ymaps.geocode(coords).then(function (res) {
            var firstGeoObject = res.geoObjects.get(0);
            myPlacemark.properties
                .set({
                    iconCaption: $('.event_item').data('name'),
                    balloonContent: $('.event_item').data('name'),
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

