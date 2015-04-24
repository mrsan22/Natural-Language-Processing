__author__ = 'sanjiv'

##Python file to process tweets so that it becomes useful in determining the sentiments

# Lower Case - Convert the tweets to lower case.
# URLs - I don't intend to follow the short urls and determine the content of the site, so we can eliminate all of
# these ' \'' \ 'URLs via regular expression matching or replace with generic word URL.
# @username - we can eliminate "@username" via regex matching or replace it with generic word AT_USER.
# #hashtag - hash tags can give us some useful information, so it is useful to replace them with the exact same word
# # without the hash. E.g. #nike replaced with 'nike'.
# Punctuations and additional white spaces - remove punctuation at the start and ending of the tweets.
# E.g: ' the day is beautiful! ' replaced with 'the day is beautiful'. It is also helpful to replace multiple whitespaces
# with a single whitespace


import re

def process_tweet(tweet):

    #convert the tweet to lowercase
    tweet = tweet.lower()

    #replace all URLs starting with http or www word URL
    tweet= re.sub(r'((https?://[^\s]+)|(www\.[^\s]+))','URL',tweet)

    #replace the @username with generic word 'AT_USERNAME'
    tweet = re.sub(r'@[\w]+','AT_USERNAME',tweet)
    #replace tags with tag name

    match = re.search(r'#([\w]+)', tweet)
    if match:
        tweet = re.sub(r'#([\w]+)', match.group(1), tweet)
    #if multiple line space at starting,remove white space
    tweet = re.sub('^[\s]+',"",tweet)

    tweet = re.sub(r'[\W]+$',"",tweet)
    return tweet

# fhandle = open('tweet.txt')
# fread = fhandle.readline()
# #fread.strip('\n')
# while fread:
#     tweet_simple = process_tweet(fread)
#     #print tweet_simple
#     fread = fhandle.readline()
#
# fhandle.close()