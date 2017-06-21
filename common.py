global debug

def disableDebug():
	debug = False

def enableDebug():
	debug = True

def d(txt):
	if(debug):
		#Print debug messages
		print txt
	else:
		#Dont bother printing debug
		pass
