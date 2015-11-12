# coding=utf-8
from bson import ObjectId
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
        """
        获取所有分类
        :return:
        """
        categories = self.db['tb_category'].find()
        return categories

    def del_category(self, category_id):
        """
        删除类别
        :param category_id:
        :return:
        """
        self.db['db_category'].remove({'_id': ObjectId(category_id)})

    def update_category(self, category):
        """
        更新类别
        :param category:
        :return:
        """
        self.db['db_category'].update({'_id': ObjectId(category.id)}, {"$set": {"name": category.name}})

    def insert_category(self, category):
        """
        添加类别
        :param category:
        :return:
        """
        self.db['db_category'].insert({"name": category.name, 'create_time': category.create_time})

    def get_blog(self, blog_id=None):
        """
        获取文章
        :param blog_id:
        :return:
        """
        if blog_id:
            return self.db['db_blog'].find_one({'_id': ObjectId(blog_id)})
        else:
            return self.db['db_blog'].find()

    def del_blog(self, blog_id):
        """
        删除文章
        :param blog_id:
        :return:
        """
        self.db['db_blog'].remove({'_id': ObjectId(blog_id)})

    def update_blog(self, blog):
        pass

    def insert_blog(self, blog):
        pass

    def get_user(self, name, pwd):
        pass


if __name__ == '__main__':
    mu = MongodbUtil()
    # mu.db.student.insert({'name': "卢加诺", "age": 22})
    for i in mu.db.student.find():
        print(i['name'])
    pass