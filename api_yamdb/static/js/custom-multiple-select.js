;(function() {
     // Получаем селекты с возможностью множественного выбора
    let allMultipleSelects = document.querySelectorAll("select[multiple]");

    // Скрываем оригинальные селекты
    allMultipleSelects.forEach(select => select.classList.add("hidden"));
    console.log("Мультивариантные селекты:")
    allMultipleSelects.forEach(select => console.log(select.getAttribute("class")))

    // Создаём счётчик, который позволит нам пронумеровать селекты
    let number = 0;

    // Создаём переменную, храняющую ссылку на активный селект
    let activeSelect;

    // Заменяем оригинальные селекты кастомными
    for (let select of allMultipleSelects) {

        // Получаем родительский элемент оригинального селекта
        let parent = select.parentElement;

        // Создаём кастомный селект
        let customSelect = document.createElement("div");
        customSelect.classList.add("custom-select", "multiple");

        // Присваиваем оригинальному и кастомному селекту свойство, по которому
        // кастомный селект будет находить оригинальный для изменения его значения
        select.dataset.number = ++ number;
        customSelect.dataset.number = number;

        for (let option of select.querySelectorAll("option")) {
            let text = option.text;
            let value = option.value;
            let selected = option.selected;

            console.log(selected)
            let customOption = document.createElement("div");
            customOption.classList.add("option");
            customOption.dataset.value = value;
            customOption.dataset.selected = false;
            customOption.textContent = text;
            if (selected) {
                customOption.classList.add("selected");
            }
            customOption.addEventListener("click", selectOption)
            customSelect.append(customOption);
        }
        parent.append(customSelect);
        customSelect.setAttribute('tabindex', '0');
        customSelect.addEventListener("blur", saveSelection)
        customSelect.addEventListener("keydown", cancelPostFocusEdits)
    }

    function selectOption(event) {
        let options = [...this.parentElement.children];
        let parent = this.parentElement;
        activeSelect = parent;
        this.classList.toggle("selected");

        if (!(event.ctrlKey || event.shiftKey)) {
            options.forEach(option => {
                if (option !== this) option.classList.remove("selected");
              });
        }
    }

    function saveSelection(event) {
        let options = [...this.children];

        options.forEach(option => option.dataset.selected = option.classList.contains("selected"));
        // options.forEach(option => console.log(option.dataset.selected))
        let originalOptions = [...document.querySelector(`select[multiple][data-number="${this.dataset.number}"]`).options];
        for (let index=0; index < originalOptions.length; index++) {
            let isSelected = options[index].dataset.selected === "true";
            originalOptions[index].selected = isSelected;
        }
    }

    function cancelPostFocusEdits(event) {
        if (event.key === "Escape") {
            event.preventDefault()
            let options = [...this.children];
            options.forEach(option => {
                if (option.dataset.selected === "true") {
                    option.classList.add("selected");
                } else {
                    option.classList.remove("selected");
                }
            })
        }
    }
})();