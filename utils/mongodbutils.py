# coding=utf-8
import pymongo
from conf import settings

__author__ = 'sunshine'


class MongodbUtil(object):
    def __init__(self, host=settings.mongodb_host, port=settings.mongodb_port, user=settings.mongodb_user,
                 pwd=settings.mongodb_pwd, db=settings.mongodb_db):
        client = pymongo.MongoClient(host, port, connect=False)
        db = client[db]
        db.authenticate(user, pwd, source='admin')
        self.db = db

    def get_category(self):
        pass

    def del_category(self, category_id):
        pass

    def update_category(self, category):
        pass

    def get_blog(self, blog_id):
        pass

    def del_blog(self, blog_id):
        pass

    def update_blog(self, blog):
        pass

    def get_user(self, name, pwd):
        pass


if __name__ == '__main__':
    mu = MongodbUtil()
    # mu.db.student.insert({'name': "卢加诺", "age": 22})
    for i in mu.db.student.find():
        print(i['name'])
    pass