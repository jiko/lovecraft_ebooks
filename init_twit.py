from twitter import Twitter, TwitterError
from twitter.oauth import OAuth, read_token_file
from twitter.oauth_dance import oauth_dance
import os

# get your own at https://dev.twitter.com/apps/new
CONSUMER_KEY='MSkGnYHDUgDxZbTBDkfP8Q'
CONSUMER_SECRET='BEN3D56OWddggyuYUUcENWK1OPmqVCy5EGIq1mg'

# path to where your oauth credentials are stored 
oauth_filename = os.environ.get('HOME', '') + os.sep + '.lovecraft_oauth'
# use the function 'from twitter.oauth import write_token_file' to create this file
oauth_token, oauth_token_secret = read_token_file(oauth_filename)

twitter = Twitter(domain='search.twitter.com')
twitter.uriparts = ()

poster = Twitter(
	auth=OAuth(
		oauth_token, oauth_token_secret, CONSUMER_KEY, CONSUMER_SECRET),
		secure=True,
		api_version='1',
		domain='api.twitter.com')

# get the status_id of the last tweet to which you replied
last_id_replied = [tweet['in_reply_to_status_id'] for tweet in poster.statuses.user_timeline() if tweet['in_reply_to_status_id'] != None][0]
# your bot's twitter handle
handle = "lovecraft_ebook"
