import os
import pickle


DES = './authors_names'
names = set([])
for filename in os.listdir(DES):
	print filename
	for line in file(DES+'/'+filename).readlines():
		for name in line.split(' '):
			name = name.strip()
			if '.' not in name and len(name) > 2:
				try:
					name.decode('ascii')
					names.add(name)
				except:
					continue

	print len(names) #241,000

pickle.dump(names, open(DES[2:]+'.pickle','wb'))