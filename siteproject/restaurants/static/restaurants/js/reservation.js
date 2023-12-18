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

function renderTables() {
    const tablesContainer = document.querySelector(".tables");

    tablesData.forEach(table => {
        const tableElement = document.createElement('div');
        tableElement.className = 'table';
        tableElement.style.left = `${table.x}px`;
        tableElement.style.top = `${table.y}px`;

        if (table.reserved) {
            tableElement.classList.add('reserved');
            tableElement.addEventListener('click', () => {
                alert(`Столик ${table.id} уже забронирован`);
            });
        } else {
            tableElement.addEventListener('click', () => {
                openModal(`Стол № ${table.id}`, table.id, table.capacity, table.imagePath);
            });
        }

        const capacitySpan = document.createElement('span');
        capacitySpan.className = 'capacity';

        tableElement.appendChild(capacitySpan);

        tablesContainer.appendChild(tableElement);
    });
}

function openModal(content, tableId, capacity, imagePath) {
    const modal = document.getElementById('myModal');
    const modalContent = document.getElementById('modalContent');
    modalContent.innerHTML = `
            <p>${content}</p>
            <label class="label-style">Информация</label>
            <p>Вместимость: ${capacity}</p>
            <label>Фотография стола</label>
            <img src="${imagePath}" alt="Стол ${tableId}">`;

    modalContent.style.padding = '20px';

    modal.style.display = 'flex';
}

function closeModal() {
    const modal = document.getElementById('myModal');
    modal.style.display = 'none';
}

window.onload = function () {
    renderTables();
    renderKitchen();
    renderToilet();
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
    if (n === 1 && !validateForm()) return false;
    x[currentTab].style.display = "none";
    currentTab = currentTab + n;
    if (currentTab >= x.length) {
        document.getElementById("bron-form").submit();
        return false;
    }
    modal.style.display = 'none';
    showTab(currentTab);
}

function validateForm() {
    let x, y, i, valid = true;
    x = document.getElementsByClassName("tab");
    y = x[currentTab].getElementsByTagName("input");
    for (i = 0; i < y.length; i++) {
        if (y[i].value === "") {
            y[i].className += " invalid";
            valid = false;
        }
    }
    return valid;
}

function fixStepIndicator(n) {
    let i, x = document.getElementsByClassName("step");
    for (i = 0; i < x.length; i++) {
        x[i].className = x[i].className.replace(" active", "");
    }
    x[n].className += " active";
}