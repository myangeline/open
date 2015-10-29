# coding=utf-8
import datetime

import pymysql

from conf import settings


__author__ = 'sunshine'


def get_db(host=settings.host, db=settings.db, user=settings.user, password=settings.password):
    return pymysql.connect(host=host, user=user, password=password, db=db, charset=settings.charset,
                           cursorclass=pymysql.cursors.DictCursor)


def get_category():
    """
    获取类别和类别下的文章数量
    :return:
    """
    connection = get_db()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT a.id, a.name, COUNT(b.id) AS count FROM category AS a LEFT JOIN blogs AS b " \
                  "ON a.id=b.category_id GROUP BY a.id"
            cursor.execute(sql)
            results = cursor.fetchall()
            return results
    except Exception as e:
        print(e)
        return []
    finally:
        connection.close()


def get_all_category():
    """
    只获取所有的类别
    :return:
    """
    connection = get_db()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT id, name FROM category"
            cursor.execute(sql)
            results = cursor.fetchall()
            return results
    except Exception as e:
        print(e)
        return []
    finally:
        connection.close()


def add_category(name, user_id):
    """
    添加类别
    :param name:
    :param user_id:
    :return:
    """
    connection = get_db()
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO category (name, user_id) VALUES (%s, %s)"
            cursor.execute(sql, (name, user_id))
        connection.commit()
    except Exception as e:
        print(e)
        connection.rollback()
    finally:
        connection.close()


def delete_category(category_id):
    """
    删除类别，同时更新blogs表中被删的category_id的字段为0
    :param category_id:
    :return:
    """
    connection = get_db()
    try:
        with connection.cursor() as cursor:
            sql = "delete FROM category WHERE id=%s"
            cursor.execute(sql, category_id)
            sql = "update blogs set category_id=0 WHERE category_id=%s"
            cursor.execute(sql, category_id)
        connection.commit()
    except Exception as e:
        print(e)
        connection.rollback()
    finally:
        connection.close()


def update_category(name, category_id):
    """
    更新类别
    :param name:
    :param category_id:
    :return:
    """
    connection = get_db()
    try:
        with connection.cursor() as cursor:
            sql = "update category SET name=%s WHERE id=%s"
            cursor.execute(sql, (name, category_id))
        connection.commit()
    except Exception as e:
        print(e)
        connection.rollback()
    finally:
        connection.close()


def add_blog(title, summary, content, category_id, user_id=1):
    """
    添加文章
    :param title:
    :param summary:
    :param content:
    :param category_id:
    :param user_id:
    :return:
    """
    connection = get_db()
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO blogs (title, summary, content, category_id, user_id, created_at) " \
                  "VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (title, summary, content, category_id, user_id, datetime.datetime.utcnow()))
        connection.commit()
    except Exception as e:
        print(e)
        connection.rollback()
    finally:
        connection.close()


def get_blog(blog_id):
    connection = get_db()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT a.id, title, summary, content, b.name, created_at, category_id " \
                  "FROM blogs AS a, category AS b WHERE a.category_id=b.id and a.id=%s"
            cursor.execute(sql, blog_id)
            result = cursor.fetchone()
            return result
    except Exception as e:
        print(e)
        return None
    finally:
        connection.close()


def get_blogs():
    connection = get_db()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT a.id, title, summary, b.name, created_at " \
                  "FROM blogs AS a, category AS b WHERE a.category_id=b.id"
            cursor.execute(sql)
            results = cursor.fetchall()
            return results
    except Exception as e:
        print(e)
        return []
    finally:
        connection.close()


def delete_blog(blog_id):
    connection = get_db()
    try:
        with connection.cursor() as cursor:
            sql = "delete FROM blogs WHERE id=%s"
            cursor.execute(sql, blog_id)
        connection.commit()
    except Exception as e:
        print(e)
        connection.rollback()
    finally:
        connection.close()


def update_blog(title, summary, content, category_id, blog_id):
    connection = get_db()
    try:
        with connection.cursor() as cursor:
            sql = "update blogs SET title=%s, summary=%s, content=%s, category_id=%s WHERE id=%s"
            cursor.execute(sql, (title, summary, content, category_id, blog_id))
        connection.commit()
    except Exception as e:
        print(e)
        connection.rollback()
    finally:
        connection.close()


if __name__ == '__main__':
    # connection = get_db()
    # try:
    #     with connection.cursor() as cursor:
    #         sql = "INSERT INTO users (email, password, name, created_at) VALUES (%s, %s, %s, %s)"
    #         cursor.execute(sql, ('269614597@qq.com', '123456', 'admin', datetime.datetime.utcnow()))
    #     connection.commit()
    # except Exception as e:
    #     print(e)
    #     connection.rollback()
    # finally:
    #     connection.close()
    rs = get_category()
    print(rs)
    pass
