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

NEGATIVE_WORDS = ["pumped", "PUMPED", "PUMPING", "pumping", "Giving", "winners", "group", "follows", "follow", "Join"]
AUTHOR_LIST = []
MY_FOLLOWERS_LIST = []
START_TIME_LIMIT = time.time() - 900
ERRORS = 0
VERSION = 2
SAVED_EPOCH_TIME = 0
BEGIN_TIME = datetime. now()

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
    #print(json.dumps(response.json()))
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
    #print(json.dumps(response.json()))


def set_rules(headers, delete, bearer_token):
    # You can adjust the rules if needed
    sample_rules = [
        {"value": "lang:en (SHIB OR safemoon OR xrp OR AKITA OR FEG OR HOGE OR ERC20 OR DOGE OR pitbullish) -@safemoon_art -ECLIPSETOKEN -SAFEMARS -GIVEAWAY -safetesla -teslasafe -pump -join -pumping -pumped -winner -giveaway -Giving -address -follow -help -wallet -is:retweet -has:links", "tag": "shib OR pitbullish OR xrp OR safemoon OR feg OR HOGE OR ERC20 OR DOGE"},
        #{"value": "lang:en (cryptocurrency OR altseason OR BTC) -@safemoon_art -ECLIPSETOKEN -SAFEMARS -GIVEAWAY -safetesla -teslasafe -pump -join -pumping -pumped -winner -giveaway -Giving -address -follow -help -is:retweet -has:links", "tag": "cryptocurrency OR altseason"},
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
    #print(json.dumps(response.json()))


def get_24h_likes(NBR_LIKED_24H_TWEETS,received_tweets):
    global SAVED_EPOCH_TIME
    likes24h = 0    
    current_epoch=int(time.mktime(datetime.now().timetuple()))
    for like in NBR_LIKED_24H_TWEETS:
        if current_epoch < (like+86400):
            likes24h = likes24h + 1

    LOG = "Likes during last 24 hours: %s received_tweets: %s" %(likes24h,received_tweets)
    LOGGER.info(LOG)
    #print("Likes during last 24 hours: %s received_tweets: %s" %(likes24h,received_tweets))

    if(likes24h > 990 and SAVED_EPOCH_TIME < current_epoch):
        LOGGER.info("We should put breaks on...")
        #print("We should put breaks on...")
        LOG = "Script started: %s" % BEGIN_TIME
        LOGGER.info(LOG)
        #print("Script started: %s" % BEGIN_TIME)
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
        #print(
        #    "There may have been an issue with the consumer_key or consumer_secret you entered."
        #)
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
    url = "https://api.twitter.com/1.1/followers/ids.json?%s" %MY_TWITTER_ID
     
    response = oauth.get(url)
    #json_response = response.json()
    #print(json.dumps(json_response, indent=4, sort_keys=True))
        
    for response_line in response.iter_lines():
        if response_line:
            json_response = json.loads(response_line)
            json_dump = (json.dumps(json_response, indent=4, sort_keys=True))
            followers=json.dumps(json_response["ids"])
            #print(json_dump)
            LOGGER.info(followers)
            #print(followers)

    followers=followers.strip('[')
    followers=followers.strip(']')
    MY_FOLLOWERS_LIST = followers.split(",")
    LOGGER.info(MY_FOLLOWERS_LIST)
    #print(MY_FOLLOWERS_LIST)

    with open('my_followers.txt', 'wb') as fp:
        pickle.dump(MY_FOLLOWERS_LIST, fp)    

    
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
        #print(
        #    "There may have been an issue with the consumer_key or consumer_secret you entered."
        #)
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
    #print(json.dumps(json_response, indent=4, sort_keys=True))
        

    
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
        #print("We return due to limit %s < %s" % (ts1,ts2))
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
        #print(
        #    "There may have been an issue with the consumer_key or consumer_secret you entered."
        #)
    #resource_owner_key = fetch_response.get("oauth_token")
    #resource_owner_secret = fetch_response.get("oauth_token_selfecret")
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
    url = "https://api.twitter.com/1.1/favorites/create.json?id=%s" %int(tweet_id)
    
    if VERSION == 2:
        #print("We use v2")
        VERSION = 2
        response = oauth.post("https://api.twitter.com/2/users/{}/likes".format(MY_TWITTER_ID), json=payload)
    else:
        LOGGER.info("We use v1")
        #print("We use v1")
        VERSION = 1
        response = oauth.post(url, json=payload)

    if response.status_code != 200:
        LOG = "Like request returned an error: {} {}".format(response.status_code, response.text)
        LOGGER.info(LOG)
        #print("Like request returned an error: {} {}".format(response.status_code, response.text))
        skip_pause = 0
        if "This tweet cannot be found" in response.text:
            LOGGER.info("This tweet cannot be found...")
            #print("This tweet cannot be found...")
            skip_pause = 1
        if "Rate limit" in response.text:
            LOGGER.info("Rate limit...")
            #print("Rate limit...")
        if "Too Many Requests" in response.text:
            LOGGER.info("Too Many Requests...")
            #print("Too Many Requests...")
        if "Internal Server Error" in response.text:
                LOGGER.info("Internal Server Error...")
                #print("Internal Server Error...")
                sys.exit(0)

        LOGGER.info(response.headers)
        #print(response.headers)

        if skip_pause == 0:
            reset_epoch_time=response.headers['x-rate-limit-reset']
            ts = datetime.fromtimestamp(int(reset_epoch_time)).strftime('%Y-%m-%d %H:%M:%S')
            LOG = "Current rate limit will reset at %s" %ts
            LOGGER.info(LOG)
            #print("Current rate limit will reset at %s" %ts)
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
            #print("Current Time =", current_time)
            START_TIME_LIMIT = time.time()
            ERRORS = 0
        return 1
    else:
        ERRORS = 0
        LOG = "Response code: {}".format(response.status_code)
        LOGGER.info(LOG)
        #print("Response code: {}".format(response.status_code))

        if "x-rate-limit-remaining" not in response.headers:
            LOGGER.info("no x-rate-limit-remaining in response")
            #print("no x-rate-limit-remaining in response")
            return 1
                    
        x_rate_limit_remaining = response.headers['x-rate-limit-remaining']
        LOG = "like_tweet - x_rate_limit_remaining: %s" % x_rate_limit_remaining
        LOGGER.info(LOG)        
        #print("like_tweet - x_rate_limit_remaining: %s" % x_rate_limit_remaining)

        if int(x_rate_limit_remaining) < 5:
            #print("Let's slow down a bit")
            LOGGER.info("Let's slow down a bit")
            LOG = "Script started: %s" % BEGIN_TIME
            LOGGER.info(LOG)
            #print("Script started: %s" % BEGIN_TIME)
            current_epoch=time.mktime(datetime.now().timetuple())
            SAVED_EPOCH_TIME = current_epoch + 120 #Just 2 min break
            
        # Saving the response as JSON
        json_response = response.json()
        #print(json.dumps(json_response, indent=4, sort_keys=True))

    return 0


def get_user_followers(headers,userid):
    global START_TIME_LIMIT
    global SAVED_EPOCH_TIME
    followers = "99999"
    friends = "99999"
    joined = "Tue Apr 06 11:16:49 +0000 2008" 
    current_epoch=time.mktime(datetime.now().timetuple())
    
    if  int(current_epoch) < int(SAVED_EPOCH_TIME):
        ts1 = datetime.fromtimestamp(int(current_epoch)).strftime('%Y-%m-%d %H:%M:%S')
        ts2 = datetime.fromtimestamp(int(SAVED_EPOCH_TIME)).strftime('%Y-%m-%d %H:%M:%S')
        LOG = "We return due to limit %s < %s" % (ts1,ts2)
        LOGGER.info(LOG)
        #print("We return due to limit %s < %s" % (ts1,ts2))
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
        #print(
        #    "There may have been an issue with the consumer_key or consumer_secret you entered."
        #)
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
        #print("Followers get returned error (HTTP {}): {}".format(response.status_code, response.text))

        LOGGER.info(response.headers)
        #print(response.headers)
        reset_epoch_time=response.headers['x-rate-limit-reset']
        ts = datetime.fromtimestamp(int(reset_epoch_time)).strftime('%Y-%m-%d %H:%M:%S')
        LOG = "Current rate limit will reset at %s" %ts
        LOGGER.info(LOG)
        #print("Current rate limit will reset at %s" %ts)
        SAVED_EPOCH_TIME = reset_epoch_time
        return followers, friends, joined


    if "x-rate-limit-remaining" not in response.headers:
        LOGGER.info("no x-rate-limit-remaining is header")
        #print("no x-rate-limit-remaining is header")
        return followers, friends, joined
    
    x_rate_limit_remaining = response.headers['x-rate-limit-remaining']
    if int(x_rate_limit_remaining) < 100:
        LOG = "get_user_followers - x_rate_limit_remaining: %s" % x_rate_limit_remaining
        LOGGER.info(LOG)
        #print("get_user_followers - x_rate_limit_remaining: %s" % x_rate_limit_remaining)
    
    if int(x_rate_limit_remaining) < 5:
        LOGGER.info("Let's slow down a bit")
        #print("Let's slow down a bit")
        LOG = "Script started: %s" % BEGIN_TIME
        LOGGER.info(LOG)        
        #print("Script started: %s" % BEGIN_TIME)
        current_epoch=time.mktime(datetime.now().timetuple())
        SAVED_EPOCH_TIME = current_epoch + 60 #Just 1 min break

    for response_line in response.iter_lines():
        if response_line:
            json_response = json.loads(response_line)
            if "data" not in json.dumps(json_response):
                LOGGER.info("No data in json!")
                #print("No data in json!")
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

def get_stream(headers, set, bearer_token, AUTHOR_LIST, NBR_LIKED_24H_TWEETS, received_tweets):
    global SAVED_EPOCH_TIME
    at_the_begin = 1
    while True:
        if at_the_begin == 1:
            at_the_begin = 0
            my_followers_at_start,friends,joined = get_user_followers(headers,MY_TWITTER_ID)
            LOG = "My followers count at the begin: %s" %my_followers_at_start
            LOGGER.info(LOG)
            #print("My followers count at the begin: %s" %my_followers_at_start)
            received_tweets_start = received_tweets

        if received_tweets > received_tweets_start + 1000:
            my_followers_now,friends,joined = get_user_followers(headers,MY_TWITTER_ID)
            received_tweets_start = received_tweets
            if my_followers_now <= my_followers_at_start:
                LOG = "My followers count at the begin: %s now: %s" % (my_followers_at_start, my_followers_now)
                LOGGER.info(LOG)
                #print("My followers count at the begin: %s now: %s" % (my_followers_at_start, my_followers_now))
                current_epoch=time.mktime(datetime.now().timetuple())
                LOGGER.info("No new followers so we should wait over 1 hour now *****************************************************************")
                #print("No new followers so we should wait over 1 hour now *****************************************************************")
                SAVED_EPOCH_TIME = current_epoch + 3600
            my_followers_at_start = my_followers_now
        
        likes24h = get_24h_likes(NBR_LIKED_24H_TWEETS,received_tweets)
        current_epoch=time.mktime(datetime.now().timetuple())
        if  int(current_epoch) < int(SAVED_EPOCH_TIME):
            ts1 = datetime.fromtimestamp(int(current_epoch)).strftime('%Y-%m-%d %H:%M:%S')
            ts2 = datetime.fromtimestamp(int(SAVED_EPOCH_TIME)).strftime('%Y-%m-%d %H:%M:%S')
            LOG = "We do not reconnect yet %s < %s" % (ts1,ts2)
            LOGGER.info(LOG)
            #print("We do not reconnect yet %s < %s" % (ts1,ts2))
            time.sleep(60)
            continue
        if likes24h > 990:
            LOG = "We do not reconnect yet due to likes: %s" % likes24h
            LOGGER.info(LOG)
            #print("We do not reconnect yet due to likes: %s" % likes24h)
            time.sleep(60)
            continue
        try:
            #print("We send the http get...")
            LOGGER.info("We send the http get...")
            response = requests.get(
                "https://api.twitter.com/2/tweets/search/stream?expansions=author_id", headers=headers, stream=True,
            )
            LOG = "HTTP GET stream response code: %s" %response.status_code
            LOGGER.info(LOG)
            #print("HTTP GET stream response code: %s" %response.status_code)
            if response.status_code != 200:
                LOG = "resp: %s %s" % (response.status_code, response.text)
                LOGGER.info(LOG)
                #print("resp: %s %s" % (response.status_code, response.text))
                if "This stream is currently at the maximum allowed connection limit" in response.text:
                    LOGGER.info("We sleep 60 seconds and reconnect...")
                    #print("We sleep 60 seconds and reconnect...")
                    response.connection.close()
                    time.sleep(60)
                    continue
                else:
                    LOGGER.info("We make the exit....")
                    #print("We make the exit....")
                    sys.exit(0)

            for response_line in response.iter_lines():
                if response_line:
                    received_tweets = received_tweets + 1
                    with open('nbr_tweets.txt', 'wb') as fp:
                        pickle.dump(received_tweets, fp)

                    if int(received_tweets % 10 == 0):
                        LOG = "received_tweets: %s" %received_tweets
                        LOGGER.info(LOG)
                        #print("received_tweets: %s" %received_tweets)
                    json_response = json.loads(response_line)
                    json_dump = (json.dumps(json_response, indent=4, sort_keys=True))
                    #print(json_dump)
                    #print(len(json.dumps(json_response["data"]["text"])))
                    negative = 0
                    for my_words in NEGATIVE_WORDS:
                        if my_words in json_dump:
                            #print(my_words)
                            #print(json_dump)
                            negative = 1

                    #random_nbr = random.randrange(4, 6)
                    #print(random_nbr)
                    #if negative == 0 and random_nbr==5:

                    if "data" not in json.dumps(json_response):
                        LOGGER.info("No data in json!")
                        #print("No data in json!")
                        continue

                    if negative == 0:
                        tweet_id=json.dumps(json_response["data"]["id"])
                        tweet_id=tweet_id.strip('"')
                        tweet_user_id=json.dumps(json_response["data"]["author_id"])
                        tweet_user_id=tweet_user_id.strip('"')
                        #print("User ID: %s" %tweet_user_id)
                        #print("Tweet ID: %s" %tweet_id)

                        if tweet_user_id in MY_FOLLOWERS_LIST:
                            LOGGER.info("************** Already my follower **********************")
                            #print("************** Already my follower **********************")
                            #sys.exit(0)
                        else:
                            #print(json_dump)
                            followers,friends,joined = get_user_followers(headers,tweet_user_id)
                            followers = int(followers)
                            friends = int(friends)
                            #print("Followers: %s" %followers)
                            #print("Friends: %s" %friends)
                            add_to_author_list = 0

                            if followers == 99999 and friends == 99999:
                                LOGGER.info("We try top stop steaming...")
                                #print("We try top stop steaming...")
                                SAVED_EPOCH_TIME = current_epoch + 900 #Just 15min break?
                                break
                            #Some let's try to catch the new users and remove bots
                            #if(followers < 50 and friends < 50 and friends > 0) and tweet_user_id not in AUTHOR_LIST:

                            #Let's try to take only new users so far..
                            new_user = 0
                            #if "2021" in joined and ("Mar" in joined or "Apr" in joined or "May" in joined):
                            if "2021" in joined:
                                new_user = 1
                                LOGGER.info("This is a new twitter users from year 2021")
                            #else:
                            #    new_user = 1

                            #if(followers < 500 and friends > 0) and tweet_user_id not in AUTHOR_LIST and new_user==1:
                            if followers < 5000 and tweet_user_id not in AUTHOR_LIST and new_user==1:
                                if(like_tweet(tweet_id)) == 0:
                                    LOG = "User ID: %s" %tweet_user_id
                                    LOGGER.info(LOG)
                                    #print("User ID: %s" %tweet_user_id)
                                    LOG = "Tweet ID: %s" %tweet_id
                                    LOGGER.info(LOG)
                                    #print("Tweet ID: %s" %tweet_id)
                                    LOGGER.info("We add this user to author list")
                                    #print("We add this user to author list")
                                    add_to_author_list = 1
                                    AUTHOR_LIST.append(tweet_user_id)
                                    #print(AUTHOR_LIST)
                                    with open('likelist.txt', 'wb') as fp:
                                        pickle.dump(AUTHOR_LIST, fp)

                                    current_epoch=int(time.mktime(datetime.now().timetuple()))
                                    NBR_LIKED_24H_TWEETS.append(current_epoch)
                                    with open('nbr_liked.txt', 'wb') as fp:
                                        pickle.dump(NBR_LIKED_24H_TWEETS, fp)

                                    get_24h_likes(NBR_LIKED_24H_TWEETS,received_tweets)
                                else:
                                    LOGGER.info("We do not add this user to author list")
                                    #print("We do not add this user to author list")
                            if tweet_user_id in AUTHOR_LIST and add_to_author_list == 0:
                                LOGGER.info("Liked already this user...")
                                #print("Liked already this user...")

            #print("End of for loop!!")
            LOGGER.info("End of for loop!!")
            response.connection.close()
            pass
        except requests.exceptions.ChunkedEncodingError:
            LOGGER.error("************* ChunkedEncodingError")
            #print("************* ChunkedEncodingError")
            LOG = "Script started: %s" % BEGIN_TIME
            LOGGER.info(LOG)
            #print("Script started: %s" % BEGIN_TIME)
            LOGGER.info("We close connection and sleep 10 seconds and reconnect...")
            #print("We close connection and sleep 10 seconds and reconnect...")
            response.connection.close()
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
            response.connection.close()
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

    #Run this periodic intervals to get followers....
    #get_followers_list_v11()
    
    #get_rate_limits_v11()
    #print("Script started: %s" % BEGIN_TIME)
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
        #print("AUTHOR_LIST len: %s" % len(AUTHOR_LIST))

    with open('my_followers.txt', 'rb') as fp:
        MY_FOLLOWERS_LIST = pickle.load(fp)
        LOG = "MY_FOLLOWERS_LIST len: %s" % len(MY_FOLLOWERS_LIST)
        LOGGER.debug(LOG)
        #print("MY_FOLLOWERS_LIST len: %s" % len(MY_FOLLOWERS_LIST))

    with open('nbr_liked.txt', 'rb') as fp:
        NBR_LIKED_24H_TWEETS = pickle.load(fp)
        #print("NBR_LIKED_24H_TWEETS len: %s" % len(NBR_LIKED_24H_TWEETS))

    LOG = "24h like array size before remove: %s" %len(NBR_LIKED_24H_TWEETS)
    LOGGER.info(LOG)
    #print("24h like array size before remove: %s" %len(NBR_LIKED_24H_TWEETS))
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
            #print("%s: %s: %s <> %s" %(my_ctr, current_epoch, like, (int(like)+86400)))
            ts1 = datetime.fromtimestamp(current_epoch).strftime('%Y-%m-%d %H:%M:%S')
            ts2 = datetime.fromtimestamp(like).strftime('%Y-%m-%d %H:%M:%S')
            ts3 = datetime.fromtimestamp((like+86400)).strftime('%Y-%m-%d %H:%M:%S')
            LOG = "%s: %s < %s" %(my_ctr, ts1, ts3)
            LOGGER.debug(LOG)
            #print("%s: %s < %s" %(my_ctr, ts1, ts3))
        
        if current_epoch < (like+86400):
            likes24h = likes24h + 1
        else:
            if debug_remove == 1:
                LOGGER.info("This should be removed")
                #print("This should be removed")
            NBR_LIKED_24H_TWEETS.remove(like)
            removed_likes24h = removed_likes24h +1

    LOG = "Removed likes: %s. 24h like array size after remove: %s" %( removed_likes24h, len(NBR_LIKED_24H_TWEETS))
    LOGGER.info(LOG)
    #print("Removed likes: %s. 24h like array size after remove: %s" %( removed_likes24h, len(NBR_LIKED_24H_TWEETS)))
    LOG = "Likes during last 24 hours: %s" %likes24h
    LOGGER.info(LOG)
    #print("Likes during last 24 hours: %s" %likes24h)

    NBR_LIKED_24H_TWEETS.sort()
    with open('nbr_liked.txt', 'wb') as fp:
        pickle.dump(NBR_LIKED_24H_TWEETS, fp)

    set = set_rules(headers, delete, bearer_token)
    get_stream(headers, set, bearer_token,AUTHOR_LIST,NBR_LIKED_24H_TWEETS,received_tweets)


if __name__ == "__main__":
    main()
