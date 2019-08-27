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

    def add(self):
        self.r.sadd(self.key)

    def get_num(self):
        return self.r.scard(self.key)


class MysqlClient(object):
    pass

class MongoClient(object):
    def __init__(self):
        
    def 