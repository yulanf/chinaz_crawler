import redis
from baseConfig import *

def load_domains():
	r = redis.Redis(**REDIS_HOST)

	with open('ul.txt', 'r') as f:
		domain_list = [line.rstrip() for line in f]



	r.sadd('screent_shot_website', *domain_list)


if __name__ == '__main__':
	load_domains()
