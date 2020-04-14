from . import mylogging as logging
from .twitter_api import get_auth
from . import twitter_api

def get_twitter_content(args):
	return 

def get_twitter(screen_name, count = 200, max_id = 10e21):
	auth = get_auth()
	url = twitter_api.user_timeline.format(screen_name = screen_name,count = count,max_id = max_id)
	res = twitter = auth.get(url)
	if len(res) == count:
		min_id = min(res,key=lambda x:x['id'])['id']
		others = get_twitter(screen_name, count = count, max_id = min_id)
		return res + others 
	else:
		return res


def get_tweets(json_data):
	return json_data['globalObjects']['tweets']

def get_users(json_data):
	return json_data['globalObjects']['users']