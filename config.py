from . import mylogging as logging

conf = dict()

conf['mode'] = 'test'
conf['global'] = dict()
conf['db_path'] = 'mydb.sqlite3'
conf['db_init_script'] = 'init.sql'