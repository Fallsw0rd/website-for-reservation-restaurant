    function submitForm() {
        document.getElementById("statisticsForm").submit();
    }

    function handleChange() {
        var dayValue = document.getElementById('day').value;
        var monthValue = document.getElementById('month').value;
        var yearValue = document.getElementById('year').value;

        if (dayValue || monthValue || yearValue) {
            submitForm();
        }
    }
    function showForm(option) {
        var dayForm = document.getElementById('dayForm');
        var monthForm = document.getElementById('monthForm');
        var yearForm = document.getElementById('yearForm');

        // Очистка значений при изменении выбора
        document.getElementById('day').value = "";
        document.getElementById('month').value = "";
        document.getElementById('year').value = "";

        if (option === 'day') {
            dayForm.style.display = 'block';
            monthForm.style.display = 'none';
            yearForm.style.display = 'none';
        } else if (option === 'month') {
            dayForm.style.display = 'none';
            monthForm.style.display = 'block';
            yearForm.style.display = 'none';
        } else if (option === 'year') {
            dayForm.style.display = 'none';
            monthForm.style.display = 'none';
            yearForm.style.display = 'block';
        } else {
            dayForm.style.display = 'none';
            monthForm.style.display = 'none';
            yearForm.style.display = 'none';
        }
    }