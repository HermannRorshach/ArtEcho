let originalSelects = [...document.querySelectorAll("select:not([multiple])")];
let originalSelectValue = originalSelects.map(select => select.value);

console.log(originalSelectValue);

document.addEventListener("DOMContentLoaded", function () {

    function updateURLParams() {
        let flag = false;
        originalSelects.forEach((select, index) => {
            if (select.value != originalSelectValue[index]) {
                flag = true;
                originalSelectValue[index] = select.value;
            }
        });

        if (!flag) {
            return;
        }

        setTimeout(() => {
            const form = document.getElementById("filter-form");
            const params = new URLSearchParams(window.location.search);

            // Удаляем параметр page
            params.delete("page");

            // Обновляем параметры фильтров
            if (form.elements.genre.value) {
                params.set("genre", form.elements.genre.value);
            } else {
                params.delete("genre");
            }

            if (form.elements.category.value) {
                params.set("category", form.elements.category.value);
            } else {
                params.delete("category");
            }

            // Перенаправляем на новый URL с фильтрами, сбрасывая страницу
            window.location.search = params.toString();
        }, 100);  // небольшая задержка в 100 мс
    }

    // Слушаем изменения фильтров жанра и категории
    document.querySelectorAll(".filters.genres, .filters.categories").forEach(select => {
        select.addEventListener("change", updateURLParams);
    });
});
