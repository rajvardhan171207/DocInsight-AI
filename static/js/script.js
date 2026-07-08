document.addEventListener("DOMContentLoaded", () => {

    // Loading Screen
    const form = document.querySelector("form");

    if (form) {

        form.addEventListener("submit", () => {

            const loading = document.getElementById("loading-screen");
            if (loading) {
                loading.style.display = "flex";
            }

            const btn = form.querySelector("button");

            if (btn) {
                btn.disabled = true;
                btn.innerHTML = "Analyzing...";
            }

        });

    }

    // Animate Statistics Cards
    const cards = document.querySelectorAll(".stat-card");

    cards.forEach((card, index) => {

        card.style.opacity = "0";
        card.style.transform = "translateY(20px)";

        setTimeout(() => {

            card.style.transition = "all 0.5s ease";
            card.style.opacity = "1";
            card.style.transform = "translateY(0)";

        }, index * 200);

    });

});