#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python
print "Content-Type: application/json\r\n\r\n"

'''
print "<html>"
print "<head>"
print "<title>Event Model Demo</title>"
print "</head>"
print "<body>"
'''
try:
	import json,sys
	import cgi, cgitb 
	cgitb.enable()

	import logging
	logging.basicConfig(filename='/tmp/warcs/errors.log')
	import eventUtils as utils



	warcDir = '/tmp/warcs/'
	form = cgi.FieldStorage() 
	
	#if 'uploadedFile' in form:
	warcf = form['uploadedFile'].file
	warcfn = form['uploadedFile'].filename
	logging.debug(warcfn)
	warcFile = warcDir + warcfn
		
	f = open(warcFile,"wb")
	f.write(warcf.read())
	f.close()
	#else:
	#	warcf = open(warcDir + 'test.warc.gz')
	#	warcFile = warcDir + warcfn
	
	#print "file="+warcFile +",name="+warcfn
	out = {}
	out['file']=warcFile
	out['name']=warcfn
	out['width']=0
	out['height']=0
	out['type']=""
	out['uploadType']=""
	out['size']=0
	print json.dumps(out)
	#print "</body>"
	#print "</html>"
except:
	logging.exception('')
	logging.debug('error!!')
	#print sys.exc_info()[0]
	print sys.exc_info()[1]
	print sys.exc_info()[2]