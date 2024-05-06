<h1>Тестовое задание: Разработка консольного приложения "Личный финансовый кошелек"</h1>
  <p>Цель этого приложения - предоставить простой инструмент для учета личных доходов и расходов через консольный интерфейс.</p>

<h2>Основные возможности</h2>
  <ul>
    <li><strong>Вывод баланса:</strong> Отображение текущего баланса, а также разбивка по доходам и расходам.</li>
    <li><strong>Добавление записи:</strong> Возможность добавить новую запись о доходе или расходе.</li>
    <li><strong>Редактирование записи:</strong> Изменение уже существующих записей о доходах и расходах.</li>
    <li><strong>Поиск по записям:</strong> Поиск по категориям, датам или сумме.</li>
  </ul>

<h2>Требования к программе</h2>
  <ul>
    <li><strong>Интерфейс:</strong> Реализация через консоль (CLI), без графического или веб-интерфейса. Без использования фреймворков таких как Django, FastAPI, Flask и т.д.</li>
    <li><strong>Хранение данных:</strong> Данные хранятся в текстовом файле. Формат файла определяется разработчиком.</li>
    <li><strong>Информация в записях:</strong> Каждая запись содержит дату, категорию (доход/расход), сумму и описание. Возможны дополнительные поля.</li>
  </ul>

<h2>Будет плюсом</h2>
  <ul>
    <li>Использование аннотаций в коде для функций и переменных.</li>
    <li>Документация к функциям и основным блокам кода.</li>
    <li>Подробное описание функционала приложения в README файле.</li>
    <li>Размещение кода программы и примера файла с данными на GitHub.</li>
    <li>Наличие тестирования.</li>
    <li>Применение объектно-ориентированного подхода в программировании.</li>
  </ul>

<h2>Пример структуры данных в файле</h2>
  <pre>
    Дата: 2024-05-02
    Категория: Расход
    Сумма: 1500
    Описание: Покупка продуктов
  </pre>

<h2>Реализация задания</h2>
  <p>Для реализации консольного интерфейса (CLI) был выбран фреймворк Typer.</p>
  <p>Основные компоненты приложения:</p>
  <ul>
    <li><strong>FileOperations:</strong> Класс для взаимодействия с файлом, содержащим записи. Обеспечивает чтение и запись данных.</li>
    <li><strong>FinanceManager:</strong> Класс-менеджер, отвечающий за обработку данных. Включает в себя основные функции приложения, что позволяет использовать их в командах Typer без дублирования кода.</li>
  </ul>
    
  <p>Для определения типа записи (доход или расход) используется знак суммы. В файле сумма хранится без знака.</p>

  <p>В целях упрощения не был создан отдельный DataClass для записи. Данные хранятся в файле <code>finances.json</code>, который находится в той же папке, что и основное приложение.</p>

  <p>Также, в файле <code>test_finances.py</code> реализованы тесты для следующих компонентов:</p>
  <ul>
      <li>Тесты для <strong>FileOperations</strong>.</li>
      <li>Тесты для <strong>FinanceManager</strong>.</li>
      <li>Тесты для команд в <strong>CLI</strong>.</li>
  </ul>

<h2>Заключение</h2>
  <p>Это приложение "Личный финансовый кошелек" предоставляет основные функции для учета финансов через консольный интерфейс. Оно легко расширяется и тестируется, что обеспечивает надежность и гибкость в использовании.</p>
