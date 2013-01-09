import fileinput
import plistlib

freq50K = {}
for line in fileinput.input('en_50K.txt'):
	#we need to remove the original EOL
	line = line[:len(line)-2].split(' ')
	freq50K.update({line[0]:int(line[1])})


freqVerbs = {}	
verbs = plistlib.readPlist('verbs.plist')
for verb in verbs:
	verbalForm = verb.values()
	count = freq50K.get(verbalForm[0],0) 	# simple
	count += freq50K.get(verbalForm[1],0) 	# past
	count += freq50K.get(verbalForm[3],0) 	# participle
	freqVerbs.update({verbalForm[0]:count})
	
list = []
for v,f in freqVerbs.items():
	list.append("%010d%s"%(f,v));
	
list.sort()
	
print list

