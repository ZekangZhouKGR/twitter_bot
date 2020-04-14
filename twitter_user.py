from . import mylogging as logging
from .twitter_api import get_auth
from . import twitter_api

def get_twitter_user(screen_name):
	auth = get_auth()
	url = twitter_api.users_search.format(q=screen_name, page=1, count=5, include_entities=False)
	try:
		data = auth.get(url)[0]
		return data
	except:
		logging.logger.info('error at url %s' % url)

def get_user_followers(screen_name,cursor = -1,count = 200):
	auth = get_auth()
	try:
		url = twitter_api.followers_list.format(screen_name=screen_name,cursor=cursor,count = count);
		res = auth.get(url)
		follwers = res['users']
		next_cursor = res['next_cursor']
	except:
		logging.logger.info('error at url %s' % url)
	if len(followers) == count:
		others = get_user_followers(screen_name, cursor = next_cursor, count = count)
		follwers = follwers + others
	return follwers

def get_user_followings(screen_name,cursor = -1,count = 200):
	auth = get_auth()
	try:
		url = twitter_api.followering_list.format(screen_name=screen_name,cursor=cursor,count = count);
		res = auth.get(url)
		following = res['users']
		next_cursor = res['next_cursor']
	except:
		logging.logger.info('error at url %s' % url)
	if len(following) == count:
		others = get_user_followings(screen_name, cursor = next_cursor, count = count)
		following = following + others
	return following


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

