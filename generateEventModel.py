#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python
print "Content-type:text/html\r\n\r\n"
print "<html>"
print "<head>"
print "<title>Event Model Demo</title>"
print "</head>"
print "<body>"
# Import modules for CGI handling

try:
	import sys
	import cgi, cgitb 
	cgitb.enable()
	#print sys.version
	import logging
	#print sys.version
	import eventUtils as utils
	
	
	topK = 10
	intersectionTh = 2
	#warcFile = '/tmp/warcs/temp.warc'
	form = cgi.FieldStorage() 
	intype = form['inputType'].value
	inData = form['inputData'].value
	#print inData
	if intype == 'warc':
		#warcFile = inData
		texts = utils.expandWarcFile(inData)
	else:
		uf = open(inData,'r')
		urls = uf.readlines()
		uf.close()
		#urls = form['inputData']
		
	#if urls:
		webpagesURLs = urls #inData.split('\n')
		webpagesText = utils.getWebpageText(webpagesURLs)
		texts = [t['text'] for t in webpagesText if t.has_key('text') and len(t['text'])>0]
	'''
	#warc = form['uploadedFile'].file
	#warc = form.getvalue('uploader')
	
	
	#print warc
	#print warc.file
	if warc: #and warc.file:
		f = open(warcFile,"wb")
		f.write(warc.read())
		f.close()
		#print "file saved"
		#warcFile = warc.file.name
		#print warcFile
		texts = utils.expandWarcFile(warcFile)
	#else:
	#	texts = utils.expandWarcFile(warcFile)			
	'''
	
	
	#print texts
	
	#Get LDA Topics
	ldaTopics = utils.getLDATopics(texts)
	
	#Get Frequent Tokens
	sortedTokensFreqs = utils.getFreqTokens(texts)

	#Get Indicative tokens
	#sortedToksTFDF = utils.getIndicativeWords(texts)
	sortedToksTFDF = utils.getFilteredImptWords(texts)
	
	'''
	filteredToksTFDF = []
	toks = " ".join([])
	#print toks
	tokEntsDict = utils.getEntities(toks)[0]
	tokEntsList = []
	for te in tokEntsDict:
		if te in ['LOCATION','DATE']:
			tokEntsList.extend(tokEntsDict[te])
	ntokEntsList= []
	for s in tokEntsList:
		s = s.lower()
		ps = s.split()
		if len(ps) > 1:
			ntokEntsList.extend(ps)
		else:
			ntokEntsList.append(s)
	print ntokEntsList
	print '--------------'
	print toks
	for k in toksTFDF:
		if k not in ntokEntsList:
			filteredToksTFDF.append((k,toksTFDF[k]))
	'''
	
	# Get Indicative Sentences	
	sortedImptSents = utils.getIndicativeSents(sortedToksTFDF,topK,intersectionTh)
	
	# Get Event Model
	eventModelInstances = utils.getEventModelInsts(sortedImptSents)
	
	rs = "<tr>"
	re = "</tr>"
	outputs = "<td>"
	outpute = "</td>"
	wordsOutput = "<tr><td>Frequent Words (term Frequency)</td><td>Important Words (term Freq * Doc Freq)</td></tr>"
	for i in range(topK):
		wordsOutput += rs + outputs + str(sortedTokensFreqs[i]) + outpute + outputs + str(sortedToksTFDF[i]) + outpute + re
	
	sents_ents = "<tr><td>Important Sentences</td><td>Named Entities</td></tr>"
	for i in range(len(sortedImptSents)):
		if eventModelInstances[i]:
			sents_ents += rs + outputs + str(sortedImptSents[i]) + outpute + outputs + str(eventModelInstances[i]) + outpute + re

	print wordsOutput
	print "<br>============<br>"

	print sents_ents
	print "<br>============<br>"
	print ldaTopics
	#print "<br>============<br>"
	#print uniqueEntsWords
	print "</body>"
	print "</html>"
except:
	logging.exception('')
	print sys.exc_info()[0]
	print sys.exc_info()[1]
	print sys.exc_info()[2]
	