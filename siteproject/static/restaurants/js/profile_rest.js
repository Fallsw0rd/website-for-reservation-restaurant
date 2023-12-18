function init() {
    let address = document.getElementById('restaurantAddress').innerText;
    let district = document.getElementById('district').innerText;
    let coordinate;
    let myGeocoder = ymaps.geocode(district + ', ' + address);
    myGeocoder.then(
        function (res) {
            coordinate = res.geoObjects.get(0).geometry.getCoordinates();
            let map = new ymaps.Map("map", {
                center: coordinate,
                zoom: 15,
            });

            let placemark = new ymaps.Placemark(coordinate, {}, {});
            map.controls.remove('geolocationControl');
            map.controls.remove('searchControl');
            map.controls.remove('trafficControl');
            map.controls.remove('typeSelector');
            map.controls.remove('fullscreenControl');
            map.controls.remove('zoomControl');
            map.controls.remove('rulerControl');

            map.geoObjects.add(placemark);
        },
        function (err) {
            alert('Ошибка');
        }
    );

}

ymaps.ready(init);

function openModal(imgUrl) {
    let modal = document.getElementById('myModal');
    let modalImg = document.getElementById('modalImg');
    modalImg.src = imgUrl;
    modal.classList.add('show');
}

function closeModal() {
    let modal = document.getElementById('myModal');
    modal.classList.remove('show');
}


// Получаем текущий день недели (0 - воскресенье, 1 - понедельник, и т.д.)
const currentDay = new Date().getDay();
document.getElementById(`day${currentDay}`).classList.add('current-day');