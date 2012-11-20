#!/usr/bin/python
import init_twit as tw
import markovgen, time, re, random, codecs

# make a separate file for these reusable functions: bot.py
# main bot-specific app logic in app.py

corpus_file = 'corpus.txt'
with open(corpus_file) as text:
	markov = markovgen.Markov(text)

def log(msg):
	print msg
	with codecs.open('log','a','utf-8') as f:
		f.write(msg+"\n")

def genTweet():
	wc = random.randint(6,18)
	return markov.generate_markov_text(size=wc)

def tweet(status,irtsi=None,at=None): 
	try:
		if at and irtsi:
			status = "@"+at+" "+status
			tw.poster.statuses.update(status=status,in_reply_to_status_id=irtsi)
		else:
			pass
			tw.poster.statuses.update(status=status)
	except tw.TwitterError as error:
		log(error.response_data)
	else:
		if irtsi: 
			status = "In reply to "+irtsi+": "+status
		log(status)

def reply(txt,mention):
	asker = mention['from_user']
	log(asker + " said " + mention['text'])
	status_id = str(mention['id'])
	if tw.last_id_replied < status_id:
		tw.last_id_replied = status_id
	while len(txt) > 123:
		txt = genTweet()
	tweet(txt,status_id,asker)

while True:
	results = []
	#results = tw.twitter.search(q="@"+tw.handle,since_id=tw.last_id_replied)['results']
	#retweets = re.compile('rt\s',flags=re.I)
	#results = [response for response in results if not retweets.search(response['text'])]
	if not results:
		log("Nobody's talking to me...")
	else:
		[reply(genTweet(),result) for result in results] 
	tweet(genTweet())
	log("Sweet Dreams...")
	time.sleep(7600) # waits for two hours
