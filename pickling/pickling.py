import pickle
from collections import Counter



DESTINATION = '../data/'
#------------------- Pickling 'grammarly_wikitionary' --------------------
output = Counter()
filename = 'grammarly_wikitionary'
with open(filename+".txt", "r") as f:
	content = f.readlines()
	for line in content:
		key, value = line.split(" ")
		if '.' in key:
			output[key.replace('.', '').lower()] = int(value.strip())
		elif '-' in key:
			output[key.replace('-', '').lower()] = int(value.strip())
		else:
			output[key.lower()] = int(value.strip())
# #turn the counts into probability
# total = sum(output.values())
# for k, v in output.iteritems():
# 	output[k] = float(v)/total
pickle.dump(output, file(DESTINATION+filename+".pickle",'wb'))



#------------------- Pickling 'count_2w' --------------------
output = Counter()
filename = 'count_2w'
with open(filename+".txt", "r") as f:
	content = f.readlines()
	for line in content:
		bi, count = line.split('\t')
		output[bi.lower()] = int(count.strip())
# #turn the counts into probability
# total = sum([v for _, _counter in output.iteritems() for _, v in _counter.iteritems()])
# for k1, _counter in output.iteritems():
# 	for k2, v in _counter.iteritems():
# 		output[k1][k2] = float(v)/total
pickle.dump(output, file(DESTINATION+filename+".pickle",'wb'))