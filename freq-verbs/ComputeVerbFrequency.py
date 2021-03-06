import fileinput
import plistlib
import unicodecsv
import math


# Utility functions used to convert from/to a CSV to edit. 
# For example
# 	call verbsPlistToCsv('verbs-org.plist','verbs.csv')
#	edit 'verbs.csv' with Excel, Numbers, etc
#	call csvToVerbsPlist('verbs.csv','verbs-edited.plist')

def	verbsPlistToCsv(plistPath, csvPath,header=False):
	plist = plistlib.readPlist(plistPath)
	outFile = open(csvPath,'w')
	csvWriter = unicodecsv.writer(outFile,encoding='utf-8',delimiter=';')
	if (header):
		csvWriter.writerow(['hint','simple','participle','past','frequency','translation'])
	for item in plist:
		values = item.values()
		csvWriter.writerow(values)
	outFile.close()

def csvToVerbsPlist(csvPath, plistPath):
    inFile = open(csvPath,'r');
    csvReader = unicodecsv.reader(inFile, encoding='utf-8', delimiter=';')
    plist = []
    for row in csvReader:
        plist.append({'simple':row[0].lower(),'past':row[1].lower(),
        'translation':row[2].lower(),'participle':row[3].lower(),'level':int(row[4])})
    plistlib.writePlist(plist,plistPath)

# Utility function to generate the README.md table
# for the 5 more frequently used verbs the function returns
#
# |Verb                  |     Freq |
# |:--------------------:|---------:|
# | be/am/are/is         | 0.225649 |
# | get                  | 0.071703 |
# | do/does              | 0.070281 |
# | have                 | 0.069897 |
# | come                 | 0.055208 |

def verbsPlistToMarkdownTopPTable(verbs,topNumber):
	freqList = []
	for v in verbs:
		freqList.append("%.6f|%s"%(v['frequency'],v['simple']))
	
	freqList.sort(reverse=True)
	table=["|Verb                  |     Freq |"]
	table.append("|:--------------------:|---------:|")
	for i in range(0,topNumber):
		row = freqList[i].split('|');
		table.append("| %-20s | %s |"%(row[1],row[0]))
	
	return '\n'.join(table)

def trimVerbsHints():
	inFile = open('verbs-hints.txt','r')
	outFile = open('verbs-hints-stripped.txt','w')
	for line in inFile:
		outFile.write("%s\n"%line.strip())
	outFile.close()
	
def loadHints():
	inFile = open('verbs-hints-stripped.txt','r')
	hints={}
	for line in inFile:
		if line[0]=='#':
			continue
		if line.strip().isdigit():
			vector = [];
			hints.update({line.strip():vector})
		else:
			line = line.strip()
			line = line.split(' ')[0]
			vector.append(line.strip())
	
	tableHints={}
	for hint,verbs in hints.items():
		for verb in verbs:
			tableHints.update({verb:int(hint)})
	return tableHints
	
def hintsDescriptionToPlist(plistPath):
	inFile = open('hints-description.txt','r');
	hints = []
	for line in inFile:
		items = line.split(':')
		hints.append(items[1].strip())
	plistlib.writePlist(hints,plistPath);
	
		
def computeVerbsFrequency():
	# Read 50K word list with use count
	freq50K = {}
	for line in fileinput.input('en_50K.txt'):
		# we need to remove the original EOL
		line = line[:len(line)-2].split(' ')
		freq50K.update({line[0]:int(line[1])})
	
	
	# Read verbs.plist from "A list of verbs" and compute use count for all tenses
	# We assume that the verbs with multiple forms are in the form "do/does"
	verbs = plistlib.readPlist('verbs-edited.plist')
	for verb in verbs:
		# We join all the verbal forms to construct a string like this:
		# was/were/be/am/are/is/been
		testValues = '/'.join([verb['simple'],verb['past'],verb['participle']])
		count = 0;
		# Now we look for each word and add the use count
		for tense in testValues.split('/'):
			count += freq50K.get(tense,0);
		verb.update({'useCount':count})
		
	# Compute frequencies
	total = reduce(lambda x,y: x+y['useCount'] ,verbs,0)
	for verb in verbs:
		verb.update({'frequency': 1.0*verb['useCount']/total})
		del verb['useCount'];
		del verb['level'];
		
	# Save a new verbs.plist with the frequency of use
	plistlib.writePlist(verbs,'verbs-freq.plist')
	
	# Save also a csv copy to statistical analysis
	verbsPlistToCsv('verbs-freq.plist','verbs-freq.csv',header=True)
	
	# Compute log distribution and normalize it
	for verb in verbs:
		verb['frequency'] = math.log(verb['frequency'])
		
	minFreq = reduce(lambda x,y: min(x,y['frequency']),verbs,1)
	for verb in verbs:
		verb['frequency'] = 1.0-verb['frequency']/minFreq
	
	total = reduce(lambda x,y: x+y['frequency'] ,verbs,0)
	for verb in verbs:
		verb['frequency'] = 1.0*verb['frequency']/total

	# Load and append hint group number
	trimVerbsHints()
	hints = loadHints()
	for verb in verbs:
		key = verb['simple']
		if hints.has_key(key):
			verb.update({'hint':hints[key]})
		else:
			key = key.split('/')[0]
		 	if hints.has_key(key):
				verb.update({'hint':hints[key]})
			else:
				verb.update({'hint':0})
		
	# Save a new verbs.plist with the frequency of use
	plistlib.writePlist(verbs,'verbs-freq-log.plist')
	
	# Save also a csv copy to statistical analysis
	verbsPlistToCsv('verbs-freq-log.plist','verbs-freq-log.csv',header=True)
	
# hintsDescriptionToPlist('hints.plist')
computeVerbsFrequency()