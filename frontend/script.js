document.addEventListener("DOMContentLoaded", function () {
    const searchInput = document.querySelector(".search-box");
    const papersGrid = document.querySelector(".papers-grid");

    searchInput.addEventListener("keyup", async function (event) {
        if (event.key === "Enter") {
            const query = searchInput.value.trim();
            if (!query) return;

            try {
                const response = await fetch("http://127.0.0.1:8000/search_papers/", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ query: query }),
                });

                if (!response.ok) {
                    throw new Error("Failed to fetch papers");
                }

                const data = await response.json();
                displayPapers(data.papers);
            } catch (error) {
                console.error("Error fetching research papers:", error);
            }
        }
    });

    function displayPapers(papers) {
        papersGrid.innerHTML = ""; // Clear previous results

        if (papers.length === 0) {
            papersGrid.innerHTML = "<p>No research papers found.</p>";
            return;
        }

        papers.forEach(paper => {
            const paperCard = document.createElement("div");
            paperCard.classList.add("paper-card");
            paperCard.innerHTML = `<h3 class="paper-title">${paper.title}</h3><p>${paper.abstract}</p>`;
            papersGrid.appendChild(paperCard);
        });
    }
});
