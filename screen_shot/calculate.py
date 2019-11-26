import json
import os

res_lst = []

def is_res(fn):
    return 'result' in fn and os.path.isfile(fn)

def takeSecond(elem):
    return elem[1]

res_files = filter(is_res, os.listdir())

# print(list(res_files))
total = []
for file in res_files:
    with open(file) as f:
        v6support_i = [json.loads(line.rstrip()) for line in f]
    total += v6support_i

for each in total:
    res_lst.append(str((each['url'], (each['pic']+each['structure']
        +each['text'])/3 * each['net'])) + '\n')


res_lst.sort(key=takeSecond)

with open('v6support.txt', 'w') as f:
    f.writelines(res_lst)