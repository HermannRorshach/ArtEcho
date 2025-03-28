// Получаем все простые селекты
let allSimpleSelects = document.querySelectorAll("select:not([multiple])");

// Получаем селекты с возможностью множественного выбора
let allMultipleSelects = document.querySelectorAll("select[multiple]");

// Скрываем оригинальные селекты
allSimpleSelects.forEach(select => select.classList.add("hidden"));
allMultipleSelects.forEach(select => select.classList.add("hidden"));

// Создаём счётчик, который позволит нам пронумеровать селекты
let number = 0;

// Заменяем оригинальные селекты кастомными
for (let select of allSimpleSelects) {
    let options = select.querySelectorAll("option");
    // let selectedIndex = select.selectedIndex;

    // Получаем родительский элемент оригинального селекта
    let parent = select.parentElement;

    // Создаём кастомный селект
    let customSelect = document.createElement("div");
    customSelect.classList.add("custom-select");
    // Задаём начальное свойство селекта, которое показывает, что все
    // элементы, кроме выбранного должны быть скрыты
    customSelect.dataset.isHidden = true;
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
        customOption.textContent = text;
        if (selected) {
            customOption.classList.add("selected");
            if (option.value === "") {
                customOption.classList.add("empty-value")
            }
        }

        customOption.classList.add("hidden")
        customOption.addEventListener("click", hiddenSwitch)
        customOption.addEventListener("click", selectOption)
        customSelect.append(customOption);
    }
    parent.append(customSelect);
    // console.log(parent)
    customSelect.setAttribute('tabindex', '0');
    customSelect.addEventListener("blur", hiddenSwitch)
}

function hiddenSwitch() {
    console.log(this)
    let options = this.classList.contains("option") ? this.parentElement.children : this.children;
    let parent = options[0].parentElement;
    // console.log(options)
    if (parent.dataset.isHidden == "true") {
        for (let option of options) {
            option.classList.remove("hidden")
        }
        parent.dataset.isHidden = false;
    } else {
        for (let option of options) {
            option.classList.add("hidden")
        }
        parent.dataset.isHidden = true;
    }
}

function selectOption() {
    let options = [...this.parentElement.children];
    let parent = this.parentElement;
    for (let option of options) {
        if (option != this) {
            option.classList.remove("selected");
        }
        this.classList.add("selected")
    }
    let originalSelect = document.querySelector(`select[data-number="${parent.dataset.number}"]`);
    // console.log("originalSelect =", originalSelect, "parent.dataset.number =", parent.dataset.number)
    currentIndex = options.indexOf(this);
    originalSelect.selectedIndex = currentIndex;
    console.log(originalSelect.selectedIndex, originalSelect.value)
}