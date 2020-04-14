from . import mylogging as logging
import sqlite3
from . import config

conf = config.conf

def get_db():
	logging.logger.debug('open {} database'.format(config['db_path']))
	if 'db' not in conf['global']:
		db = sqlite3.connect(conf['db_path'])
		conf['global']['db'] = db
	return db

def init_db():
	logging.logger.info('init db by {}'.format(conf['db_init_script']))
	db = get_db();cur = db.cursor()
	cur.executescript(conf['db_init_script'])
	db.commit()

def insert():
	pass

def query():
	pass

def remove():
	pass

def bak():
	pass

def update():
	pass


