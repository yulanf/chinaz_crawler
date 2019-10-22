with open('ip_len_46_list.txt', 'r') as f:
	ymlb = [line.split('\t')[0].strip() for line in f]

with open('url_list.txt', 'w') as f:
	for i in ymlb:
		f.write(i + '\n')
		