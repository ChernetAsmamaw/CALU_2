document.getElementById("login-form").addEventListener("submit", function(event) {
    var termsCheckbox = document.getElementById("terms-checkbox");

    if (!termsCheckbox.checked) {
      event.preventDefault(); // Prevent form submission

      Swal.fire({
        title: "Terms and Conditions",
        text: "Please agree to the terms and conditions before logging in.",
        icon: "warning",
        confirmButtonText: "OK"
      });
    }
  });