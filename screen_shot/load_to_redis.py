import redis
from baseConfig import *
url_list = []
with open('aaaa_1.txt', 'r') as f:
    for line in f:
        url_list.append(line.rstrip())
r = redis.Redis(**REDIS_HOST)
r.sadd("screenshot", *(url_list[:10000]))
