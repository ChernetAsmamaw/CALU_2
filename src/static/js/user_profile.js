const saveButton = document.getElementById('saveButton');
saveButton.addEventListener('click', function () {
    const email = document.getElementById('email').value;
    const message = 'Saved!';

    Swal.fire({
        title: 'Profile Updated!',
        text: message,
        icon: 'success',
        confirmButtonColor: '#3085d6',
        confirmButtonText: 'OK'
    });
});