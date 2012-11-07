import re, random

tempMapping = {}
mapping = {}
starts = []

def fixCaps (word):
	# Ex: "FOO" -> "foo"
	if word.isupper () and word != "I":
		word = word.lower ()
	# Ex: "LaTeX" => "Latex"
	elif word [0].isupper ():
		word = word.lower().capitalize ()
	# Ex: "wOOt" -> "woot"
    	else:
        	word = word.lower()
	return word

def toHash (lst):
	return tuple (lst)

def wordlist (filename):
	f = open (filename, 'r')
	wordlist = [fixCaps (w) for w in re.findall (r"[\w']+|[.,!?;]", f.read ())]
	f.close ()
	return wordlist

def addItemToTempMapping (history, word):
	global tempMapping
	while len (history) > 0:
		first = toHash (history)
		if first in tempMapping:
			if word in tempMapping [first]:
				tempMapping [first][word] += 1.0
			else:
				tempMapping [first][word] = 1.0
		else:
			tempMapping [first] = {}
			tempMapping [first][word] = 1.0
		history = history [1:]

def buildMapping (wordlist, markovLength):
	global tempMapping
	starts.append (wordlist [0])
	for i in range (1, len (wordlist) - 1):
		if i <= markovLength:
			history = wordlist [: i + 1]
		else:
			history = wordlist [i - markovLength + 1 : i + 1]
		follow = wordlist [i + 1]
		# if the last elt was a period, add the next word to the start list
		if follow not in "'.,!?;":
			starts.append (follow)
		addItemToTempMapping (history, follow)
	# Normalize the values in tempMapping, put them into mapping
	for first, followset in tempMapping.iteritems ():
		total = sum (followset.values ())
		# Normalizing here:
		mapping [first] = dict ([(k, v / total) for k, v in followset.iteritems ()])

def next (prevList):
	sum = 0.0
	retval = ""
	index = random.random ()
	# Shorten prevList until it's in mapping
	while toHash (prevList) not in mapping:
		prevList.pop (0)
	# Get a random word from the mapping, given prevList
	for k, v in mapping [toHash (prevList)].iteritems ():
		sum += v
		if sum >= index and retval == "":
			retval = k
	return retval

def genSentence (markovLength):
	# Start with a random "starting word"
	curr = random.choice(starts)
	sent = curr.capitalize ()
	prevList = [curr]
	# Keep adding words until we hit a period
	while (curr not in ".!?"):
		curr = next (prevList)
		prevList.append (curr)
		# if the prevList has gotten too long, trim it
		if len (prevList) > markovLength:
			prevList.pop (0)
		if (curr in 'st'):
			sent += "'"
		elif (curr not in ".,!?;"):
			sent += " " # Add spaces between words (but not punctuation)	
		sent += curr
	return sent 
