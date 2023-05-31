## Управление базой данных книжных магазинов

#### ***Программа предназначена для создания базы данных книжных магазинов и обращения к ней при помощи PostgreSQL.***

База данных имеет структуру:
![Схема БД](https://github.com/netology-code/py-homeworks-db/blob/SQLPY-76/06-orm/readme/book_publishers_scheme.png?raw=true)

### Установка:
1. Клонировать репозиторий.
```
git clone ссылка-на-репозиторий(SSH)
```
2. Установить зависимости из requrements.txt: 
```
pip install -r requirements.txt
```
3. Создать базу данных, выполнив в терминале:
```
createdb -U postgres название_БД
```
Потребуется ввести пароль для пользователя postgres.

4. Переименовать файл ".env.example" в ".env", записать в него название БД, логин и пароль для пользователя PostgreSQL, например: 
```
db_name=bookstore
user=postgres
password=postgres
```
5. Запустить код в IDE или выполнить в терминале:
```
python main.py
```
6. Данные могут быть внесены автоматически или вручную.
Для заполнения вручную следуйте инструкциям в консоли.
Пример содержания данных для БД при автоматическом заполнении в JSON-файле.

### Формат получаемых данных:

Принимает имя или идентификатор издателя (publisher), через пользовательский ввод. Выводит построчно факты покупки книг этого издателя:

```
название книги | название магазина, в котором была куплена эта книга | стоимость покупки | дата покупки
```

Пример (было введено имя автора — `Пушкин`):

```
Капитанская дочка | Буквоед     | 600 | 09-11-2022
Руслан и Людмила  | Буквоед     | 500 | 08-11-2022
Капитанская дочка | Лабиринт    | 580 | 05-11-2022
Евгений Онегин    | Книжный дом | 490 | 02-11-2022
Капитанская дочка | Буквоед     | 600 | 26-10-2022
```