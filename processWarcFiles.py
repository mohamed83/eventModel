#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python
print "Content-type:text/html\r\n\r\n"
print "<html>"
print "<head>"
print "<title>Hello - Second CGI Program</title>"
print "</head>"
print "<body>"

import os
import sys
import os.path
import warcunpack_ia

from hanzo.warctools import ArchiveRecord, WarcRecord
from hanzo.httptools import RequestMessage, ResponseMessage
from contextlib import closing
import eventUtils as utils
import cgi, cgitb
import generateEventModel as ge

form = cgi.FieldStorage() 

# Get data from fields
warc = form.getvalue('uploader')
if warc.file:
	warcFile = warc.file.name
txts = expandWarcFile(warcFile)
#Get LDA Topics
ldaTopics = utils.getLDATopics(texts)

#Get Frequent Tokens
sortedTokensFreqs = utils.getFrequentWords(texts)

#Get Indicative tokens
sortedToksTFDF = utils.getIndicativeWords(texts)

# Get Indicative Sentences	
sortedImptSents = utils.getIndicativeSents(sortedToksTFDF,allSents,topK)

# Get Event Model
eventModelInstances = utils.getEventModelInsts(sortedImptSents)

rs = "<tr>"
re = "</tr>"
outputs = "<td>"
outpute = "</td>"
wordsOutput = "<tr><td>Frequent Words (term Frequency)</td><td>Important Words (term Freq * Doc Freq)</td></tr>"
for i in range(topK):
	wordsOutput += rs + outputs + str(sortedTokensFreqs[i]) + outpute + outputs + str(topToksTuples[i]) + outpute + re

sents_ents = "<tr><td>Important Sentences</td><td>Named Entities</td></tr>"
for i in range(len(sortedImptSents)):
	sents_ents += rs + outputs + str(sortedImptSents[i]) + outpute + outputs + str(eventModelInstances[i]) + outpute + re

print wordsOutput
print "<br>============<br>"

print sents_ents
print "<br>============<br>"
print ldaTopics
print "</body>"
print "</html>"
# Filters out html files from a log file produced by warc extraction
def parseLogFileForHtml(log_file):
    htmlList = []
    
    with open(log_file, 'r+b') as f:
        for line in f:
            splitext = line.split('\t')
            if len(splitext) >= 9:
                content_type = splitext[6]
                if content_type.find("text/html") == 0:
                    htmlList.append({"file":splitext[7], "wayback_url":splitext[8], "url":splitext[5]})
                
    return htmlList

# Extracts text from a given HTML file and indexes it into the Solr Instance
def extractText(html_files):
    textFiles = []
    for f in html_files:
        html_file = f["file"]
        file_url = f["url"].strip()
        wayback_url = f["wayback_url"].strip()
        # read the file into a string so beautifulsoup can use it 
           
        html_fileh = open(html_file, "r")
        html_string = html_fileh.read()
        
        if len(html_string) < 1:
            print "error parsing html file " + str(html_file)
            continue
        try:   
            #soup = BeautifulSoup(html_string)
            d = utils.extractTextFromHTML(html_string)
        except:
            print "Error: Cannot parse HTML from file: " + html_file
            continue    
        
        
        titles = {}
        title = d['title']
        if title and title in titles:
            continue
        else:
            titles[title]=1
        html_body = d['text']
		textFiles.append(html_body)
	return textFiles

        #html_id = hashlib.md5(file_url).hexdigest()
        
    #     text_file = open(html_file + ".txt", "w+b")
    #     text_file.write(html_body)
    #     text_file.close()

# Processes the given directory for .warc files
#def main(argv):
def expandWarcFile(warcFile):
#     if (len(argv) < 1):
#         print >> sys.stderr, "usage: processWarcDir.py -d <directory> -i <collection_id> -e <event> -t <event_type>"
#         sys.exit()
#         
#     if (argv[0] == "-h" or  len(argv) < 4):
#         print >> sys.stderr, "usage: processWarcDir.py -d <directory> -i <collection_id> -e <event> -t <event_type>"
#         sys.exit()
    #Done
    #argv = ["","/home/mohamed/IACollections/rem","","3647","","Texas Fertilizer Plant Explosion","","Accident"]
    #argv = ["","/home/mohamed/IACollections/3437","","3437","","Connecticut School Shooting","","Shooting"]
    #argv = ["","/home/mohamed/IACollections/2305","","2305","","Tucson Shooting","","Shooting"]
    #argv = ["","/home/mohamed/IACollections/2823","","2823","","Russia Plane Crash","","Plane_Crash"]
    #argv = ["","/home/mohamed/IACollections/2379","","2379","","Youngstown Shooting","","Shooting"]
    #argv = ["","/home/mohamed/IACollections/2772","","2772","","Norway Shooting","","Shooting"]
    #argv = ["","/home/mohamed/IACollections/694","","694","","April 16 Shooting","","Shooting"]
    #argv = ["","/home/mohamed/IACollections/2892","","2892","","Somalia_Bomb_Blast","","Bombing"]
    #argv = ["","/home/mohamed/IACollections/2838","","2838","","Nevada_AirRace_Crash","","Plane_Crash"]
    #argv = ["","/home/mohamed/IACollections/2822","","2822","","Texas_Wild_Fire","","Fire"]
    #argv = ["","/home/mohamed/IACollections/2882","","2882","","Encephalitis","","Disease_Outbreak"]
    #argv = ["","/home/mohamed/IACollections/2842","","2842","","China_Flood","","Flood"]
    #argv = ["","/home/mohamed/IACollections/2836","","2836","","Pakistan_Flood","","Flood"]
    #argv = ["","/home/mohamed/IACollections/3535","","3535","","Brazil_NightClub_Fire","","Fire"]
    #argv = ["","/home/mohamed/IACollections/2316","","2316","","Haiti_Earthquake_Anniversary","","Earthquake"]
    #argv = ["","/home/mohamed/IACollections/2406","","2406","","New_Zealand_Earthquake","","Earthquake"]
    #argv = ["","/home/mohamed/IACollections/2821","","2821","","Virginia_Earthquake","","Earthquake"]
    #Not Yet
    
    
    #argv = ["","/home/mohamed/IACollections/2903","","2903","","Turkey_Earthquake","","Earthquake"]
    
    
    rootdir = warcFile
    #rootdir = argv[1]
    #collection_id = argv[3]
    #event = argv[5]
    #event_type = argv[7]
    
    for root, subFolders, files in os.walk(rootdir):
        for filename in files:
            filePath = os.path.join(root, filename)
            if filename.endswith(".warc") or filename.endswith(".warc.gz"):# or filename.endswith(".arc.gz"):
                # processWarcFile(filePath, collection_id, event, event_type)
                splitext = filePath.split('.')
                output_dir = splitext[0] + "/"
                
                log_file = os.path.join(output_dir, filePath[filePath.rfind("/")+1:] + '.index.txt')
                
                # output_file = output_dir + filePath.split("/")[1] + ".index.txt"
                if os.path.exists(output_dir) == False:                    
                
                    os.makedirs(output_dir)
        
                    # unpackWarcAndRetrieveHtml(filePath, collection_id, event, event_type)
                    # output_dir = filePath.split(".")[0] + "/"
                    default_name = 'crawlerdefault'
                    wayback = "http://wayback.archive-it.org/"
                    collisions = 0
                        
                    #log_file = os.path.join(output_dir, filePath[filePath.rfind("/")+1:] + '.index.txt')
                    
                    log_fileh = open(log_file, 'w+b')
                    warcunpack_ia.log_headers(log_fileh)
                
                    try:
                        with closing(ArchiveRecord.open_archive(filename=filePath, gzip="auto")) as fh:
                            collisions += warcunpack_ia.unpack_records(filePath, fh, output_dir, default_name, log_fileh, wayback)
                
                    except StandardError, e:
                        print >> sys.stderr, "exception in handling", filePath, e
                        return
                
                    #print "Warc unpack finished"
                
                html_files = parseLogFileForHtml(log_file)
                #print "Log file parsed for html files pathes"
                
                
                # for i in html_files:
                    # extractTextAndIndexToSolr(i["file"], i["url"], i["wayback_url"], collection_id, event, event_type)
                tf = extractText(html_files)
                #print "extracting Text finished"
                return tf

#if __name__ == "__main__":
#    main(sys.argv[1:])
