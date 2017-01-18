# form-frame (Фрейм-анкета)

Пользователь запускает программу **gui.py**, вводит запрос в формате: **$prefix.name=value;**</br>
Возможен ввод нескольких триплетов подряд.

* **prefix**: один или более символ (A-Z, a-z);
* **name**: один или более символ (A-Z, a-z, 0-9);
* **value**: любое количество любых символов;
 * **пустое значение**: значение будет взято из словаря метаданных (заполнение НЕ обязательно);
 * **пробел**: значение будет взято из словаря метаданных (заполнение НЕ обязательно);
 * **двоеточие**: значение будет взято из словаря метаданных (заполнение обязательно);
 * **любое другое значение**: будет использоваться введенное значение.

После осуществляется сравнение запроса с данными в словаре метаданных.
Генерируется фрейм-анета, в которой вместо триплета отображается его читаемое имя
и поле ввода значения. По умолчанию будет использовано введенное значение или значение из словаря метаданных (в зависимости от запроса). Если рядом с текстовым полем стоит звездочка (*), то это значит, что поле обязательно для заполнения. 

После ввода данных в анкету, нужно нажать кнопку "Принять данные". Далее откроется окно с результатами операции, в котором будет сообщение об успешном сохранении данных в файле (**result.txt**) или список ошибок.
**Нереализованные функции:**
* Проверка введенного в текстовое поле значения на соответствие необходимому типу данных.
* Проверка на обязательность заполнения текстового поля.
* Сохранение введенных в текстовое поле значений.
* Запрет некорректного ввода после первого триплета.

В словаре метаданных (**database.txt**) хранится:
* Для каждой пары класс + имя ($prefix.name) хранится читаемое имя (display_label).
Например, для класса L и имени NM читаемое имя – «Тип фрезы».
* Значение поля по умолчанию (value).
* Тип каждого поля (field_type). Например, String, Int.

### Пример работы программы

![](Example/1.PNG)
![](Example/2.PNG)
![](Example/3.PNG)
