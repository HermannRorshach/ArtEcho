;(function() {
    // Получаем все простые селекты
    let allSimpleSelects = document.querySelectorAll("select:not([multiple])");

    // Скрываем оригинальные селекты
    allSimpleSelects.forEach(select => select.classList.add("hidden"));

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
        customSelect.addEventListener("blur", setClassHidden)
    }

    function setClassHidden() {
        let options = [...this.children];
        options.forEach(option => option.classList.add("hidden"))
    }

    function hiddenSwitch() {
        console.log(this)
        let options = this.parentElement.children;
        let parent = this.parentElement;
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
        let originalSelect = document.querySelector(`select:not([multiple])[data-number="${parent.dataset.number}"]`);
        // console.log("originalSelect =", originalSelect, "parent.dataset.number =", parent.dataset.number)
        currentIndex = options.indexOf(this);
        originalSelect.selectedIndex = currentIndex;
        console.log(originalSelect.getAttribute("class"), originalSelect.selectedIndex, originalSelect.value)
    }

    // Добавляем обработчик keydown для кастомных селектов
// Новый обработчик клавиатуры (добавляется отдельно, не изменяя ваш код)
function initKeyboardNavigation() {
    document.querySelectorAll('.custom-select').forEach(select => {
        select.addEventListener('keydown', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                // Открываем/закрываем по Enter
                const clickEvent = new Event('click');
                this.querySelector('.option.selected').dispatchEvent(clickEvent);
                return;
            }

            if (e.key === 'Escape' && this.dataset.isHidden === 'false') {
                e.preventDefault();
                // Закрываем без изменений
                this.querySelectorAll('.option').forEach(opt => opt.classList.add('hidden'));
                this.dataset.isHidden = 'true';
                return;
            }

            // Работаем только с открытым списком
            if (this.dataset.isHidden === 'false') {
                const options = Array.from(this.querySelectorAll('.option:not(.hidden)'));
                const current = this.querySelector('.option.selected');
                let index = options.indexOf(current);

                if (e.key === 'ArrowDown') {
                    e.preventDefault();
                    if (index < options.length - 1) {
                        current.classList.remove('selected');
                        options[index + 1].classList.add('selected');
                        options[index + 1].focus();
                    }
                    return;
                }

                if (e.key === 'ArrowUp') {
                    e.preventDefault();
                    if (index > 0) {
                        current.classList.remove('selected');
                        options[index - 1].classList.add('selected');
                        options[index - 1].focus();
                    }
                    return;
                }
            }
        });
    });
}

// Инициализация после создания кастомных селектов
initKeyboardNavigation();
})();