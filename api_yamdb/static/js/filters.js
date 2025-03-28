let titleCards = document.querySelectorAll("div.title-card");

let genres = document.querySelector("select.filters.genres");
let categories = document.querySelector("select.filters.categories");



function filterTitlesByGenreAndCategory() {
    let selectedGenreText = genres.options[genres.selectedIndex].text;
    let selectedCategoryText = categories.options[categories.selectedIndex].text;
    let isAllGenre = genres.options[genres.selectedIndex].text
        .toLowerCase()
        .includes("все");
    let isAllCategory = categories.options[categories.selectedIndex].text
        .toLowerCase()
        .includes("все");
    for (let card of titleCards) {
        let lastLi = card.querySelector("li:last-child")
        let secondLi = lastLi.previousElementSibling
        if (
            !(
                (lastLi.textContent.includes(selectedGenreText) || isAllGenre) &&
                (secondLi.textContent.includes(selectedCategoryText) || isAllCategory)
            )
        ) {
            card.style.display = 'none';
        } else {
            card.style.display = '';
        }
    }
}

genres.addEventListener("change", filterTitlesByGenreAndCategory);
categories.addEventListener("change", filterTitlesByGenreAndCategory);
