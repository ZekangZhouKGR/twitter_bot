from . import mylogging as logging

def like_pair(host):
	like_pair = None
	return host,like_pair

def reply_pair(host):
	reply_pair = None
	return host,reply_pair

def repost_pair(host):
	repost_pair = None
	return host,repost_pair

def cofollow_pair(host):
	cofollow_pair = None
	return host,cofollow_pair

def like_group(core_user,level):
	return core_user,like_group

def reply_group(core_user,level):
	return core_user,reply_group

def repost_group(core_user,level):
	return core_user,repost_group
