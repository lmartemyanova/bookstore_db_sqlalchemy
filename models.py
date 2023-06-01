import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship, sessionmaker


Base = declarative_base()


class Publisher(Base):
    __tablename__ = "publisher"

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=200), unique=True, nullable=False)

    # books = relationship("Book", back_populates="publisher")

    def __str__(self):
        return f"Автор {self.name} добавлен с id {self.id}"


class Book(Base):
    __tablename__ = "book"

    id = sq.Column(sq.Integer, primary_key=True, nullable=False, autoincrement=True)
    title = sq.Column(sq.String(length=250), nullable=False)
    id_publisher = sq.Column(sq.Integer, sq.ForeignKey("publisher.id"), nullable=False)
    # id_stock = sq.Column(sq.Integer, sq.ForeignKey("stock.id"), nullable=False)

    publisher = relationship(Publisher, backref="books")
    stock = relationship("Stock", back_populates="books")

    def __str__(self):
        return f"Книга {self.title} добавлена с id {self.id}"


class Stock(Base):
    __tablename__ = "stock"

    id = sq.Column(sq.Integer, primary_key=True, nullable=False, autoincrement=True)
    id_book = sq.Column(sq.Integer, sq.ForeignKey('book.id'), nullable=False)
    id_shop = sq.Column(sq.Integer, sq.ForeignKey('shop.id'), nullable=False)
    count = sq.Column(sq.Integer)

    books = relationship(Book, back_populates="stock")
    shop = relationship("Shop", back_populates="stock")

    def __str__(self):
        return f"Количество добавлено с id {self.id} для книги с id {self.id_book} и магазина с id {self.id_shop}"


class Shop(Base):
    __tablename__ = "shop"

    id = sq.Column(sq.Integer, primary_key=True, nullable=False, autoincrement=True)
    name = sq.Column(sq.String(length=250), unique=True, nullable=False)

    stock = relationship(Stock, back_populates="shop")

    def __str__(self):
        return f"Магазин добавлен с id {self.id}"


class Sale(Base):
    __tablename__ = "sale"

    id = sq.Column(sq.Integer, primary_key=True, nullable=False, autoincrement=True)
    price = sq.Column(sq.Numeric)
    date_sale = sq.Column(sq.Date, nullable=False)
    id_stock = sq.Column(sq.Integer, sq.ForeignKey("stock.id"))
    count = sq.Column(sq.Integer)

    # stock = relationship(Stock, back_populates="sale")

    def __str__(self):
        return f"Скидка  с id {self.id} по цене {self.price} добавлена с даты {self.date_sale} для {self.count} книг."


def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

