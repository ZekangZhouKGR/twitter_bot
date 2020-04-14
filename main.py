from . import mylogging as logging
from . import config
from . import db

logger = logging.logger
conf = config.conf

def main():
	logger.info('into main...');
	logger.info('application\'s mode is {}'.format(conf['mode']))
	pass




if __name__ == '__main__':
	main()