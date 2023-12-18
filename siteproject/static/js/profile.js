document.getElementById('edit').addEventListener('click', function () {
    enableEdit();
});

function enableEdit() {
    let form = document.querySelector('.rectangle-info');
    let inputs = form.getElementsByTagName('input');

    for (let i = 0; i < inputs.length; i++) {
        inputs[i].removeAttribute('readonly');
        inputs[i].style.background = '#fff';
        inputs[i].style.cursor = 'text';
    }

    // Показать кнопку "Сохранить" и скрыть кнопку "Редактировать"
    document.getElementById('edit').style.display = 'none';
    document.getElementById('confirm').style.display = 'inline-block';
}

$(document).ready(function () {
    $("#change-avatar-btn").click(function () {
        // Trigger click on the hidden file input
        $("#avatar-form").find("input[type='file']").click();
    });

    // Listen for changes in the file input
    $("#avatar-form").find("input[type='file']").change(function () {
        // Check if the file input has a value (i.e., a file is selected)
        if ($(this).val()) {
            // Automatically submit the form when a file is selected
            $("#avatar-form").submit();
        }
    });
});