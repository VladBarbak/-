import mysql.connector
from mysql.connector import MySQLConnection, Error
from utils import unit_by_field, nested_dict_to_list
import json
import random
from datetime import *


def read_db_config():
    return dict(
        host="remotemysql.com",
        user="FJxxN13JAf",
        passwd="xdapbFJMy8",
        database="FJxxN13JAf",
        auth_plugin='mysql_native_password')


def query_with_fetchall(sql, data, dictionary=True, return_id=False):
    try:
        returned_id = 0
        row = []
        db_config = read_db_config()
        with MySQLConnection(**db_config) as conn:
            with conn.cursor(dictionary=dictionary) as cursor:
                cursor.execute(sql, data)

                if return_id:
                    returned_id = cursor.lastrowid

                row = cursor.fetchall()
            conn.commit()

        if return_id:
            return row, returned_id
        else:
            return row

    except Error as e:
        print(e)


def get_books():
    sql = """
    select
      *
    from book
    """

    return query_with_fetchall(sql, [])


def get_books_catalog():
    sql = """
    select
      book.book_id as `book_id`,
      book.title as `title`,
      book.year as `year`,
      price as `price`,
      author.name as `author`,
      category.name as `category`
    from book
      inner join book_author using(book_id)
      inner join author using(author_id)
      inner join book_category using(book_id)
      inner join category using(category_id)
    """

    return query_with_fetchall(sql, [])


def get_books_catalog_by_category(category_id):
    sql = """
    select
      book.book_id as `book_id`,
      book.title as `title`,
      book.year as `year`,
      price as `price`,
      author.name as `author`,
      category.name as `category`
    from book
      inner join book_author using(book_id)
      inner join author using(author_id)
      inner join book_category using(book_id)
      inner join category using(category_id)
    where
      category_id = %s
    """

    return query_with_fetchall(sql, [category_id])


def get_categories():
    sql = """
    select
      *
    from category
    """

    return query_with_fetchall(sql, [])


def get_sellers():
    sql = """
    select
      *
    from seller
    """

    return query_with_fetchall(sql, [])


def get_seller_by_id(seller_id):
    sql = """
    select
      *
    from seller
    where
      seller_id = %s
    """

    return query_with_fetchall(sql, [seller_id])


def get_schedule_for_seller(seller_id):
    sql = """
    select
      day,
      open_at as `open at`,
      close_at as `close at`
    from schedule
    where
      schedule.seller_id = %s
    """

    return query_with_fetchall(sql, [seller_id])


def get_contacts():
    sql = """
    select
      *
    from contract
    """

    return query_with_fetchall(sql, [])


def get_supplying_for_seller(seller_id):
    sql = """
    select
      book.title as `book`,
      supplying.count,
      supplying.count * book.price as `amount of cost`,
      supplying.datetime as `date and time`,
      provider.name as `provider`
    from supplying
      inner join contract using(contract_id)
      inner join provider using(provider_id)
      inner join book using(book_id)
    where
      contract.seller_id = %s
    """

    return query_with_fetchall(sql, [seller_id])


def get_buyers():
    sql = """
    select
      *
    from buyer
    """

    return query_with_fetchall(sql, [])


def get_providers():
    sql = """
    select
      *
    from provider
    """

    return query_with_fetchall(sql, [])


def get_selling_of_seller(seller_id):
    sql = """
    select
      selling.datetime as `date and time`,
      book.book_id as `book id`,
      book.title as `book`,
      selling.count,
      buyer.nickname as `buyer`,
      buyer.email
    from selling
      inner join payment using(payment_id)
      inner join buyer using(buyer_id)
      inner join book using(book_id)
    where
      selling.seller_id = %s
    order by `date and time`
    """

    return query_with_fetchall(sql, [seller_id])


def insert_contract(seller_id, provider_id, supply_interval, count, dateandtime, book_id):
    sql = """
    insert into contract (`seller_id`, `provider_id`, `supply_interval`)
    values (%s, %s, %s)
    """
    data, contract_id = query_with_fetchall(sql, [seller_id, provider_id, supply_interval], return_id=True)

    sql = """
    insert into supplying (`count`, `datetime`, `book_id`, `contract_id`)
    values (%s, %s, %s, %s)
    """

    query_with_fetchall(sql, [count, dateandtime, book_id, contract_id])


def get_providers_for_seller(seller_id):
    sql = """
    select
      contract_id as `id`,
      provider.name as `provider`,
      contract.supply_interval as `provide interval`
    from contract
      inner join provider using(provider_id)
    where
      contract.seller_id = %s
    """

    return query_with_fetchall(sql, [seller_id])


if __name__ == '__main__':
    # buyers = get_buyers()
    # sellers = get_sellers()
    # books = get_books()
    #
    # for i in range(40, 90):
    #     rand_count = random.randint(1, 4)
    #     rand_book = books[random.randint(0, len(books) - 1)]
    #
    #     sql = """
    #     insert into payment (`payment_id`, `buyer_id`, `amount`)
    #     values (%s, %s, %s)
    #     """
    #     query_with_fetchall(sql, [i, random.randint(1, 10), rand_book['price'] * rand_count])
    #
    #     sql = """
    #     insert into selling (`seller_id`, `datetime`, `payment_id`, `book_id`, `count`)
    #     values (%s, %s, %s, %s, %s)
    #     """
    #     query_with_fetchall(sql, [random.randint(1, 3),
    #                               datetime.now() - timedelta(days=random.randint(1, 10),
    #                                                          hours=random.randint(1, 10),
    #                                                          minutes=random.randint(1, 50)),
    #                               i, rand_book['book_id'], rand_count])
    pass