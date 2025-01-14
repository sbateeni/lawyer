document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('searchInput');
    const searchButton = document.getElementById('searchButton');
    const categoryFilter = document.getElementById('categoryFilter');

    async function searchResources() {
        const searchTerm = searchInput.value;
        const category = categoryFilter.value;

        try {
            const response = await fetch('/api/legal-resources/search', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    search: searchTerm,
                    category: category
                })
            });

            const data = await response.json();
            if (data.status === 'success') {
                updateResults(data.results);
            }
        } catch (error) {
            console.error('Error searching resources:', error);
        }
    }

    searchButton.addEventListener('click', searchResources);
    searchInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') searchResources();
    });
});
