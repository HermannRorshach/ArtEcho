;(function() {
    // Синхронизируем выбранные опции в кастомном селекте с оригинальным
    // перед отправкой формы
    document.querySelector("form").addEventListener("submit", function() {
        document.querySelectorAll(".custom-select.multiple").forEach(customSelect => saveSelection.call(customSelect));
    });

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
    let previousSelection = new Map();

    // Создаём объект для хранения индекса начала последнего диапазона
    // для каждого из селектов
    let lastSelectionStarts = {};

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

            let customOption = document.createElement("div");
            customOption.classList.add("option");
            customOption.dataset.value = value;
            customOption.dataset.selected = selected ? "true" : "false";
            customOption.textContent = text;
            if (selected) {
                customOption.classList.add("selected");
            }
            customOption.setAttribute("tabindex", "-1");
            customOption.addEventListener("click", function(e) {
                if (e.ctrlKey) {
                    e.preventDefault();
                    e.stopPropagation();
                }
                selectOption.call(this, e);
            });
            customSelect.append(customOption);
        }
        parent.append(customSelect);
        customSelect.setAttribute('tabindex', '0');
        customSelect.addEventListener("focus", storePreviousSelection);
        customSelect.addEventListener("focus", () => console.log("Фокус сработал"));
        customSelect.addEventListener("mousedown", storePreviousSelection);
        customSelect.addEventListener("blur", saveSelection);
        customSelect.addEventListener("keydown", handleKeyboardNavigation);
    }

    function selectOption(event) {
        let options = [...this.parentElement.children];
        let parent = this.parentElement;
        activeSelect = parent;

        // Убираем класс .focused у всех опций
        options.forEach(option => {
            option.classList.remove('focused');
        });

        if (event.shiftKey) {
            let lastSelectedIndex = options.findIndex(option => option.classList.contains("selected"));
            let currentIndex = options.indexOf(this);
            if (lastSelectedIndex !== -1) {
                let [start, end] = [lastSelectedIndex, currentIndex].sort((a, b) => a - b);
                for (let i = start; i <= end; i++) {
                    options[i].classList.add("selected");
                }
                return;
            }
        }

        if (!(event.ctrlKey || event.shiftKey)) {
            options.forEach(option => {
                if (option !== this) option.classList.remove("selected");
            });
        }

        this.classList.toggle("selected");
    }


    function saveSelection(event) {
        let options = [...this.children];
        options.forEach(option => option.dataset.selected = option.classList.contains("selected"));
        let originalOptions = [...document.querySelector(`select[multiple][data-number="${this.dataset.number}"]`).options];
        for (let index = 0; index < originalOptions.length; index++) {
            let isSelected = options[index].dataset.selected === "true";
            originalOptions[index].selected = isSelected;
        }
   }

    function storePreviousSelection(event) {
        let options = [...this.children];
        previousSelection.set(this, options.map(option => option.classList.contains("selected")));
        console.log("Сохранено состояние:", previousSelection.get(this));

        // Устанавливаем фокус на первую опцию при получении фокуса
        if (options.length > 0) {
            options[0].focus();
        }
    }


    function selectAllFocused(option) {
        if (option.classList.contains("focused")) {
            let select = option.closest('.custom-select');
            let options = [...select.querySelectorAll('.option')];

            options.forEach(opt => {
                // Убираем класс .focused
                opt.classList.remove('focused');

                // Добавляем класс .selected
                opt.classList.add('selected');
            });
        }
    }


   function handleKeyboardNavigation(event) {
       let options = [...this.children];
       let focusedIndex = options.findIndex(option => option === document.activeElement);
       let selectionPoints = options
           .map((option, index) => (option.classList.contains("selected") ? index : -1))
           .filter(index => index !== -1);

       function selectRange(start, end) {
           for (let i = start; i <= end; i++) {
               options[i].classList.add("selected");
           }
       }

        switch (event.key) {
            case "ArrowDown":
            case "ArrowUp":
                event.preventDefault();
                let nextIndex = event.key === "ArrowDown" ? focusedIndex + 1 : focusedIndex - 1;

                if (nextIndex >= 0 && nextIndex < options.length) {
                if (event.shiftKey) {
                    let startIndex = lastSelectionStarts[this.dataset.number] !== undefined ? lastSelectionStarts[this.dataset.number] : focusedIndex;

                    if (!event.ctrlKey || (event.key === " " || event.key === "Enter")) {
                        lastSelectionStarts[this.dataset.number] = focusedIndex; // При Ctrl + Shift + Space обновляем начало диапазона
                    }

                    lastSelectionStarts[this.dataset.number] = undefined;

                    console.log("Выделение:", { startIndex, nextIndex });
                    console.log("lastSelectionStart =", lastSelectionStarts[this.dataset.number]);

                    selectRange(Math.min(startIndex, nextIndex), Math.max(startIndex, nextIndex));
                }

                    options[nextIndex].focus();
                }
                options.forEach(option => option.classList.remove("focused"));
                break;

            case "Enter":
            case " ":
                if (event.shiftKey && event.ctrlKey) {
                    // Обработка Ctrl + Shift + Enter / Space
                    event.preventDefault();
                    console.log("Сработало условие event.shiftKey && event.ctrlKey")

                    // Проверка, был ли уже выделен диапазон
                    if (lastSelectionStarts[this.dataset.number] === undefined) {
                        // Начало нового диапазона
                        lastSelectionStarts[this.dataset.number] = focusedIndex;
                        options[focusedIndex].classList.toggle("selected");
                        console.log("Мы в блоке lastSelectionStart === null", lastSelectionStarts[this.dataset.number])
                    } else {
                        // Конец текущего диапазона
                        console.log("Мы в блоке if lastSelectionStart === null else", "lastSelectionStart =", lastSelectionStarts[this.dataset.number], "focusedIndex =", focusedIndex)
                        selectRange(Math.min(lastSelectionStarts[this.dataset.number], focusedIndex), Math.max(lastSelectionStarts[this.dataset.number], focusedIndex));
                        lastSelectionStarts[this.dataset.number] = undefined;  // Сбросить, завершив диапазон
                    }
                    selectAllFocused(options[focusedIndex]);
                } else if (event.shiftKey) {
                    // Обработка Shift + Enter / Space для выделения диапазона
                    event.preventDefault();
                    if (selectionPoints.length) {
                        selectRange(
                            Math.min(selectionPoints[selectionPoints.length - 1], focusedIndex),
                            Math.max(selectionPoints[selectionPoints.length - 1], focusedIndex)
                        );
                    }
                    lastSelectionStarts[this.dataset.number] = undefined;
                    console.log("lastSelectionStart в блоке if event.shiftKey =", lastSelectionStarts[this.dataset.number])
                    // Выбираем все опции с классом focused, который добавляется опциям при команде
                    // ctrl + a
                    selectAllFocused(options[focusedIndex]);
                } else if (event.ctrlKey) {
                    // Обработка Ctrl + Enter / Space для переключения текущего элемента
                    event.preventDefault();
                    options[focusedIndex].classList.toggle("selected");
                    // Выбираем все опции с классом focused, который добавляется опциям при команде
                    // ctrl + a
                    selectAllFocused(options[focusedIndex]);
                } else {
                    options.forEach(option => option.classList.remove("focused"));
                }
                break;
        case "Home":
            event.preventDefault();
            options[0].focus();
            if (event.shiftKey) {
                if (event.ctrlKey) {
                    if (lastSelectedIndex !== -1) {
                        selectRange(0, lastSelectedIndex);
                    }
                } else {
                    selectRange(0, focusedIndex);
                }
            }
            options.forEach(option => option.classList.remove("focused"));
            break;

        case "End":
            event.preventDefault();
            options[options.length - 1].focus();
            if (event.shiftKey) {
                if (event.ctrlKey) {
                    if (lastSelectedIndex !== -1) {
                        selectRange(lastSelectedIndex, options.length - 1);
                    }
                } else {
                    selectRange(focusedIndex, options.length - 1);
                }
            }
            options.forEach(option => option.classList.remove("focused"));
            break;

        case "Escape":
            event.preventDefault();
            if (previousSelection.has(this)) {
                let prevSelection = previousSelection.get(this);
                options.forEach((option, index) => {
                    if (prevSelection[index]) {
                        option.classList.add("selected");
                    } else {
                        option.classList.remove("selected");
                    }
                });
            }
            options.forEach(option => option.classList.remove("focused"));
            console.log("Восстанавливаю состояние:", previousSelection.get(this));
            break;

        case "a":  // Обработка Ctrl + A
            if (event.ctrlKey) {
                event.preventDefault();
                options.forEach(option => {
                    option.classList.add("focused");
                });
                lastSelectionStarts[this.dataset.number] = undefined;  // Сбросить начало диапазона для текущего селекта
            }
            break;

    }
}


})();