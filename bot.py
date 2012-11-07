#!/usr/bin/python
import init_twit as tw
import markov, time, re, random, os

# make a separate file for these reusable functions: bot.py
# main bot-specific app logic in app.py
# check out jamlitbot setup for best practices
def log(msg):
	with open('log','a') as f:
		f.write(msg+"\n")
	print msg

def tweet(seq,irtsi=None,at=None): 
	status = random.choice(tweets[seq])
	try:
		if at and irtsi:
			status = "@"+at+" "+status
			tw.poster.statuses.update(status=status,in_reply_to_status_id=irtsi)
		else:
			tw.poster.statuses.update(status=status)
	except TwitterHTTPError as error:
		log(error)
	else:
		if irtsi: 
			status = "in reply to"+irtsi+": "+status
		log(status)

def reply(mention,seq):
	asker = mention['from_user']
	log(asker + " said " + mention['text'])
	status_id = str(mention['id'])
	if tw.last_id_replied < status_id:
		tw.last_id_replied = status_id
	tweet(seq,status_id,asker)

markovLength = 3

corpus_files = []
# get a list of all txt file in corpus folder

if (markov.mapping=={}):
	corpus = []
	[corpus.extend(markov.wordlist(filename)) for filename in corpus_files]
	markov.buildMapping(corpus,markovLength)

def genTweet():
	sentence = markov.genSentence(markovLength)
	while (len (sentence) > 140 or len(sentence) < 20):
		sentence = markov.genSentence(markovLength)
	return sentence

while True:
	results = tw.twitter.search(q="@"+tw.handle,since_id=tw.last_id_replied)['results']
	if not results:
		print "Nobody's talking to me...\n"
	for result in results:
		question = result['text'].replace('@jmkp','')
		asker = result['from_user']
		status_id = str(result['id'])
		print asker + " said '" + question + "'\n"
		sentence = genTweet()
		sentence = "@"+asker+" "+sentence
		print status_id+": "+sentence+"\n"
		if tw.last_id_replied < status_id:
			tw.last_id_replied = status_id
		tw.poster.statuses.update(status=sentence,in_reply_to_status_id=status_id)
	sentence = genTweet()
	print sentence+"\n"
	tw.poster.statuses.update(status=sentence)
	print "Sweet Dreams...\n"
	time.sleep(7600) # waits for two hours
