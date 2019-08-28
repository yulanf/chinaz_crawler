from storage import RedisClient

rc = RedisClient('url', '127.0.0.1', None)
with open('ul.txt', 'r') as f:
	n = [line.rstrip() for line in f]
# print(n)

for x in n:
	rc.add(x)