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
   let previousSelection = new Map();

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
           customOption.addEventListener("click", selectOption);
           customSelect.append(customOption);
       }
       parent.append(customSelect);
       customSelect.setAttribute('tabindex', '0');
       customSelect.addEventListener("focus", storePreviousSelection);
       customSelect.addEventListener("blur", saveSelection);
       customSelect.addEventListener("keydown", handleKeyboardNavigation);
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
       let originalOptions = [...document.querySelector(`select[multiple][data-number="${this.dataset.number}"]`).options];
       for (let index = 0; index < originalOptions.length; index++) {
           let isSelected = options[index].dataset.selected === "true";
           originalOptions[index].selected = isSelected;
       }
   }

   function storePreviousSelection(event) {
       let options = [...this.children];
       previousSelection.set(this, options.map(option => option.classList.contains("selected")));
   }

   function handleKeyboardNavigation(event) {
       let options = [...this.children];
       let focusedIndex = options.findIndex(option => option === document.activeElement);

       switch (event.key) {
           case "ArrowDown":
               event.preventDefault();
               if (focusedIndex < options.length - 1) {
                   options[focusedIndex + 1].focus();
               }
               break;
           case "ArrowUp":
               event.preventDefault();
               if (focusedIndex > 0) {
                   options[focusedIndex - 1].focus();
               }
               break;
           case "Home":
               event.preventDefault();
               options[0].focus();
               break;
           case "End":
               event.preventDefault();
               options[options.length - 1].focus();
               break;
           case "Tab":
               saveSelection.call(this);
               break;
           case "a":
               if (event.ctrlKey) {
                   event.preventDefault();
                   options.forEach(option => option.classList.add("selected"));
               }
               break;
           case "Enter":
           case " ":
               if (event.ctrlKey) {
                   event.preventDefault();
                   let focusedOption = document.activeElement;
                   if (focusedOption && focusedOption.classList.contains("option")) {
                       focusedOption.classList.toggle("selected");
                   }
               }
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
               break;
       }
   }
})();