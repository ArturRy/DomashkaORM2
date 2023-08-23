import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models import Publisher, Book, Shop, Stock, Sale, create_table
import json


DSN =
engine = sqlalchemy.create_engine(DSN)
create_table(engine)
Session = sessionmaker(bind=engine)
session = Session()


def fill_in_the_table():
    with open('tests_data.json') as file:
        my_data = json.load(file)
        for d in my_data:
            if d['model'] == 'publisher':
                name = d['fields']['name']
                id_p = d['pk']
                publisher = Publisher(name=name, id_publisher=id_p)
                session.add(publisher)
                session.commit()
            elif d['model'] == 'book':
                id_b = d['pk']
                title = d['fields']['title']
                id_p = d['fields']['id_publisher']
                book = Book(id_book=id_b, title=title, id_publisher=id_p)
                session.add(book)
                session.commit()
            elif d['model'] == 'shop':
                id_sh = d['pk']
                name = d['fields']['name']
                shop = Shop(id_shop=id_sh, name=name)
                session.add(shop)
                session.commit()
            elif d['model'] == 'stock':
                id_st = d['pk']
                id_sh = d['fields']['id_shop']
                id_b = d['fields']['id_book']
                count = d['fields']['count']
                stock = Stock(id_stock=id_st, id_shop=id_sh, id_book=id_b, count=count)
                session.add(stock)
                session.commit()
            elif d['model'] == 'sale':
                id_s = d['pk']
                price = d['fields']['price']
                date_sale = d['fields']['date_sale']
                count = d['fields']['count']
                id_st = d['fields']['id_stock']
                sale = Sale(id_sale=id_s, price=price, date_sale=date_sale, count=count, id_stock=id_st)
                session.add(sale)
                session.commit()


fill_in_the_table()


def info_book():
    # info = '1'
    info = str(input('Введите имя или ID издателя'))
    query = session.query(Book.title, Shop.name, Sale.price, Sale.date_sale).join(Publisher).join(Stock).join(
        Shop).join(Sale)
    if info.isalpha():
        query1 = query.filter(Publisher.name == info)
    elif info.isdigit():
        query1 = query.filter(Publisher.id_publisher == int(info))

    book = 'Название книги'
    shop = 'Название магазина, в котором была куплена книга'
    price = 'Стоимость покупки'
    date = 'Дата покупки'
    print(f'{book:<40}|{shop:<50}|{price:<20}|{date}')
    for q, w, e, r in query1:
        print(f'{q:<40}|{w:<50}|{e:<20}|{r.strftime("%d-%m-%Y")}')


if __name__ == '__main__':
    info_book()
session.close()
