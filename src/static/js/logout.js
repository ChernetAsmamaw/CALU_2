function confirmLogout() {
    swal({
        title: "Logout",
        text: "Are you sure you want to log out?",
        icon: "warning",
        buttons: ["Cancel", "Logout"],
        dangerMode: true,
    }).then((willLogout) => {
        if (willLogout) {
            logout();
        }
    });
}

function logout() {
    // Perform a GET request to the logout route
    fetch("/logout", {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
        },
    })
        .then((response) => {
            if (response.redirected) {
                // Redirect to the home page after successful logout
                window.location.href = response.url;
            }
        })
        .catch((error) => {
            console.error("Logout failed", error);
        });
}
