import json
import sqlalchemy as sq
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv, find_dotenv
from models import Publisher, Book, Stock, Shop, Sale, create_tables


def fill_tables_from_json():
    path = os.path.join(os.getcwd(), "tests_data.json")
    with open(path, encoding="utf-8") as f:
        json_data = json.load(f)
        models = json_data
        for model in models:
            if model['model'] == 'publisher':
                new_model = Publisher(id=model['pk'], name=model['fields']['name'])
            elif model['model'] == 'book':
                new_model = Book(id=model['pk'], title=model['fields']['title'],
                                id_publisher=model['fields']['publisher'])
            elif model['model'] == 'shop':
                new_model = Shop(id=model['pk'], name=model['fields']['name'])
            elif model['model'] == 'stock':
                new_model = Stock(id=model['pk'], id_shop=model['fields']['shop'], id_book=model['fields']['book'],
                                  count=model['fields']['count'])
            elif model['model'] == 'sale':
                new_model = Sale(id=model['pk'], price=model['fields']['price'], date_sale=model['fields']['date_sale'],
                                count=model['fields']['count'], id_stock=model['fields']['stock'])
            Session = sessionmaker(bind=engine)
            session = Session()
            session.add(new_model)
            session.commit()
            print(new_model)
            session.close()
    return


def create_publisher():
    Session = sessionmaker(bind=engine)
    session = Session()
    new_publisher = Publisher(name=input("Введите имя автора: "))
    session.add(new_publisher)
    session.commit()
    print(new_publisher)
    session.close()
    return


def create_book():
    Session = sessionmaker(bind=engine)
    session = Session()
    new_book = Book(title=input("Введите название книги: "),
                    id_publisher=int(input("Введите id автора: ")))
    session.add(new_book)
    session.commit()
    print(new_book)
    session.close()
    return


def create_stock():
    Session = sessionmaker(bind=engine)
    session = Session()
    new_stock = Stock(id_book=int(input("Введите id книги: ")),
                      count=int(input("Введите количество книг на складе: ")),
                      id_shop=int(input("Введите id магазина: ")))
    session.add(new_stock)
    session.commit()
    print(new_stock)
    session.close()
    return


def create_shop():
    Session = sessionmaker(bind=engine)
    session = Session()
    new_shop = Shop(name=input("Введите название магазина: "))
    session.add(new_shop)
    session.commit()
    print(new_shop)
    session.close()
    return


def create_sale():
    Session = sessionmaker(bind=engine)
    session = Session()
    new_sale = Sale(price=float(input("Введите цену: ")),
                    date_sale=input("Введите дату скидки: "),
                    count=input("Введите количество: "),
                    id_stock=input("Введите id склада: "))
    session.add(new_sale)
    session.commit()
    print(new_sale)
    session.close()
    return


def fill_tables_by_input():
    print("""
    Для заполнения таблицы введите команду:
    "p": таблица publisher,
    "b": таблица book,
    "st": таблица stock,
    "sh": таблица shop,
    "sa": таблица sale,
    "q": выход из программы.
    """)
    commands = {
        "p": create_publisher,
        "b": create_book,
        "st": create_stock,
        "sh": create_shop,
        "sa": create_sale
    }
    run = True
    while run:
        command = input("Какую таблицу вы хотите заполнить? ").lower()
        if command in commands.keys():
            commands[command]()
        elif command == "q":
            run = False
        else:
            print("Вы ввели неправильную команду.")


if __name__ == '__main__':
    load_dotenv(find_dotenv())
    login = os.getenv("user")
    password = os.getenv("password")
    db_name = os.getenv("db_name")

    DSN = f"postgresql://{login}:{password}@localhost:5432/{db_name}"
    engine = sq.create_engine(DSN)
    create_tables(engine)

    while True:
        print("Введите 1, если Вы хотите заполнить таблицы вручную. "
              "Введите 2 для автоматического заполнения из json-файла.")
        command = input("Как вы хотите заполнить таблицы? ")
        if command == "1":
            fill_tables_by_input()
        elif command == "2":
            fill_tables_from_json()
        else:
            print("Неверная команда.")
