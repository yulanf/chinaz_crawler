# -*- coding:utf-8 -*-

import pymysql
import pymongo
import redis

class RedisClient(object):
    def __init__(self, key, host, password):
        self.key = key
        self.r = redis.Redis(host='', password='', decode_responses=True)

    def pop(self):
        return self.r.spop(self.key)

    def add(self, item):
        self.r.sadd(self.key, item)

    def get_num(self):
        return self.r.scard(self.key)


class MysqlClient(object):
    pass

class WebsiteMetricRepo(object):
    def __init__(self, host, password):
        pass

    def insert():
        pass

    def update():
