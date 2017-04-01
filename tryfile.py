# main.py 
# test file I/O

import os

f = open('data.txt','w')
for x in range(0,10):
	f.write('0123456789')
f.close()

f = open('data.txt','r')
print( f.read())
f.close()

print(os.listdir() )
