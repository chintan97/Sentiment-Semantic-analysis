# Before executing this file, fetch_tweets.py and change_sentiwords.py is executed.
# fetch_tweets.py was executed to fetch 2000 tweets.
# change_sentiwords.py was executed to format sentiwords.txt file.
# Why it was need to format is mentioned in change_sentiwords.py

import json
import re
import csv
import os

# Create output folder if not exists
if not os.path.exists('./output'):
    os.makedirs('./output')

# Fetch tweet data from tweets_data.json. Format of json is {"tweets": [list containing tweets text]}
with open("tweets_data.json", "r") as file:
    get_data = json.load(file)
    tweets_data = [tweet for tweet in get_data["tweets"]]   # Fetch tweets and store in list

# Fetch list of words and polarity from newly generated sentiwords_new.json file. Format of file is
# { "word": "<polarity of word in -1.0 to +1.0 where -1.0 is negative polarity and +1.0 is positive polarity>"
with open("sentiwords_new.json", "r") as file:
    word_dictionary = json.load(file)

# Create CSV file for output.
output_file = open("./output/output.csv", 'w', newline='')
output_file = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
output_file.writerow(['number', 'tweet (actual tweet text will defer. Open txt file instead)', 'polarity'])

# Create TXT file for output because of issue being faced in storing emoticons in CSV file.
sentiment_output = open("./output/sentiment_output.txt", "w", encoding="utf-8")

# Stopwords taken from words provided by nltk
stop_words = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"]

count = 1   # Just to count tweets
number_of_positives = 0   # It will store number of positive tweets
number_of_negatives = 0   # It will store number of negative tweets
number_of_neutral = 0   # It will store number of neutral tweets

for tweet in tweets_data:
    polarity = 0   # Initial polarity = 0
    save_tweet = tweet   # Just making a copy of tweet to write in output file
    tweet = tweet.strip()
    tweet = tweet.replace("\\u", '')   # It will remove emoticons
    tweet = tweet.replace("\n", ' ')  # Replace new line with space
    tweet = tweet.replace(".", ' ')  # Replace dot with space
    tweet = re.sub(r'[^A-Za-z0-9 ]+', '', tweet)   # Remove special characters
    tweet = tweet.lower()   # Convert sentence in lower. Word dictionary also contains lower case words
    tweet = tweet.split(" ")   # Split sentence into list of words
    for stop_word in stop_words:
        if stop_word in tweet:
            tweet.remove(stop_word)   # Remove stop words

    # Now for each words of dictionary, check if word is in the tweet. If it is in tweet, count polarity of
    # sentence. If it is >0 ,the tweet is positive; <0 ,the tweet is negative; else neutral.
    for word, polarity_value in word_dictionary.items():
        if word in tweet:
            polarity += float(polarity_value)

    if polarity > 0:
        number_of_positives += 1   # Increment positive tweet counter
        output_file.writerow([count, save_tweet.encode('utf-8'), 'positive'])
        sentiment_output.write("Tweet #" + str(count) + ":\n" + save_tweet + ": positive" + "\n\n")

    elif polarity < 0:
        number_of_negatives += 1   # Increment negative tweet counter
        output_file.writerow([count, save_tweet.encode('utf-8'), 'negative'])
        sentiment_output.write("Tweet #" + str(count) + ":\n" + save_tweet + ": negative" + "\n\n")

    else:
        number_of_neutral += 1   # Increment neutral tweet counter
        output_file.writerow([count, save_tweet.encode('utf-8'), 'neutral'])
        sentiment_output.write("Tweet #" + str(count) + ":\n" + save_tweet + ": neutral" + "\n\n")

    count += 1

print("\nNumber of positive tweets: " + str(number_of_positives))
print("\nNumber of negative tweets: " + str(number_of_negatives))
print("\nNumber of neutral tweets: " + str(number_of_neutral))