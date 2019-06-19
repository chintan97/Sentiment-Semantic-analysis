# Some part of the code is taken from my assignment 2 of CSCI 5408 file search.py

import tweepy
import json

auth = tweepy.OAuthHandler("", "")
auth.set_access_token("",
                      "")

api = tweepy.API(auth)

max_count = 2000   # To limit tweet fetching
per_query_count = 100   # To fetch 100 tweets per query
tweet_count = 1   # To store count of tweets fetched

save_tweets = []   # To store tweets text

# Initially set max_id to max. It will be used in getting the tweets
max_id = 9999999999999999999

# We will run a loop till 2000 tweets are extracted. More than 2000 tweets may be fetched because the
# the counter is among top of all loops. Thus, if it satisfies tweet_count loop, it will fetch 100 tweets and store
# if conditions are satisfied.
# In each loop, 100 tweets are fetched and max_id will be used to fetch old 100 tweets
while tweet_count < max_count:
    id_list = []   # To store ids of tweet. Using minimum value, we can get older bunch of 100 tweets
    results = api.search(q='canada', count=per_query_count, max_id=max_id, tweet_mode='extended')
    for tweet in results:
        try:
            if (hasattr(tweet, 'retweeted_status')):   # Ignoring retweeted tweets to avoid repetition
                pass
            elif tweet.lang == 'en':   # fetch only tweets with english language
                save_tweets.append(tweet.full_text)   # full_text will fetch whole tweet with max 240 characters which is character limit per tweet specified by twitter
                id_list.append(tweet.id)
                tweet_count += 1
            else:
                pass
        except:
            pass
    max_id = min(id_list)   # This values will passed in tweet fetching. Thus, query will fetch 100 older tweets

dict = {"tweets": save_tweets}

# Store fetched tweets in tweets_data.json. Format will be {"tweets": [list of tweets]}
with open("tweets_data.json", "w") as file:
    json.dump(dict, file)