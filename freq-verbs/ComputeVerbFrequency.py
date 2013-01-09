import fileinput
import plistlib
import unicodecsv


# Utility functions used to convert from/to a CSV to edit. 
# For example
# 	call verbsPlistToCsv('verbs-org.plist','verbs.csv')
#	edit 'verbs.csv' with Excel, Numbers, etc
#	call csvToVerbsPlist('verbs.csv','verbs-edited.plist')

def	verbsPlistToCsv(plistPath, csvPath):
	plist = plistlib.readPlist(plistPath)
	outFile = open(csvPath,'w')
	csvWriter = unicodecsv.writer(outFile,encoding='utf-8',delimiter=';')
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

# Save a new verbs.plist with the frequency of use
plistlib.writePlist(verbs,'verbs-freq.plist')

# Save also a csv copy to statistical analysis
verbsPlistToCsv('verbs-freq.plist','verbs-freq.csv')

