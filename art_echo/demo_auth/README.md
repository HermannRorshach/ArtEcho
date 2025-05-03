demo_auth
Приложение demo_auth добавляет в Django-проект поддержку демонстрационного режима: ограниченного по правам пользователя, чьи действия не затрагивают реальные данные. Это особенно полезно для создания публичной демонстрации проекта без необходимости разворачивать отдельную среду.

Особенности:
- Реализация полностью синхронная, не требует асинхронных фреймворков.
- Подходит для хостинга на бесплатных тарифах, включая pythonanywhere.com.
- Не требует внешних зависимостей.
- Поддерживает автоматическую фильтрацию и сброс данных.

# 🚀 Пошаговое подключение
1. Добавьте приложение в INSTALLED_APPS

```python
# settings.py
INSTALLED_APPS = [
    'demo_auth',
    'custom_commands', # если используете команды для сброса
]
```
2. Унаследуйте модели от IsDemoFieldModel
Чтобы включить поддержку поля is_demo, от которого зависит вся фильтрация и логика, унаследуйте нужные модели:

```python
from demo_auth.models import IsDemoFieldModel

class Category(IsDemoFieldModel):
    name = models.CharField(...)
```
IsDemoFieldModel добавляет поле is_demo = models.BooleanField(default=False), которое используется для фильтрации объектов, созданных в демонстрационном режиме.

3. Используйте DemoModelForm в формах
Если в форме используются поля типа ModelChoiceField или ModelMultipleChoiceField, подключите базовую форму:
```python
from demo_auth.forms import DemoModelForm

class TitleForm(DemoModelForm):
    class Meta:
        model = Title
        fields = ('name', 'year', 'category', 'genre')
```
При использовании демо-пользователя формы автоматически фильтруют связанные поля по is_demo=True.

4. Подключайте DemoFormMixin к Create/Update/DeleteView
Когда вы используете формы (в CreateView, UpdateView и т. д.), добавьте DemoFormMixin для автоматической передачи текущего пользователя в форму:

```python
from demo_auth.mixins import DemoFormMixin

class TitleCreateView(DemoAccessMixin, DemoFormMixin, CreateView):
    ...
```
DemoFormMixin нужен только в представлениях, где используется .get_form().

5. Подключайте DemoAccessMixin ко всем вьюхам, работающим с демо-режимом
Этот миксин:
- проверяет, совпадает ли значение поля is_demo у пользователя и объекта
- ограничивает доступ к объектам с несовпадающим флагом is_demo
- предотвращает просмотр, редактирование и удаление «не своих»
  объектов в демо-режиме

Примеры:
```python
class TitleListView(DemoAccessMixin, ListView):
    ...

class TitleUpdateView(DemoAccessMixin, DemoFormMixin, UpdateView):
    ...
```
Важно: порядок миксинов имеет значение. DemoAccessMixin должен идти раньше, чем DemoFormMixin, чтобы ограничения были применены до передачи пользователя в форму.

6. Подготовка фикстур и настройка сброса демо-данных

Функция reset_demo_data() отвечает за сброс базы данных в исходное состояние, предназначенное для демонстрационного режима. Она восстанавливает только те данные, которые предназначены для использования в демо-режиме, и удаляет или изменяет те, которые не соответствуют этому режиму. Это позволяет пользователям в демо-режиме работать с предварительно заданными данными, не затрагивая реальные записи в базе данных. Эта функция вызывается при входе демо-пользователя во view-классе DemoUserLoginView. Перед её использованием необходимо выполнить несколько шагов:

    Шаг 1: Подготовьте фикстуры

Создайте фикстуры для всех моделей, которые вы хотите использовать в демо-режиме, и сохраните их в директории demo_auth/fixtures/

Например:
- user.json
- category.json
- title.json
и т.д.

Фикстуры должны содержать только те объекты, которые действительно предназначены для демонстрационного режима (например, с флагом is_demo=True).

    Шаг 2: Настройте команды для сброса

В файле restore_data_for_demo.py опишите кортежи команд, которые будут вызываться внутри reset_demo_data(). Они используют кастомные команды из приложения custom_commands:
- reset_bd_from_fixtures: загружает данные из фикстур и заменяет записи в базе, соответствующие объектам из фикстур (по первичному ключу); остальные записи остаются без изменений;
- delete_records_with_conditions: удаляет записи по SQL-условию;
- delete_records_with_conditions_by_model: удаляет записи через ORM с использованием фильтров.

Примеры использования кастомных команд для сброса смотрите в файле restore_data_for_demo.py

# Примеры и рекомендации по использованию

Соответствие типов View и миксинов
ListView — DemoAccessMixin
→ для фильтрации списка объектов
```python
class TitleListView(DemoAccessMixin, ListView):
    ...
```

DetailView — DemoAccessMixin
→ для ограничения доступа к объектам
```python
class TitleDetailView(DemoAccessMixin, DetailView):
    ...
```

CreateView / UpdateView — DemoAccessMixin, DemoFormMixin
→ DemoAccessMixin ограничивает доступ, DemoFormMixin фильтрует связанные поля формы
```python
class TitleCreateView(DemoAccessMixin, DemoFormMixin, CreateView):
    ...
```

DeleteView — DemoAccessMixin
→ только для ограничения доступа (без DemoFormMixin)
```python
class TitleDeleteView(DemoAccessMixin, DeleteView):
    ...
```
