document.addEventListener('DOMContentLoaded', function () {
    var selectMenus = document.querySelectorAll('.select-menu');

    selectMenus.forEach(function (selectMenu) {
        var selectBtn = selectMenu.querySelector('.select-btn');
        var optionsList = selectMenu.querySelector('.options');

        selectBtn.addEventListener('click', function () {
            selectMenu.classList.toggle('active');
        });
    });
});

// Отображение карты Yandex
let mapVisible = false;

function toggleMap() {
    let mapDiv = document.getElementById('map');
    let overlay = document.getElementById('overlay');

    if (!mapVisible) {
        mapDiv.style.display = 'block';
        overlay.style.display = 'block';
        mapDiv.classList.add('fade-in');
    } else {
        mapDiv.classList.remove('fade-in');
        mapDiv.classList.add('fade-out');
        overlay.classList.add('fade-out');

        mapDiv.classList.remove('fade-out');
        overlay.classList.remove('fade-out');
        setTimeout(() => {
            mapDiv.style.display = 'none';
            overlay.style.display = 'none';
        }, 500);
    }

    mapVisible = !mapVisible;
}

function init() {
    let map = new ymaps.Map("map", {
        center: [55.78695085570812, 49.12842339349504],
        zoom: 11,
    });

    restaurantsData.forEach(function (restaurant) {
        // Формируем строку для геокодирования
        let query = restaurant.district + ', ' + restaurant.address;

        // Получаем координаты через геокодирование
        ymaps.geocode(query).then(
            function (res) {
                let coordinate = res.geoObjects.get(0).geometry.getCoordinates();

                // Создаем метку
                let placemark = new ymaps.Placemark(coordinate, {
                    hintContent: restaurant.name,
                    balloonContent: "Название: " + restaurant.name + "<br>Район: " + restaurant.district + "<br>Адрес: " + restaurant.address +
                        "<br><a href='" + restaurant.profileUrl + "'>Перейти в профиль ресторана</a>",
                });

                // Добавляем метку на карту
                map.geoObjects.add(placemark);
            },
            function (err) {
                console.error('Ошибка геокодирования для ресторана: ' + restaurant.name);
            }
        );
    });

    // Удалите ненужные элементы управления картой (если требуется)
    map.controls.remove('geolocationControl');
    map.controls.remove('searchControl');
    map.controls.remove('trafficControl');
    map.controls.remove('typeSelector');
    map.controls.remove('fullscreenControl');
    map.controls.remove('zoomControl');
    map.controls.remove('rulerControl');
}

ymaps.ready(init);

document.getElementById('overlay').addEventListener('click', function () {
    if (mapVisible) {
        toggleMap();
    }
});