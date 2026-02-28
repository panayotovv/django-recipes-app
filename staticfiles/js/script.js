document.addEventListener('DOMContentLoaded', () => {
    const cards = document.querySelectorAll('.recipe-card');

    const observer = new IntersectionObserver(entries => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.remove('opacity-0', 'translate-y-10');
            }
        });
    }, { threshold: 0.1 });

    cards.forEach(card => observer.observe(card));

    const searchInput = document.getElementById('recipeSearch');

    if (searchInput) {
        searchInput.addEventListener('input', () => {
            const query = searchInput.value.toLowerCase();

            cards.forEach(card => {
                const titleElem = card.querySelector('h1, h3');
                if (!titleElem) return;

                const title = titleElem.textContent.toLowerCase();
                card.style.display = title.includes(query) ? '' : 'none';
            });
        });
    }

    const input = document.getElementById('image-upload');
    const fileName = document.getElementById('file-name');

    input.addEventListener('change', function() {
      if (input.files.length > 0) {
          fileName.textContent = input.files[0].name;
      } else {
          fileName.textContent = 'No file chosen';
      }
  });
});
