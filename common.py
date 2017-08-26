# Common Utilities
global debug

def disableDebug():
	debug = False

def enableDebug():
	debug = True

def d(txt):
	if((txt is not None) or (txt is not 'None')):
		print(txt)

