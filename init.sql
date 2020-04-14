DROP TABLE IF EXISTS twitter;
DROP TABLE IF EXISTS content;
DROP TABLE IF EXISTS like_list;
DROP TABLE IF EXISTS retwitter_list;
DROP TABLE IF EXISTS follower;

CREATE TABLE twitter(
	id integer primary key autoincrement,
	utype text, # lock unlock
	uid text,
	uname text,
	birthday text,
	joinedday text,
	signed text
);

CREATE TABLE content(
	id integer primary key autoincrement,
	pid integer,
	content text,  # 包括文字，媒体，图片链接
	twitter_id integer, # 发推者ID
	replay_id integer, # 如果是回复则回复的推特ID，否则就是-1
	ctime text # 发推时间
);

CREATE TABLE like_list(
	id integer primary key autoincrement,
	pid integer, # 推文ID
	ctime text, # 点赞时间
	uid integer # 用户ID 
);


CREATE TABLE retwitter_list(
	id integer primary key autoincrement,
	pid integer, # 推文ID
	ctime text, # 转推时间
	uid integer # 用户ID
);

CREATE TABLE follower(
	id integer primary key autoincrement,
	uid integer, # 被关注者
	follower_id integer, # 关注者
	ctime text # follower时间
);

# CREATE VIEW 互follow列表 
