    $('.select-menu .option').on('click', function () {
        let selectedValue = $(this).data('value');
        let $selectMenu = $(this).closest('.select-menu');

        // Находим input внутри текущей формы и устанавливаем ему значение
        $selectMenu.find('input[type="hidden"]').val(selectedValue);

        // Скрываем выпадающий список и убираем класс "active"
        $selectMenu.removeClass('active');
        $selectMenu.find('.options').removeClass('open');

        // Автоматическая отправка формы
        $selectMenu.submit();
    });



document.addEventListener('DOMContentLoaded', function () {
    const selectBtns = document.querySelectorAll('.select-btn');
    // Вкладки с фильтрами
    selectBtns.forEach(function (btn) {
        btn.addEventListener('click', function (event) {
            const options = this.nextElementSibling;

            selectBtns.forEach(function (otherBtn) {
                if (otherBtn !== btn) {
                    otherBtn.parentNode.classList.remove('active');
                }
            });

            this.parentNode.classList.toggle('active');

            event.stopPropagation();
        });
    });

    document.addEventListener('click', function () {
        const selectMenus = document.querySelectorAll('.select-menu');
        selectMenus.forEach(function (menu) {
            menu.classList.remove('active');
        });
    });
    // Вкладки с фильтрами

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
        center: [55.788784294749334, 49.12401459277338],
        zoom: 11,
    });

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