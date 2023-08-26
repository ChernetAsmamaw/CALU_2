//filter by search
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




//filter by category
document.addEventListener("DOMContentLoaded", function () {
    const categorySelect = document.getElementById("category-select");
    const clubs = document.querySelectorAll(".club-card"); // Add the "club-card" class to each club's container

    categorySelect.addEventListener("change", function () {
        const selectedCategory = categorySelect.value;

        clubs.forEach((club) => {
            const clubCategory = club.dataset.category; // Add a data-category attribute to each club card
            if (selectedCategory === "Type" || clubCategory === selectedCategory) {
                club.style.display = "block";
            } else {
                club.style.display = "none";
            }
        });
    });
});

