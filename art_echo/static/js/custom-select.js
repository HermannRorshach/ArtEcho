document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".custom-select").forEach(select => {
        const selected = select.querySelector(".selected");
        const options = select.querySelector(".options");
        const optionElements = select.querySelectorAll(".option");
        const hiddenInput = select.nextElementSibling; // Скрытый input
        let selectedValues = [];

        selected.addEventListener("click", function () {
            options.classList.toggle("show");
        });

        optionElements.forEach(option => {
            option.addEventListener("click", function () {
                const value = this.dataset.value;
                if (selectedValues.includes(value)) {
                    selectedValues = selectedValues.filter(v => v !== value);
                    this.classList.remove("selected");
                } else {
                    selectedValues.push(value);
                    this.classList.add("selected");
                }

                selected.textContent = selectedValues.length
                    ? selectedValues.map(v => select.querySelector(`.option[data-value="${v}"]`).textContent).join(", ")
                    : "Выберите варианты";

                hiddenInput.value = selectedValues.join(",");
            });
        });

        document.addEventListener("click", function (e) {
            if (!select.contains(e.target)) {
                options.classList.remove("show");
            }
        });
    });
});
