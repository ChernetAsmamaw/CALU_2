document.addEventListener("DOMContentLoaded", function () {
    const searchInput = document.getElementById("club-search-input");
    const clubs = document.querySelectorAll(".club-card");

    searchInput.addEventListener("input", function () {
        const searchTerm = searchInput.value.trim().toLowerCase();

        clubs.forEach((club) => {
            const clubName = club.querySelector(".club-name").textContent.toLowerCase();
            if (clubName.includes(searchTerm)) {
                club.style.display = "block";
            } else {
                club.style.display = "none";
            }
        });
    });
   });
