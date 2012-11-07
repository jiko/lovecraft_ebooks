#!/usr/bin/python
import init_twit as tw
import markov, time, os, re

# make a separate file for these reusable functions: bot.py
# main bot-specific app logic in app.py
# check out jamlitbot setup for best practices
def log(msg):
	with open('log','a') as f:
		f.write(msg+"\n")
	print msg

def genTweet():
	sentence = markov.genSentence(markovLength)
	while (len (sentence) > 123 or len(sentence) < 20):
		sentence = markov.genSentence(markovLength)
	return sentence

def tweet(irtsi=None,at=None): 
	status = genTweet()
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

def reply(mention):
	asker = mention['from_user']
	log(asker + " said " + mention['text'])
	status_id = str(mention['id'])
	if tw.last_id_replied < status_id:
		tw.last_id_replied = status_id
	tweet(status_id,asker)

markovLength = 3

corpus_files = []
[corpus_files.append("corpus/"+files) for files in os.listdir("corpus") if files.endswith(".txt")]

if (markov.mapping=={}):
	corpus = []
	[corpus.extend(markov.wordlist(filename)) for filename in corpus_files]
	markov.buildMapping(corpus,markovLength)

while True:
	results = tw.twitter.search(q="@"+tw.handle,since_id=tw.last_id_replied)['results']
	retweets = re.compile('rt\s',flags=re.I)
	results = [response for response in results if not retweets.search(response['text'])]
	if not results:
		log("Nobody's talking to me...")
	else:
		[reply(result) for result in results] 
	tweet()
	log("Sweet Dreams...")
	time.sleep(7600) # waits for two hours
