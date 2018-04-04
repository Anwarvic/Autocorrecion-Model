import pickle, re
from collections import Counter


OnlyAscii = lambda s: re.match('^[\x00-\x7F]+$', s) != None

DESTINATION = '../data/'
#------------------- Pickling 'grammarly_wikitionary' --------------------
output = Counter()
filename = 'grammarly_wikitionary'
with open(filename+".txt", "r") as f:
	content = f.readlines()
	for line in content:
		key, value = line.split(" ")
		if key.istitle():
			output[key.lower()] = int(value.strip())
		elif key.isupper(): #abbreviations
			continue
		else:
			output[key.lower()] = int(value.strip())
pickle.dump(output, open(DESTINATION+filename+".pickle",'wb'))



#------------------- Pickling 'count_2w' --------------------
output = Counter()
filename = 'count_2w'
with open(filename+".txt", "r") as f:
	content = f.readlines()
	for line in content:
		bi, count = line.split('\t')
		output[bi.lower()] = int(count.strip())
pickle.dump(output, open(DESTINATION+filename+".pickle",'wb'))