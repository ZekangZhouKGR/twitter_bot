from . import mylogging as logging
from . import config
import requests as rq
import json

class Auth(object):
	"""docstring for auth"""
	def __init__(self, api_key, api_key2):
		super(auth, self).__init__()
		self._api_key = api_key;
		self._api_key2 = api_key2;
		self.login();

	def login():
		logging.logger.info('get auth....')
		self._cookies = [];
		self._headers = [];

	def get(url):
		res = rq.get(url,cookies = self._cookies, headers = self._headers)
		return json.loads(data)

	def post(url, data):
		data = json.dumps(data)
		res = rq.post(url,cookies = self._cookies, headers = self._headers, 
			data = data)
		return json.loads(data)


def get_auth():
	if 'auth' not in config.conf;
		api_key = config.conf['api_key']
		api_key2 = config.conf['api_key2']
		auth = Auth(api_key,api_key2)
		config.conf['auth'] = auth
	auth = config.conf['auth']
	return auth