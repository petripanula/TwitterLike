import requests
import os
import json
import sys
import string
import time
import random
import pickle
import logging
from datetime import datetime
from datetime import date
from requests_oauthlib import OAuth1Session

# To set your enviornment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'

MY_TWITTER_ID = "2776468107"
MOBILE_DONK_ID = "1416302384393953282"

NEGATIVE_WORDS = ["pumped", "PUMPED", "PUMPING", "pumping", "Giving", "winners", "group", "follows", "follow", "Join", "luck", "faucet", "dodge", "Elon", "VIP", "vip", "project", "holders", "HOLDERS", "sugar"]
AUTHOR_LIST = []
MY_FOLLOWERS_LIST = []
START_TIME_LIMIT = time.time() - 900
ERRORS = 0
VERSION = 2
SAVED_EPOCH_TIME = 0
BEGIN_TIME = datetime. now()
MAX_LIKES = 991

def setup_custom_logger(name):
    ''' my custom logger '''
    formatter = logging.Formatter(fmt='%(asctime)s.%(msecs)03d %(levelname)-8s %(message)s',
                                  datefmt='%Y-%m-%d %H:%M:%S')
    today = date.today()
    d1 = today.strftime("%d_%m_%Y_")
    handler = logging.FileHandler(d1+'log.txt', mode='a')
    handler.setFormatter(formatter)
    screen_handler = logging.StreamHandler(stream=sys.stdout)
    screen_handler.setFormatter(formatter)
    mylogger = logging.getLogger(name)
    mylogger.setLevel(logging.DEBUG)
    mylogger.addHandler(handler)
    mylogger.addHandler(screen_handler)
    return mylogger


def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers


def get_rules(headers, bearer_token):
    response = requests.get(
        "https://api.twitter.com/2/tweets/search/stream/rules", headers=headers
    )
    if response.status_code != 200:
        raise Exception(
            "Cannot get rules (HTTP {}): {}".format(response.status_code, response.text)
        )
    LOGGER.info(json.dumps(response.json()))
    return response.json()


def delete_all_rules(headers, bearer_token, rules):
    if rules is None or "data" not in rules:
        return None

    ids = list(map(lambda rule: rule["id"], rules["data"]))
    payload = {"delete": {"ids": ids}}
    response = requests.post(
        "https://api.twitter.com/2/tweets/search/stream/rules",
        headers=headers,
        json=payload
    )
    if response.status_code != 200:
        raise Exception(
            "Cannot delete rules (HTTP {}): {}".format(
                response.status_code, response.text
            )
        )
    LOGGER.info(json.dumps(response.json()))


def set_rules(headers, delete, bearer_token):
    # You can adjust the rules if needed
    sample_rules = [
        #{"value": "lang:en (SHIB OR safemoon OR XRP OR AKITA OR FEG OR HOGE OR ERC20 OR DOGE OR pitbullish) -@safemoon_art -ECLIPSETOKEN -SAFEMARS -GIVEAWAY -safetesla -teslasafe -pump -join -pumping -pumped -winner -giveaway -Giving -address -follow -help -wallet -is:retweet -has:links", "tag": "shib OR pitbullish OR XRP OR safemoon OR feg OR HOGE OR ERC20 OR DOGE"},
        {"value": "lang:en (cryptocurrency OR altseason OR BTC OR XRP OR ethereum) -pig -CasinoCoin -SHIB -ChumToken -safemoon -akita -feg -doge -hoge -ECLIPSETOKEN -SAFEMARS -GIVEAWAY -safetesla -teslasafe -pump -join -pumping -block -version -pumped -price -blocks -value -winner -giveaway -Giving -address -adress -babyxrp -BabyCake -Contract -follow -help -unusual -bot -change -funds -pending -transactions -transaction -CryptoSignals -Technical -trade -volume -circulation -stake -WHALEALERT -is:reply -is:retweet -has:links", "tag": ""},
    ]
    payload = {"add": sample_rules}
    response = requests.post(
        "https://api.twitter.com/2/tweets/search/stream/rules",
        headers=headers,
        json=payload,
    )
    if response.status_code != 201:
        raise Exception(
            "Cannot add rules (HTTP {}): {}".format(response.status_code, response.text)
        )
    LOGGER.info(json.dumps(response.json()))


def test_if_tweet_has_address(tweet):
    words = tweet.split()
    for word in words:
        if word[:2] == "0x":
            LOGGER.info("Probably address in tweet?")
            return True
        if "0x" in word:
            LOGGER.info("Probably address in tweet?")
            return True            
    return False
    
def get_24h_likes(NBR_LIKED_24H_TWEETS,received_tweets,timerange=86400):
    global SAVED_EPOCH_TIME
    likes24h = 0    
    current_epoch=int(time.mktime(datetime.now().timetuple()))
    for like in NBR_LIKED_24H_TWEETS:
        if current_epoch < (like+timerange):
            likes24h = likes24h + 1

    LOG = "Likes during last %s hours: %s received_tweets: %s" %(int(timerange/3600),likes24h,received_tweets)
    LOGGER.info(LOG)

    if(likes24h > MAX_LIKES and int(SAVED_EPOCH_TIME) < current_epoch):
        LOGGER.info("We should put breaks on...")
        LOG = "Script started: %s" % BEGIN_TIME
        LOGGER.info(LOG)
        current_epoch=time.mktime(datetime.now().timetuple())
        SAVED_EPOCH_TIME = current_epoch + 900 #Just 15min break?

    return likes24h
        
def get_followers_list_v11():
    #my followers list
    consumer_key = os.environ.get("CONSUMER_KEY")
    consumer_secret = os.environ.get("CONSUMER_SECRET")
    #payload = {"tweet_id": tweet_id}
    request_token_url = "https://api.twitter.com/oauth/request_token"
    oauth = OAuth1Session(consumer_key, client_secret=consumer_secret)
    try:
        fetch_response = oauth.fetch_request_token(request_token_url)
    except ValueError:
        LOGGER.error("There may have been an issue with the consumer_key or consumer_secret you entered.")
    resource_owner_key = fetch_response.get("oauth_token")
    resource_owner_secret = fetch_response.get("oauth_token_selfecret")
    #print("Got OAuth token: %s" % resource_owner_key)

    with open('auth.json') as json_file:
        oauth_tokens = json.load(json_file)

    access_token = oauth_tokens["oauth_token"]
    access_token_secret = oauth_tokens["oauth_token_secret"]

    # Make the request
    oauth = OAuth1Session(
        consumer_key,
        client_secret=consumer_secret,
        resource_owner_key=access_token,
        resource_owner_secret=access_token_secret,
    )

    #This only with V1.1
    #url = "https://api.twitter.com/1.1/application/rate_limit_status.json?resources=tweets"
    url = "https://api.twitter.com/1.1/followers/ids.json?%s" %MY_TWITTER_ID
     
    response = oauth.get(url)
        
    for response_line in response.iter_lines():
        if response_line:
            json_response = json.loads(response_line)
            json_dump = (json.dumps(json_response, indent=4, sort_keys=True))
            followers=json.dumps(json_response["ids"])

    followers=followers.strip('[')
    followers=followers.strip(']')
    followers=followers.strip(' ')
    MY_FOLLOWERS_LIST = followers.split(",")
    #LOGGER.info(MY_FOLLOWERS_LIST)
    
    with open('my_followers.txt', 'rb') as fp:
        MY_FOLLOWERS_LIST_ORG = pickle.load(fp)
        #https://www.geeksforgeeks.org/python-set-method/
        MY_DIFF_LIST = set(MY_FOLLOWERS_LIST_ORG) ^ set(MY_FOLLOWERS_LIST)
        LOGGER.info("My Changed Follower list below:")
        LOGGER.info(MY_DIFF_LIST)

        #Just remove dublicates
        MY_DIFF_LIST_NEW = []
        for user in MY_DIFF_LIST:
            if user not in MY_DIFF_LIST_NEW:
                MY_DIFF_LIST_NEW.append(user)

        LOGGER.info(MY_DIFF_LIST_NEW)
        for user in MY_DIFF_LIST_NEW:
            LOG = "User:%s:" %user
            LOGGER.info(LOG)
            if user in MY_FOLLOWERS_LIST_ORG:
                LOG = "User %s is UnFollower" %user
                LOGGER.info(LOG)
                username = get_info_from_id(user,"username")
                LOGGER.info(username)

                if check_in_my_following_list(user):
                    LOGGER.info("I was following this user so we should also unfollow!!")
                    unfollow_user(user)
            else:
                LOG = "User %s is New Follower" %user
                LOGGER.info(LOG)
                user_followers = get_info_from_id(user,"followers_count")
                LOGGER.info(user_followers)

                if user_followers.isnumeric():
                    if int(user_followers) > 1000:
                        LOGGER.info("We Should Follow this!!")
                        follow_user(user)
                    else:
                        LOGGER.info("Less than 1000 followers")   
                else:
                    LOGGER.info("Probably NA....")
                    
    with open('my_followers.txt', 'wb') as fp:
        pickle.dump(MY_FOLLOWERS_LIST, fp)    

def check_in_my_following_list(userid):
    userid = userid.strip()
    userid = userid.replace(" ", "")
    LOG = "userid:%s:" %userid
    LOGGER.info(LOG)
    consumer_key = os.environ.get("CONSUMER_KEY")
    consumer_secret = os.environ.get("CONSUMER_SECRET")
    #payload = {"target_user_id": userid}
    request_token_url = "https://api.twitter.com/oauth/request_token"
    oauth = OAuth1Session(consumer_key, client_secret=consumer_secret)
    try:
        fetch_response = oauth.fetch_request_token(request_token_url)
    except ValueError:
        LOGGER.error("There may have been an issue with the consumer_key or consumer_secret you entered.")

    with open('auth.json') as json_file:
        oauth_tokens = json.load(json_file)

    access_token = oauth_tokens["oauth_token"]
    access_token_secret = oauth_tokens["oauth_token_secret"]

    # Make the request
    oauth = OAuth1Session(
        consumer_key,
        client_secret=consumer_secret,
        resource_owner_key=access_token,
        resource_owner_secret=access_token_secret,
    )

    response = oauth.get("https://api.twitter.com/2/users/{}/following".format(MY_TWITTER_ID))
    json_response = response.json()
    #LOGGER.info(json.dumps(json_response, indent=4, sort_keys=True))
    data = json.dumps(json_response, indent=4, sort_keys=True)
    if userid in data:
        LOGGER.info("This user is in my following list")
        return True
    else:
        return False
    
    
def unfollow_user(userid):
    userid = userid.strip()
    #V2.0
    consumer_key = os.environ.get("CONSUMER_KEY")
    consumer_secret = os.environ.get("CONSUMER_SECRET")
    #payload = {"target_user_id": userid}
    request_token_url = "https://api.twitter.com/oauth/request_token"
    oauth = OAuth1Session(consumer_key, client_secret=consumer_secret)
    try:
        fetch_response = oauth.fetch_request_token(request_token_url)
    except ValueError:
        LOGGER.error("There may have been an issue with the consumer_key or consumer_secret you entered.")

    with open('auth.json') as json_file:
        oauth_tokens = json.load(json_file)

    access_token = oauth_tokens["oauth_token"]
    access_token_secret = oauth_tokens["oauth_token_secret"]

    # Make the request
    oauth = OAuth1Session(
        consumer_key,
        client_secret=consumer_secret,
        resource_owner_key=access_token,
        resource_owner_secret=access_token_secret,
    )

    response = oauth.delete("https://api.twitter.com/2/users/{}/following/{}".format(MY_TWITTER_ID,userid))
    json_response = response.json()
    LOGGER.info(json.dumps(json_response, indent=4, sort_keys=True))

def follow_user(userid):
    userid = userid.strip()
    #V2.0
    consumer_key = os.environ.get("CONSUMER_KEY")
    consumer_secret = os.environ.get("CONSUMER_SECRET")
    payload = {"target_user_id": userid}
    request_token_url = "https://api.twitter.com/oauth/request_token"
    oauth = OAuth1Session(consumer_key, client_secret=consumer_secret)
    try:
        fetch_response = oauth.fetch_request_token(request_token_url)
    except ValueError:
        LOGGER.error("There may have been an issue with the consumer_key or consumer_secret you entered.")

    with open('auth.json') as json_file:
        oauth_tokens = json.load(json_file)

    access_token = oauth_tokens["oauth_token"]
    access_token_secret = oauth_tokens["oauth_token_secret"]

    # Make the request
    oauth = OAuth1Session(
        consumer_key,
        client_secret=consumer_secret,
        resource_owner_key=access_token,
        resource_owner_secret=access_token_secret,
    )

    response = oauth.post("https://api.twitter.com/2/users/{}/following".format(MY_TWITTER_ID), json=payload)
    json_response = response.json()
    LOGGER.info(json.dumps(json_response, indent=4, sort_keys=True))

def get_info_from_id(userid,info):
    userid = userid.strip()
    #V2.0
    consumer_key = os.environ.get("CONSUMER_KEY")
    consumer_secret = os.environ.get("CONSUMER_SECRET")
    payload = {"user.fields": "description"}
    request_token_url = "https://api.twitter.com/oauth/request_token"
    oauth = OAuth1Session(consumer_key, client_secret=consumer_secret)
    try:
        fetch_response = oauth.fetch_request_token(request_token_url)
    except ValueError:
        LOGGER.error("There may have been an issue with the consumer_key or consumer_secret you entered.")

    with open('auth.json') as json_file:
        oauth_tokens = json.load(json_file)

    access_token = oauth_tokens["oauth_token"]
    access_token_secret = oauth_tokens["oauth_token_secret"]

    # Make the request
    oauth = OAuth1Session(
        consumer_key,
        client_secret=consumer_secret,
        resource_owner_key=access_token,
        resource_owner_secret=access_token_secret,
    )

    my_url = "https://api.twitter.com/2/users/{}?user.fields=created_at,public_metrics".format(userid)
    response = oauth.get(my_url)
    json_response = response.json()
    LOGGER.info(json.dumps(json_response, indent=4, sort_keys=True))

    if "data" not in json.dumps(json_response):
        LOGGER.info("No data in json!")
        return "Mr.NoBody"
    #username=json.dumps(json_response[json_string]) #v2.0
    if "username" in info:
        info=json.dumps(json_response["data"]["username"]) #v2.0
    if "followers_count" in info:
        info=json.dumps(json_response["data"]["public_metrics"]["followers_count"]) #v2.0        
    return info
    

def get_rate_limits_v11():
    
    consumer_key = os.environ.get("CONSUMER_KEY")
    consumer_secret = os.environ.get("CONSUMER_SECRET")
    #payload = {"tweet_id": tweet_id}
    request_token_url = "https://api.twitter.com/oauth/request_token"
    oauth = OAuth1Session(consumer_key, client_secret=consumer_secret)
    try:
        fetch_response = oauth.fetch_request_token(request_token_url)
    except ValueError:
        LOGGER.error("There may have been an issue with the consumer_key or consumer_secret you entered.")

    resource_owner_key = fetch_response.get("oauth_token")
    resource_owner_secret = fetch_response.get("oauth_token_selfecret")
    #print("Got OAuth token: %s" % resource_owner_key)

    with open('auth.json') as json_file:
        oauth_tokens = json.load(json_file)

    #print(oauth_tokens)

    access_token = oauth_tokens["oauth_token"]
    access_token_secret = oauth_tokens["oauth_token_secret"]

    # Make the request
    oauth = OAuth1Session(
        consumer_key,
        client_secret=consumer_secret,
        resource_owner_key=access_token,
        resource_owner_secret=access_token_secret,
    )

    #This only with V1.1
    #url = "https://api.twitter.com/1.1/application/rate_limit_status.json?resources=tweets"
    url = "https://api.twitter.com/1.1/application/rate_limit_status.json"
     
    response = oauth.get(url)
    json_response = response.json()
    LOGGER.info(json.dumps(json_response, indent=4, sort_keys=True))
        

    
def like_tweet(tweet_id):
    global START_TIME_LIMIT
    global ERRORS
    global VERSION
    global SAVED_EPOCH_TIME

    current_epoch=time.mktime(datetime.now().timetuple())

    if  int(current_epoch) < int(SAVED_EPOCH_TIME):
        ts1 = datetime.fromtimestamp(int(current_epoch)).strftime('%Y-%m-%d %H:%M:%S')
        ts2 = datetime.fromtimestamp(int(SAVED_EPOCH_TIME)).strftime('%Y-%m-%d %H:%M:%S')
        LOG = "We return due to limit %s < %s" % (ts1,ts2)
        LOGGER.info(LOG)
        return 1
    
    consumer_key = os.environ.get("CONSUMER_KEY")
    consumer_secret = os.environ.get("CONSUMER_SECRET")
    payload = {"tweet_id": tweet_id}
    request_token_url = "https://api.twitter.com/oauth/request_token"
    oauth = OAuth1Session(consumer_key, client_secret=consumer_secret)
    try:
        fetch_response = oauth.fetch_request_token(request_token_url)
    except ValueError:
        LOGGER.error("There may have been an issue with the consumer_key or consumer_secret you entered.")

    with open('auth.json') as json_file:
        oauth_tokens = json.load(json_file)

    access_token = oauth_tokens["oauth_token"]
    access_token_secret = oauth_tokens["oauth_token_secret"]

    # Make the request
    oauth = OAuth1Session(
        consumer_key,
        client_secret=consumer_secret,
        resource_owner_key=access_token,
        resource_owner_secret=access_token_secret,
    )

    #This only with V1.1
    url = "https://api.twitter.com/1.1/favorites/create.json?id=%s" %int(tweet_id)
    
    if VERSION == 2:
        VERSION = 2
        response = oauth.post("https://api.twitter.com/2/users/{}/likes".format(MY_TWITTER_ID), json=payload)
    else:
        LOGGER.info("We use v1")
        VERSION = 1
        response = oauth.post(url, json=payload)

    if response.status_code != 200:
        LOG = "Like request returned an error: {} {}".format(response.status_code, response.text)
        LOGGER.error(LOG)
        skip_pause = 0
        if "Service Unavailable" in response.text:
            LOGGER.info("Service Unavailable...")
            skip_pause = 1
        if "This tweet cannot be found" in response.text:
            LOGGER.info("This tweet cannot be found...")
            skip_pause = 1
        if "Unauthorized" in response.text:
            LOGGER.info("Unauthorized...")
            skip_pause = 1
        if "Rate limit" in response.text:
            LOGGER.info("Rate limit...")
        if "Too Many Requests" in response.text:
            LOGGER.info("Too Many Requests...")
        if "Internal Server Error" in response.text:
                LOGGER.info("Internal Server Error...")
                sys.exit(0)

        LOGGER.info(response.headers)

        if skip_pause == 0:
            reset_epoch_time=response.headers['x-rate-limit-reset']
            ts = datetime.fromtimestamp(int(reset_epoch_time)).strftime('%Y-%m-%d %H:%M:%S')
            LOG = "Current rate limit will reset at %s" %ts
            LOGGER.info(LOG)
            SAVED_EPOCH_TIME = reset_epoch_time
        """        
        print("Let's try to switch version...")
        if VERSION == 2:
            VERSION = 1
        else:
            VERSION = 2
        """
        ERRORS = ERRORS + 1

        if ERRORS > 5:
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            LOG = "Current Time =", current_time
            LOGGER.info(LOG)
            START_TIME_LIMIT = time.time()
            ERRORS = 0
        return 1
    else:
        ERRORS = 0
        LOG = "Response code: {}".format(response.status_code)
        LOGGER.info(LOG)

        if "x-rate-limit-remaining" not in response.headers:
            LOGGER.info("no x-rate-limit-remaining in response")
            return 1
                    
        x_rate_limit_remaining = response.headers['x-rate-limit-remaining']
        LOG = "like_tweet - x_rate_limit_remaining: %s" % x_rate_limit_remaining
        LOGGER.info(LOG)        

        if int(x_rate_limit_remaining) < 5:
            LOGGER.info("Let's slow down a bit")
            LOG = "Script started: %s" % BEGIN_TIME
            LOGGER.info(LOG)
            current_epoch=time.mktime(datetime.now().timetuple())
            SAVED_EPOCH_TIME = current_epoch + 120 #Just 2 min break
            
        # Saving the response as JSON
        json_response = response.json()

    return 0

def check_how_many_like_list_is_in_follower_list():
    my_count = 0
    with open ('likelist.txt', 'rb') as fp:
        AUTHOR_LIST = pickle.load(fp)
        LOG = "AUTHOR_LIST len: %s" % len(AUTHOR_LIST)
        LOGGER.debug(LOG)

        with open('my_followers.txt', 'rb') as fp:
            MY_FOLLOWERS_LIST = pickle.load(fp)
            LOG = "MY_FOLLOWERS_LIST len: %s" % len(MY_FOLLOWERS_LIST)
            LOGGER.debug(LOG)

            for follower in AUTHOR_LIST:
                LOGGER.debug(follower)

            for follower in MY_FOLLOWERS_LIST:
                follower = follower.strip(' ')
                #LOG = ":%s:" % follower
                #LOGGER.debug(LOG)
                if follower in AUTHOR_LIST:
                     LOGGER.debug("Follower found in likelist")
                     my_count = my_count + 1

    LOG = "MY_COUNT: %s" % my_count
    LOGGER.info(LOG)
    
                
def get_user_followers(headers,userid):
    global START_TIME_LIMIT
    global SAVED_EPOCH_TIME
    followers = "99999"
    friends = "99999"
    joined = "Tue Apr 06 11:16:49 +0000 2008" 
    current_epoch=time.mktime(datetime.now().timetuple())
    
    if  int(current_epoch) < int(SAVED_EPOCH_TIME) and userid != MY_TWITTER_ID:
        ts1 = datetime.fromtimestamp(int(current_epoch)).strftime('%Y-%m-%d %H:%M:%S')
        ts2 = datetime.fromtimestamp(int(SAVED_EPOCH_TIME)).strftime('%Y-%m-%d %H:%M:%S')
        LOG = "get_user_followers: We return due to limit %s < %s" % (ts1,ts2)
        LOGGER.info(LOG)
        return followers, friends, joined
    
    followers = 0

    #V2.0
    consumer_key = os.environ.get("CONSUMER_KEY")
    consumer_secret = os.environ.get("CONSUMER_SECRET")
    payload = {"user.fields": "description"}
    request_token_url = "https://api.twitter.com/oauth/request_token"
    oauth = OAuth1Session(consumer_key, client_secret=consumer_secret)
    try:
        fetch_response = oauth.fetch_request_token(request_token_url)
    except ValueError:
        LOGGER.error("There may have been an issue with the consumer_key or consumer_secret you entered.")

    with open('auth.json') as json_file:
        oauth_tokens = json.load(json_file)

    access_token = oauth_tokens["oauth_token"]
    access_token_secret = oauth_tokens["oauth_token_secret"]

    # Make the request
    oauth = OAuth1Session(
        consumer_key,
        client_secret=consumer_secret,
        resource_owner_key=access_token,
        resource_owner_secret=access_token_secret,
    )

    my_url = "https://api.twitter.com/2/users/{}?user.fields=created_at,public_metrics".format(userid)
    response = oauth.get(my_url)

    #V1.1
    #url = "https://api.twitter.com/1.1/users/show.json?user_id=%s" %userid
    #response = requests.get(url, headers=headers)

    if response.status_code != 200:
        LOG = "Followers get returned error (HTTP {}): {}".format(response.status_code, response.text)
        LOGGER.error(LOG)

        LOGGER.info(response.headers)
        reset_epoch_time=response.headers['x-rate-limit-reset']
        ts = datetime.fromtimestamp(int(reset_epoch_time)).strftime('%Y-%m-%d %H:%M:%S')
        LOG = "Current rate limit will reset at %s" %ts
        LOGGER.info(LOG)
        SAVED_EPOCH_TIME = reset_epoch_time
        return followers, friends, joined


    if "x-rate-limit-remaining" not in response.headers:
        LOGGER.info("no x-rate-limit-remaining is header")
        return followers, friends, joined
    
    x_rate_limit_remaining = response.headers['x-rate-limit-remaining']
    if int(x_rate_limit_remaining) < 100:
        LOG = "get_user_followers - x_rate_limit_remaining: %s" % x_rate_limit_remaining
        LOGGER.info(LOG)
    
    if int(x_rate_limit_remaining) < 5:
        LOGGER.info("Let's slow down a bit")
        LOG = "Script started: %s" % BEGIN_TIME
        LOGGER.info(LOG)        
        current_epoch=time.mktime(datetime.now().timetuple())
        SAVED_EPOCH_TIME = current_epoch + 60 #Just 1 min break

    for response_line in response.iter_lines():
        if response_line:
            json_response = json.loads(response_line)
            if "data" not in json.dumps(json_response):
                LOGGER.info("No data in json!")
                break
            json_response = json.loads(response_line)
            json_dump = (json.dumps(json_response, indent=4, sort_keys=True))
            #print(json_dump)
            #followers=json.dumps(json_response["followers_count"])
            #friends=json.dumps(json_response["friends_count"])
            #joined=json.dumps(json_response["created_at"])
            joined=json.dumps(json_response["data"]["created_at"]) #v2.0
            followers=json.dumps(json_response["data"]["public_metrics"]["followers_count"]) #v2.0
            friends=json.dumps(json_response["data"]["public_metrics"]["following_count"])   #v2.0
            #print(joined)
            
    return followers, friends, joined

def get_stream(headers, set, bearer_token, AUTHOR_LIST, NBR_LIKED_24H_TWEETS, received_tweets,MY_FOLLOWERS_LIST):
    global SAVED_EPOCH_TIME
    at_the_begin = 1
    current_epoch_tmp_saved = 0
    current_epoch_tmp_saved2 = 0
    current_epoch_at_start=time.mktime(datetime.now().timetuple())
    while True:
        if at_the_begin == 1:
            at_the_begin = 0
            my_followers_at_start,friends,joined = get_user_followers(headers,MY_TWITTER_ID)
            LOG = "*** My followers count at the begin: %s" %my_followers_at_start
            LOGGER.info(LOG)
            received_tweets_start = received_tweets

        likes24h = get_24h_likes(NBR_LIKED_24H_TWEETS,received_tweets)
        current_epoch=time.mktime(datetime.now().timetuple())
        if  int(current_epoch) < int(SAVED_EPOCH_TIME):
            ts1 = datetime.fromtimestamp(int(current_epoch)).strftime('%Y-%m-%d %H:%M:%S')
            ts2 = datetime.fromtimestamp(int(SAVED_EPOCH_TIME)).strftime('%Y-%m-%d %H:%M:%S')
            LOG = "We do not reconnect yet %s < %s" % (ts1,ts2)
            LOGGER.info(LOG)
            time.sleep(60)
            continue
        if likes24h > MAX_LIKES:
            LOG = "We do not reconnect yet due to likes: %s" % likes24h
            LOGGER.info(LOG)
            time.sleep(60)
            continue
        try:
            LOGGER.info("We send the http get...")
            response = requests.get(
                "https://api.twitter.com/2/tweets/search/stream?expansions=author_id", headers=headers, stream=True,
            )
            LOG = "HTTP GET stream response code: %s" %response.status_code
            LOGGER.info(LOG)
            if response.status_code != 200:
                LOG = "resp: %s %s" % (response.status_code, response.text)
                LOGGER.error(LOG)
                if "This stream is currently at the maximum allowed connection limit" in response.text:
                    LOGGER.info("We sleep 60 seconds and reconnect...")
                    time.sleep(60)
                    continue
                else:
                    LOGGER.info("We make the exit....")
                    sys.exit(0)

            for response_line in response.iter_lines():
                if response_line:
                    received_tweets = received_tweets + 1
                    
                    likes1h = get_24h_likes(NBR_LIKED_24H_TWEETS,received_tweets,3600)  #Get likes from last hour
                    likes3h = get_24h_likes(NBR_LIKED_24H_TWEETS,received_tweets,10800)  #Get likes from last hour
                    LOG = "1 hour likes: %s. 3 hour likes: %s." %(likes1h, likes3h)
                    LOGGER.info(LOG)
                    current_epoch_tmp=time.mktime(datetime.now().timetuple())


                    #Let's try to pause if already 50 likes per hour
                    #Over 50 is not maybe human behaviour??
                    if likes1h >= 50 and current_epoch_tmp > current_epoch_tmp_saved2 + 1800: 
                        current_epoch_tmp_saved2=time.mktime(datetime.now().timetuple())
                        my_followers_now,friends,joined = get_user_followers(headers,MY_TWITTER_ID)
                        current_epoch=time.mktime(datetime.now().timetuple())
                        LOGGER.info("* Over 50 likes during last hour - let's push breaks *****************************************************************")
                        SAVED_EPOCH_TIME = current_epoch + 1800
                        get_followers_list_v11()
                        
                    #It has been investigated 3 followers per 100 likes should come. If now maybe need to do something....
                    '''
                    if likes3h >= 100 and current_epoch_tmp > current_epoch_tmp_saved + 1800 and current_epoch_tmp > current_epoch_at_start + 1800: 
                        current_epoch_tmp_saved=time.mktime(datetime.now().timetuple())
                        my_followers_now,friends,joined = get_user_followers(headers,MY_TWITTER_ID)
                        if my_followers_now <= my_followers_at_start:
                            LOG = "* My followers count at the begin: %s now: %s" % (my_followers_at_start, my_followers_now)
                            LOGGER.info(LOG)
                            current_epoch=time.mktime(datetime.now().timetuple())
                            LOGGER.info("* No new followers so we should wait couple of hours now *****************************************************************")
                            SAVED_EPOCH_TIME = current_epoch + 7200
                        my_followers_at_start = my_followers_now
                    '''
                    with open('nbr_tweets.txt', 'wb') as fp:
                        pickle.dump(received_tweets, fp)

                    if int(received_tweets % 10 == 0):
                        LOG = "received_tweets: %s" %received_tweets
                        LOGGER.info(LOG)
                    json_response = json.loads(response_line)
                    json_dump = (json.dumps(json_response, indent=4, sort_keys=True))
                    number_of_percentages = json_dump.count('%')
                    #LOGGER.debug(json_dump)
                    negative = 0
                    for my_words in NEGATIVE_WORDS:
                        if my_words in json_dump:
                            LOG = "Negative word: %s" %my_words
                            LOGGER.info(LOG)
                            negative = 1

                    if test_if_tweet_has_address(json_dump):
                        LOGGER.info("Maybe address in this tweet?")
                        negative = 1
                        
                    if "data" not in json.dumps(json_response):
                        LOGGER.info("No data in json!")
                        continue

                    if negative == 0:
                        tweet_id=json.dumps(json_response["data"]["id"])
                        tweet_id=tweet_id.strip('"')
                        tweet_user_id=json.dumps(json_response["data"]["author_id"])
                        tweet_user_id=tweet_user_id.strip('"')
                        username=json.dumps(json_response["includes"]["users"][0]["username"])
                        name=json.dumps(json_response["includes"]["users"][0]["name"])

                        bot = 0
                        if "BOT" in username.upper() or "BOT" in name.upper() or "ALERT" in name.upper() or number_of_percentages > 1:
                            LOGGER.info("************** Possible bot **********************")
                            LOG = "username: %s name: %s number_of_percentages: %s" % (username,name,number_of_percentages)
                            LOGGER.info(LOG)
                            LOGGER.debug(json_dump)
                            bot = 1

                        if tweet_user_id in MY_FOLLOWERS_LIST and tweet_user_id!=MOBILE_DONK_ID:
                            LOGGER.info("************** Already my follower **********************")
                            #sys.exit(0)
                        else:
                            followers,friends,joined = get_user_followers(headers,tweet_user_id)
                            followers = int(followers)
                            friends = int(friends)
                            #print("Followers: %s" %followers)
                            #print("Friends: %s" %friends)
                            add_to_author_list = 0

                            if followers == 99999 and friends == 99999:
                                LOGGER.info("We try top stop steaming...")
                                #SAVED_EPOCH_TIME = current_epoch + 900 #Just 15min break?
                                break
                            #Some let's try to catch the new users and remove bots
                            #if(followers < 50 and friends < 50 and friends > 0) and tweet_user_id not in AUTHOR_LIST:

                            #Let's try to take only new users so far..
                            new_user = 0
                            #if "2021" in joined and ("Mar" in joined or "Apr" in joined or "May" in joined):
                            #if "2021" in joined or "2020" in joined or "2019" in joined or "2018" in joined or "2017" in joined or "2016" in joined or "2015" in joined or "2014" in joined or "2013" in joined or "2012" in joined or "2011" in joined or "2010" in joined:
                            new_user = 1
                                #LOGGER.info("This is a twitter user from year 2010-2021. USER_ID: %s" % tweet_user_id)
                            #else:
                            #    new_user = 1

                            #if(followers < 500 and friends > 0) and tweet_user_id not in AUTHOR_LIST and new_user==1:
                            if followers < 10000 and (tweet_user_id not in AUTHOR_LIST or tweet_user_id==MOBILE_DONK_ID) and new_user==1 and bot==0:
                                if(like_tweet(tweet_id)) == 0:
                                    LOG = "User ID: %s" %tweet_user_id
                                    LOGGER.info(LOG)
                                    LOG = "Tweet ID: %s" %tweet_id
                                    LOGGER.info(LOG)
                                    LOGGER.info("We add this user to author list")
                                    add_to_author_list = 1
                                    AUTHOR_LIST.append(tweet_user_id)
                                    with open('likelist.txt', 'wb') as fp:
                                        pickle.dump(AUTHOR_LIST, fp)

                                    current_epoch=int(time.mktime(datetime.now().timetuple()))
                                    NBR_LIKED_24H_TWEETS.append(current_epoch)
                                    with open('nbr_liked.txt', 'wb') as fp:
                                        pickle.dump(NBR_LIKED_24H_TWEETS, fp)

                                    get_24h_likes(NBR_LIKED_24H_TWEETS,received_tweets)
                                else:
                                    LOGGER.info("We do not add this user to author list")
                            if tweet_user_id in AUTHOR_LIST and add_to_author_list == 0 and tweet_user_id!=MOBILE_DONK_ID:
                                LOGGER.info("Liked already this user...")
                    else:
                        LOGGER.info("Negative word found - skipped..")
                        LOGGER.debug(json_dump)
            LOGGER.info("End of for loop!!")
            #response.connection.close()
            pass
        except requests.exceptions.ChunkedEncodingError:
            LOGGER.error("************* ChunkedEncodingError")
            #print("************* ChunkedEncodingError")
            LOG = "Script started: %s" % BEGIN_TIME
            LOGGER.info(LOG)
            #print("Script started: %s" % BEGIN_TIME)
            LOGGER.info("We close connection and sleep 10 seconds and reconnect...")
            #print("We close connection and sleep 10 seconds and reconnect...")
            #response.connection.close()
            time.sleep(10)
            pass
        except requests.exceptions.RequestException as e:
            LOG = "Request exception `{}`, exiting".format(e)
            LOGGER.error(LOG)
            #print("Request exception `{}`, exiting".format(e))
            LOG = "Script started: %s" % BEGIN_TIME
            LOGGER.info(LOG)
            #print("Script started: %s" % BEGIN_TIME)
            LOGGER.info("We close connection and sleep 10 seconds and reconnect...")
            #print("We close connection and sleep 10 seconds and reconnect...")
            #response.connection.close()
            time.sleep(10)
            pass

LOGGER = setup_custom_logger('twitter')

def main():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    LOG = "Current Time =", current_time
    LOGGER.info(LOG)
    bearer_token = os.environ.get("BEARER_TOKEN")    
    headers = create_headers(bearer_token)
    rules = get_rules(headers, bearer_token)
    delete = delete_all_rules(headers, bearer_token, rules)


    #tweet = "I want more crypto. Be a good beta bitch and start sending Relieved face BTC wallet:1DRTAM4JEy7uLxfccJh7vq3Eom7dTV6PT7 ETH wallet:0xda44642b736fdbb24579f117caac2c4be5bee240XRP wallet:rBgnUKAEiFhCRLPoYNPPe3JUWayRjP6Aygfindom findomaus paypig ausfindom humanatm cuck cashslave"    
    #test_if_tweet_has_address(tweet)

    ##Run this periodic intervals to get followers....
    #get_followers_list_v11()
    #sys.exit(0)
    #get_rate_limits_v11()
    #print("Script started: %s" % BEGIN_TIME)

    #check_how_many_like_list_is_in_follower_list()
    #sys.exit(0)

    #with open('nbr_tweets.txt', 'wb') as fp:
    #    pickle.dump(0, fp)
                        
    with open('nbr_tweets.txt', 'rb') as fp:
        received_tweets = pickle.load(fp)

    #MONTHLY TWEET CAP USAGE Resets on August 8 at 00:00 UTC
    if int(datetime.today().strftime('%d')) == 8 and received_tweets > 50000:
        LOGGER.info("We reset the received tweets counter")
        received_tweets = 0
        with open('nbr_tweets.txt', 'wb') as fp:
            pickle.dump(received_tweets, fp)
    
    with open ('likelist.txt', 'rb') as fp:
        AUTHOR_LIST = pickle.load(fp)
        LOG = "AUTHOR_LIST len: %s" % len(AUTHOR_LIST)
        LOGGER.debug(LOG)

    with open('my_followers.txt', 'rb') as fp:
        MY_FOLLOWERS_LIST = pickle.load(fp)
        LOG = "MY_FOLLOWERS_LIST len: %s" % len(MY_FOLLOWERS_LIST)
        LOGGER.debug(LOG)

    with open('nbr_liked.txt', 'rb') as fp:
        NBR_LIKED_24H_TWEETS = pickle.load(fp)

    LOG = "24h like array size before remove: %s" %len(NBR_LIKED_24H_TWEETS)
    LOGGER.info(LOG)
    likes24h = 0
    removed_likes24h = 0
    my_ctr = 0
    current_epoch=int(time.mktime(datetime.now().timetuple()))
    debug_remove = 1
    list_len = range(len(NBR_LIKED_24H_TWEETS))
    for like in NBR_LIKED_24H_TWEETS[:]:  #Copy of NBR_LIKED_24H_TWEETS object
        my_ctr = my_ctr + 1
        if debug_remove == 1:
            LOG = "%s: %s: %s <> %s" %(my_ctr, current_epoch, like, (int(like)+86400))
            LOGGER.debug(LOG)
            ts1 = datetime.fromtimestamp(current_epoch).strftime('%Y-%m-%d %H:%M:%S')
            ts2 = datetime.fromtimestamp(like).strftime('%Y-%m-%d %H:%M:%S')
            ts3 = datetime.fromtimestamp((like+86400)).strftime('%Y-%m-%d %H:%M:%S')
            LOG = "%s: %s < %s" %(my_ctr, ts1, ts3)
            LOGGER.debug(LOG)
        
        if current_epoch < (like+86400):
            likes24h = likes24h + 1
        else:
            if debug_remove == 1:
                LOGGER.info("This should be removed")
            NBR_LIKED_24H_TWEETS.remove(like)
            removed_likes24h = removed_likes24h +1

    LOG = "Removed likes: %s. 24h like array size after remove: %s" %( removed_likes24h, len(NBR_LIKED_24H_TWEETS))
    LOGGER.info(LOG)
    LOG = "Likes during last 24 hours: %s" %likes24h
    LOGGER.info(LOG)

    NBR_LIKED_24H_TWEETS.sort()
    with open('nbr_liked.txt', 'wb') as fp:
        pickle.dump(NBR_LIKED_24H_TWEETS, fp)

    set = set_rules(headers, delete, bearer_token)
    get_stream(headers, set, bearer_token,AUTHOR_LIST,NBR_LIKED_24H_TWEETS,received_tweets,MY_FOLLOWERS_LIST)


if __name__ == "__main__":
    main()
