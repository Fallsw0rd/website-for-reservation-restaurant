const kitchenData = [
    {id: 1, x: 120, y: 30},
];

const toiletData = [
    {id: 1, x: 300, y: 30},
];

function renderKitchen() {
    const kitchenContainer = document.querySelector(".kitchen-container");

    kitchenData.forEach(item => {
        const kitchenElement = document.createElement('div');
        kitchenElement.className = 'kitchen';
        kitchenElement.style.left = `${item.x}px`;
        kitchenElement.style.top = `${item.y}px`;

        const labelSpan = document.createElement('span');
        labelSpan.className = 'label';
        labelSpan.textContent = 'Кухня';

        kitchenElement.appendChild(labelSpan);

        kitchenContainer.appendChild(kitchenElement);
    });
}

function renderToilet() {
    const toiletContainer = document.querySelector(".toilet-container");

    toiletData.forEach(item => {
        const toiletElement = document.createElement('div');
        toiletElement.className = 'toilet';
        toiletElement.style.left = `${item.x}px`;
        toiletElement.style.top = `${item.y}px`;

        const labelSpan = document.createElement('span');
        labelSpan.className = 'label';
        labelSpan.textContent = 'Уборная';

        toiletElement.appendChild(labelSpan);

        toiletContainer.appendChild(toiletElement);
    });
}


function updateTableStatus() {
    const tables = document.querySelectorAll('.table');
    const enteredGuests = parseInt(document.getElementById('id_count_guess').value);
    let backgroundStop = document.getElementById('background-stop')

    if (!isNaN(enteredGuests)){
        backgroundStop.style.display = 'none';
    } else {
        backgroundStop.style.display = 'flex';
    }

    tables.forEach(table => {
        const tableCapacity = parseInt(table.dataset.capacity);
        if (isNaN(enteredGuests)) {
            table.classList.add('reserved-guests');
        } else {
            if (enteredGuests > tableCapacity || !(tableCapacity - 1 <= enteredGuests)) {
                table.classList.add('reserved-guests');
            } else {
                table.classList.remove('reserved-guests');
            }
        }
    });
}

async function updateTableStatusDateTime() {
    const tables = document.querySelectorAll('.table');

    for (const table of tables) {
        const tableId = table.dataset.table;
        const date = document.getElementById('id_date').value;
        const time = document.getElementById('id_time').value;
        let csrfToken = $('[name=csrfmiddlewaretoken]').val();
        if (date && time) {
            try {
                const response = await $.ajax({
                    url: '/restaurants/check_reservation/',
                    type: 'POST',
                    data: {
                        table_id: tableId,
                        date: date,
                        time: time,
                        csrfmiddlewaretoken: csrfToken,
                    },
                });
                if (response.is_reserved) {
                    table.classList.add('reserved-datetime');
                } else {
                    table.classList.remove('reserved-datetime');
                }
            } catch (error) {
            }
        }
    }
}


document.getElementById('id_time').addEventListener('input', () => {
    updateTableStatus();
    updateTableStatusDateTime();
});
document.getElementById('id_date').addEventListener('input', () => {
    updateTableStatus();
    updateTableStatusDateTime();
});
document.getElementById('id_count_guess').addEventListener('input', () => {
    updateTableStatus();
    updateTableStatusDateTime();
});

function openModal(content, tableId, capacity, imagePath) {
    const selectedTable = document.querySelector(`.table[data-table="${tableId}"]`);
    if (selectedTable.classList.contains('reserved-datetime') || selectedTable.classList.contains('reserved-guests')) {
        const messageContainer = document.getElementById('reservation-message');
        messageContainer.textContent = 'Стол не подходит';
        messageContainer.style.opacity = '90%';
        messageContainer.style.display = 'flex';
        setTimeout(() => {
            messageContainer.style.opacity = '0%';
            setTimeout(() => {
                messageContainer.style.display = 'none';
            }, 500)
        }, 500);

        return;
    }
    const modal = document.getElementById('myModal');
    const modalContent = document.getElementById('modalContent');
    modalContent.innerHTML = `
            <p>Стол №${content}</p>
            <label class="label-style">Информация</label>
            <p>Вместимость: ${capacity}</p>
            <label>Фотография стола</label>
            <img src="/media/${imagePath}" alt="Стол ${tableId}">`;

    modalContent.style.padding = '20px';

    document.getElementById('selectedTableId').value = tableId;

    modal.style.display = 'flex';
}

function closeModal() {
    const modal = document.getElementById('myModal');
    modal.style.display = 'none';
}

window.onload = function () {
    renderKitchen();
    renderToilet();
    updateTableStatus();
    updateTableStatusDateTime();
};

let currentTab = 0;
showTab(currentTab);

function showTab(n) {
    let x = document.getElementsByClassName("tab");
    x[n].style.display = "block";
    if (n === 0) {
        document.getElementById("prevBtn").style.display = "none";
    } else {
        document.getElementById("prevBtn").style.display = "inline";
    }
    if (n === (x.length - 1)) {
        document.getElementById("nextBtn").innerHTML = "Забронировать";
    } else {
        document.getElementById("nextBtn").innerHTML = "Далее";
    }
    fixStepIndicator(n)
}

function nextPrev(n) {
    const modal = document.getElementById('myModal');
    let x = document.getElementsByClassName("tab");

    x[currentTab].style.display = "none";
    currentTab = currentTab + n;

    if (currentTab >= x.length) {
        modal.style.display = 'none';
        return false;
    }

    modal.style.display = 'none';
    showTab(currentTab);
}

function fixStepIndicator(n) {
    let i, x = document.getElementsByClassName("step");
    for (i = 0; i < x.length; i++) {
        x[i].className = x[i].className.replace(" active", "");
    }
    x[n].className += " active";
}

$(document).ready(function(){
    let restaurant_id = document.getElementById('go-rest').dataset.rest;
    $('#id_date').on('change', function(){
        let selectedDate = $(this).val();
        // Отправка запроса на сервер для получения обновленного списка времени
        $.ajax({
            url: '/restaurants/get_time_choices/',
            type: 'GET',
            data: {
                'selected_date': selectedDate,
                'restaurant_id': restaurant_id
            },
            success: function(data){
                // Обновление вариантов в поле выбора времени
                $('#id_time').empty();
                $.each(data.choices, function(key, value){
                    $('#id_time').append($('<option>').text(value).attr('value', value));
                });
            }
        });
    });
});