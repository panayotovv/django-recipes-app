document.addEventListener('DOMContentLoaded', () => {
    // --- Intersection Observer for card animations ---
    const cards = document.querySelectorAll('.recipe-card');

    const observer = new IntersectionObserver(entries => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.remove('opacity-0', 'translate-y-10');
            }
        });
    }, { threshold: 0.1 });

    cards.forEach(card => observer.observe(card));

    // --- Favorite button AJAX ---
    const favBtns = document.querySelectorAll(".favoriteBtn");

    favBtns.forEach(favBtn => {
        favBtn.addEventListener("click", () => {
            const recipeId = favBtn.dataset.recipeId;

            fetch(`/recipe/${recipeId}/favorite/`, {
                method: "POST",
                headers: {
                    "X-CSRFToken": getCookie("csrftoken"),
                    "Content-Type": "application/json"
                },
            })
            .then(response => response.json())
            .then(data => {
                if (data.liked) {
                    favBtn.textContent = "❤️";
                } else {
                    favBtn.textContent = "🤍";
                }
                // small animation
                favBtn.classList.add("scale-110");
                setTimeout(() => favBtn.classList.remove("scale-110"), 200);
            })
            .catch(error => console.error("Error:", error));
        });
    });

    // --- CSRF helper ---
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== "") {
            const cookies = document.cookie.split(";");
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.startsWith(name + "=")) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // --- Recipe search filter ---
    const searchInput = document.getElementById('recipeSearch');

    if (searchInput) {
        searchInput.addEventListener('input', () => {
            const query = searchInput.value.toLowerCase();

            cards.forEach(card => {
                const titleElem = card.querySelector('h1, h3'); // support h1 or h3
                if (!titleElem) return;

                const title = titleElem.textContent.toLowerCase();
                card.style.display = title.includes(query) ? '' : 'none';
            });
        });
    }
});
