import json
import sqlalchemy
import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
import os
from dotenv import load_dotenv, find_dotenv

Base = declarative_base()


class Publisher(Base):
    __tablename__ = "publisher"

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=200), unique=True, nullable=False)

    books = relationship("Book", back_populates="publisher")

    def __str__(self):
        return f"{self.id}: {self.name}"


class Book(Base):
    __tablename__ = "book"

    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String(length=250))
    id_publisher = sq.Column(sq.Integer, sq.ForeignKey("publisher.id"), nullable=False)

    publisher = relationship(Publisher, back_populates="books")
    stock = relationship("Stock", back_populates="book")


class Stock(Base):
    __tablename__ = "stock"

    id = sq.Column(sq.Integer, primary_key=True)
    id_book = sq.Column(sq.Integer, sq.ForeignKey('book.id'), nullable=False)
    id_shop = sq.Column(sq.Integer, sq.ForeignKey('shop.id'), nullable=False)
    count = sq.Column(sq.Integer)

    book = relationship(Book, back_populates="stock")
    shop = relationship("Shop", back_populates="stock")


class Shop(Base):
    __tablename__ = "shop"

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=250), unique=True, nullable=False)

    stock = relationship(Stock, back_populates="shop")


class Sale(Base):
    __tablename__ = "sale"

    id = sq.Column(sq.Integer, primary_key=True)
    price = sq.Column(sq.Numeric)
    date_sale = sq.Column(sq.Date, nullable=False)
    id_stock = sq.Column(sq.Integer, sq.ForeignKey("stock.id"))
    count = sq.Column(sq.Integer)

    # stock = relationship(Stock, back_populates="sale")


def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


def fill_tables_from_json(data_json=os.getcwd()):
    with open(data_json, encoding="utf-8") as f:
        json_data = json.load(f)


def fill_tables_by_input():
    publisher = Publisher(name=input("Введите название издателя: "))
    # print(f"Автор добавлен с id {publisher.id}")
    book = Book(title=input("Введите название книги: "))
    # print(f"Книга добавлена с id {book.id}")
    stock = Stock(count=input("Введите количество книг на складе: "))
    # print(f"Количество добавлено с id {stock.id} для книги с id {stock.id_book} и магазина с id {stock.id_shop}")
    shop = Shop(name=input("Введите название магазина: "))
    # print(f"Магазин добавлен с id {shop.id}")
    sale = Sale(
        price=input("Введите цену: "),
        date_sale=input("Введите дату скидки: "),
        count=input("Введите количество экземпляров со скидкой: ")
    )
    # print(f"Скидка добавлена с id {sale.id}")

    session.add_all([publisher, book, stock, shop, sale])
    session.commit()
    print(publisher.id, book.id, stock.id, shop.id, sale.id)


if __name__ == '__main__':
    load_dotenv(find_dotenv())
    login = os.getenv("user")
    password = os.getenv("password")
    db_name = os.getenv("db_name")

    DSN = f"postgresql://{login}:{password}@localhost:5432/{db_name}"
    engine = sq.create_engine(DSN)
    create_tables(engine)

    while True:
        Session = sessionmaker(bind=engine)
        session = Session()
        print("Введите 1, если Вы хотите заполнить таблицы вручную. "
              "Введите 2 для автоматического заполнения из json-файла.")
        command = input("Как вы хотите заполнить таблицы? ")
        if command == "1":
            fill_tables_by_input()
        elif command == "2":
            data_json = os.path.abspath(input("Введите путь к файлу: "))
            fill_tables_from_json(data_json)

    session.close()