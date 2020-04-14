#from . import mylogging as logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import request_log as rlog
import sys
import time 
import os
import json
import twitter_api

import re

timeline = 'https://api.twitter.com/2/timeline/'

driver_path = os.environ['CHROMEDRIVER'] if 'CHROMEDRIVER' in os.environ else 'D:/chromedriver/chromedriver.exe'


from functools import wraps
global_temp = None

def is_twitter_api(func):
    @wraps(func)
    def www(*args,**kwargs):
        kwargs.setdefault('include_profile_interstitial_type',1)
        kwargs.setdefault('include_tweet_replies',1)
        kwargs.setdefault('include_blocking',1)
        kwargs.setdefault('include_blocked_by',1)
        kwargs.setdefault('include_followed_by',1)
        kwargs.setdefault('include_want_retweets',1)
        kwargs.setdefault('include_mute_edge',1)
        kwargs.setdefault('include_can_dm',1)
        kwargs.setdefault('include_can_media_tag',1)
        kwargs.setdefault('skip_status',1)
        kwargs.setdefault('cards_platform','Web-12')
        kwargs.setdefault('include_cards',1)
        kwargs.setdefault('include_composer_source','true')
        kwargs.setdefault('include_ext_alt_text','true')
        kwargs.setdefault('include_reply_count',1)
        kwargs.setdefault('tweet_mode','extended')
        kwargs.setdefault('include_entities','true')
        kwargs.setdefault('include_user_entities','true')
        kwargs.setdefault('include_ext_media_color','true')
        kwargs.setdefault('include_ext_media_availability','true')
        kwargs.setdefault('send_error_codes','true')
        kwargs.setdefault('simple_quoted_tweets','true')
        kwargs.setdefault('earned',1)
        kwargs.setdefault('lca','true')
        kwargs.setdefault('ext','mediaStats%2CcameraMoment')
        return func(*args,**kwargs)
    return www



class Twitter_Spider(object):
    """docstring for Twitter_Spider"""
    def __init__(self, chrome, har_log):
        super(Twitter_Spider, self).__init__()
        self._driver = chrome;
        self._twittersQueue = [];
        self._tweetsQueue = [];
        self._outTwittersQueue = [];
        self._outTweetsQueue = [];
        self._save_file = 'process.data'
        self._cookies_file = 'cookies.data'
        self._har_log = har_log

    def load(self):
        with open(self._save_file,'r') as f:
            data = json.load(data,f)
        self._twittersQueue = data[0]
        self._tweetsQueue = data[1]
        self._outTwittersQueue = data[2]
        self._outTweetsQueue = data[3]

    def save(self):
        data = [self._twittersQueue,self._tweetsQueue,self._outTwittersQueue,self._outTweetsQueue];
        with open(self._save_file,'w') as f:
            json.dump(data,f)
    
    def prepare(self):
        # 载入COOKIES
        import os
        self.login();
        if os.path.isfile(self._save_file):
            self.load();

    def login(self):
        if self.auto_login():
            return
        bowser = self._driver
        #login_page = 'https://passport.bilibili.com/login'
        login_page = 'https://www.twitter.com/login'
        bowser.get(login_page)
        time.sleep(30);
        cookies = bowser.get_cookies()
        with open(self._cookies_file,'w') as f:
            json.dump(cookies,f)
        return

    def auto_login(self):
        home_page = 'https://www.twitter.com/'
        bowser = self._driver
        bowser.get(home_page)
        if os.path.isfile(self._cookies_file):
            with open(self._cookies_file,'r') as f:
                cookies = json.load(f)
            for cookie in cookies:
                bowser.add_cookie({
                    'domain':cookie['domain'],
                    'name':cookie['name'],
                    'value':cookie['value']
                    })
            bowser.get(home_page)
            return True
        return False


    def run(self):
        for twitter in self.get_next_twitter():
            friends = self.run_friends(twitter);
            follwers = self.run_followers(twitter);
            timeline = self.run_timeline(twitter);
            self.putInTwittersQueue(friends);
            self.putInTwittersQueue(follwers);
            self.putInTweetsQueue(timeline)
            for tweet in self.get_next_tweet():
                replies = self.run_replies(tweet);
                retweeted = self.run_retweeted_by(tweet);
                liked_by = self.run_liked_by(tweet);
                #
                self.putInTweetsQueue(replies)
                self.putInTwittersQueue(retweeted)
                self.putInTweetsQueue(liked_by)
            self.save();

    def putInTwittersQueue(self):
        return

    def putInTweetsQueue(self):
        return

    def get_next_twitter(self):
        while True:
            if len(self._twittersQueue) == 0:
                break
            twitter = self._twittersQueue.pop();
            if twitter not in self._outTwittersQueue:
                yield twitter

    def get_next_tweet(self):
        while True:
            if len(self._tweetsQueue) == 0:
                break
            tweet = self._tweetsQueue.pop();
            if tweet not in self._outTweetsQueue:
                yield tweet

    def run_timeline(self,twitter):
        # 载入
        self._driver.get('https://twitter.com/{}'.format(twitter))
        entry = self.get_timeline_entry()
        #user_id = self.get_user_id(entry)
        self._headers = self.get_headers(entry)
        res = self.get_timeline(entry['request']['url'])
        urls = [];
        urls.append(entry['request']['url'])
        results = [];
        results.append(res)
        try:
            while True:
                entry = self.get_timeline_entry(ready = urls)
                if entry == None:
                    break
                self._headers = self.get_headers(entry)
                urls.append(entry['request']['url'])
                res = self.get_timeline(entry['request']['url'])
                results.append(res)
        except KeyboardInterrupt:
            pass
        except Exception as e:
            print(e)
        return results


    @is_twitter_api
    def get_timeline(self,url,**kwargs):
        import requests as rq
        headers = self._headers
        print(url)
        res = rq.get(url,headers = headers)
        return res.json()


    def find(self,d,key):
      if isinstance(d,dict):
        if key in d.keys():
          return d[key]
        else:
          for i in d.keys():
            r = self.find(d[i], key)
            if r != None:
              return r
      elif isinstance(d,list):
        for i in range(len(d)):
            r = self.find(d[len(d) - i - 1],key)
            if r != None:
              return r

    def run_friends(self,twitter):
        # 载入
        # 载入
        self._driver.get('https://twitter.com/{}/following'.format(twitter))
        entry = self.get_friend_entry()
        self._headers = self.get_headers(entry)
        res = self.get_timeline(entry['request']['url'])
        urls = [];
        urls.append(entry['request']['url'])
        results = [];
        results.append(res)
        try:
            while True:
                entry = self.get_friend_entry(ready = urls)
                if entry == None:
                    break
                self._headers = self.get_headers(entry)
                urls.append(entry['request']['url'])
                res = self.get_timeline(entry['request']['url'])
                results.append(res)
        except KeyboardInterrupt:
            pass
        except Exception as e:
            print(e)
        return results

    def run_followers(self,twitter):
        # 载入
        followers = []
        return follwers

    def run_replies(self,twitter,tweet):
        # 载入
        return replies

    def run_retweeted_by(self,tweets):
        # 载入
        self._driver.get('https://twitter.com/{}/status/{}/retweets'.format(twitter,tweet))
        return twitters

    def run_liked_by(self,tweets):
        # 载入
        self._driver.get('https://twitter.com/{}/status/{}/likes'.format(twitter,tweet))
        return twitters

    def run_search(self,keyword):
        # 载入
        return timeline

    def action_to_bottom(self):
        last = self._driver.execute_script('return document.documentElement.scrollTop'); 
        self._driver.execute_script('document.documentElement.scrollTop+=10000')
        cur = self._driver.execute_script('return document.documentElement.scrollTop')
        print(cur)
        return last == cur

    def get_height(self):
        pass

    def get_timeline_entry(self, uids = -1, ready = -1):
        import re
        if uids == -1:
            matcher = 'timeline/profile'
        else:
            matcher = 'timeline/profile/{}.json'.format(uids)
        while True:
            har = self._har_log.getHar();
            timeline = filter(lambda x: matcher in x['request']['url'], har['log']['entries']);
            if ready != -1:
                entry = tuple(filter(lambda x: x['request']['url'] not in ready, timeline))
            else:
                entry = tuple(timeline)
            if len(entry) > 1:
                return entry[-1]
            time.sleep(0.4)
            self.action_to_bottom()

    def get_friend_entry(self, ready = -1):
        import re
        matcher = 'friends/following'
        while True:
            har = self._har_log.getHar();
            following = filter(lambda x: matcher in x['request']['url'], har['log']['entries']);
            if ready != -1:
                entry = tuple(filter(lambda x: x['request']['url'] not in ready, following))
            else:
                entry = tuple(timeline)
            if len(entry) > 1:
                return entry[-1]
            time.sleep(0.4)
            self.action_to_bottom()
        else:
            return None

    def get_user_id(self,entry):
        uid = re.search('([\\d]+)(?=.json)',entry['request']['url']).group()
        return uid

    def get_headers(self,entry):
        source = entry['request']['headers']
        headers = {}
        for i in source:
            headers[i['name']] = i['value']
        if 'Accept-Encoding' in headers.keys():
            del headers['Accept-Encoding']
        return headers

    def get_cookies(self):
        source = self._driver.get_cookies()
        cookies = []
        for i in source:
            cookies.append({'domain':i['domain'],
                'name':i['name'],
                'value':i['value']})
        return cookies


def main():
    chrome = None;
    requestlog = None;
    try:
        chrome_options = Options()
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument('--allow-running-insecure-content')
        chrome_options.add_argument('--start-maximized')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1280,720')
        #caps = set_logger(chrome_options)
        requestlog = rlog.RequestLog('rlog.log')
        requestlog.setOptions(chrome_options)
        chrome = webdriver.Chrome(executable_path=driver_path,options = chrome_options)
        spider = Twitter_Spider(chrome, requestlog)
        spider.prepare()  # 登录或载入COOKIES
        screen_name = ''
        assert screen_name != ''
        #results = spider.run_timeline(screen_name)
        #json.dump(results,open(screen_name + '_tweets.json','w'))
        results = spider.run_friends(screen_name)
        json.dump(results,open(screen_name + '_friends.json','w'))
        #spider.action_to_bottom();
    finally:
        if chrome != None:
            #time.sleep(10);
            chrome.get_screenshot_as_file("test.png")
            chrome.quit()
        if requestlog != None:
            har = requestlog.getHar()
            har['log']['entries'] = [*filter(lambda x: 'api.twitter.com' in x['request']['url'],har['log']['entries'])]
            json.dump(har,open('rlog_' + str(int(time.time())) + '.har','w'))
            requestlog.close();

if __name__ == '__main__':
    spider = main()

    