import datetime

import pymysql

from conf import settings


__author__ = 'sunshine'


def get_db(host=settings.host, db=settings.db, user=settings.user, password=settings.password):
    return pymysql.connect(host=host, user=user, password=password, db=db, charset=settings.charset,
                           cursorclass=pymysql.cursors.DictCursor)

if __name__ == '__main__':
    connection = get_db()
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO users (email, password, name, created_at) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, ('269614597@qq.com', '123456', 'admin', datetime.datetime.utcnow()))
        connection.commit()
    except Exception as e:
        print(e)
        connection.rollback()
    finally:
        connection.close()
