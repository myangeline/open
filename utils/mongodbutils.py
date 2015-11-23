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

    def get_category(self, category_id=None):
        """
        获取所有分类
        :param category_id:
        :return:
        """
        if category_id:
            return self.db['dt_category'].find_one({'_id': ObjectId(category_id)})
        else:
            return self.db['dt_category'].find()

    def del_category(self, category_id):
        """
        删除类别
        :param category_id:
        :return:
        """
        self.db['dt_category'].remove({'_id': ObjectId(category_id)})

    def update_category(self, category):
        """
        更新类别
        :param category:
        :return:
        """
        if category.id:
            self.db['dt_category'].update({'_id': ObjectId(category.id)},
                                          {"$set": {"name": category.name, 'create_time': category.create_time}})
            # 修改类别后需要更新文章中的类别名称
            self.update_blog_category(category.id, category.name)
        else:
            self.db['dt_category'].insert({"name": category.name, 'count': category.count,
                                           'create_time': category.create_time})

    def update_category_count(self, category_id, count=1):
        """
        更新类别中文章的数量
        :param category_id:
        :param count:
        :return:
        """
        category = self.get_category(category_id)
        self.db['dt_category'].update({'_id': ObjectId(category_id)},
                                      {"$set": {"count": count+category['count']}})

    def get_blog(self, blog_id=None):
        """
        获取文章
        :param blog_id:
        :return:
        """
        if blog_id:
            return self.db['dt_blog'].find_one({'_id': ObjectId(blog_id)})
        else:
            return self.db['dt_blog'].find()

    def del_blog(self, blog_id):
        """
        删除文章
        :param blog_id:
        :return:
        """
        # 删除文章后需要减去类别中对文章的统计
        blog = self.get_blog(blog_id)
        self.db['dt_blog'].remove({'_id': ObjectId(blog_id)})
        self.update_category_count(blog['category_id'], -1)

    def update_blog(self, blog):
        """
        更新文章
        :param blog:
        :return:
        """
        kwargs = dict()
        if blog.title:
            kwargs['title'] = blog.title
        if blog.summary:
            kwargs['summary'] = blog.summary
        if blog.html_content:
            kwargs['html_content'] = blog.html_content
        if blog.source_content:
            kwargs['source_content'] = blog.source_content
        if blog.category:
            kwargs['category'] = blog.category
        kwargs['create_time'] = blog.create_time
        self.db['dt_blog'].update({'_id': ObjectId(blog.id)}, {'$set': kwargs})

    def update_blog_category(self, category_id, category_name):
        """
        更新文章中的类别名称
        :param category_id:
        :param category_name:
        :return:
        """
        self.db['dt_blog'].update({'category_id': category_id}, {'$set': {'category': category_name}})

    def insert_blog(self, blog):
        """
        添加文章
        :param blog:
        :return:
        """
        self.db['dt_blog'].insert({'title': blog.title, 'summary': blog.summary, 'html_content': blog.html_content,
                                   'source_content': blog.source_content, 'category': blog.category,
                                   'category_id': blog.category_id, 'create_time': blog.create_time})
        self.update_category_count(blog.category_id)

    def get_user(self, name, pwd):
        """
        根据用户名和密码获取用户
        :param name:
        :param pwd:
        :return:
        """
        user = self.db['dt_user'].find_one({'name': name, 'pwd': pwd})
        return user


if __name__ == '__main__':
    # mu = MongodbUtil()
    # mu.db.student.insert({'name': "卢加诺", "age": 22})
    # for i in mu.db.student.find():
    #     print(i['name'])
    # mu.db.dt_user.insert({'name': 'admin', 'pwd': '6412121cbb2dc2cb9e460cfee7046be2'})
    pass