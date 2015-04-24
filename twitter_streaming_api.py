__author__ = 'sanjiv'


import tweepy
import sys

#variables that contains user credentials to access API : Authentication details
consumer_key = 'GrHbT3dDzFcn3ipCzCQILs12r'
consumer_secret = '4AmVh9oTJuSi7kYbhB8GUew2DfJKa6QgVjLsz3SzAt9r5cLQiV'
access_token = '222357703-yOBXfn0pZOrTCPdKSVsHGXHIlrPQJ5MymKC2X9Zb'
access_token_secret = 'tUVZOQ3cSNqVkoDBK0M6ERVlbtw7dzlg6piHSiYrgsLP1'

#This is a listener for hearing data
class StdOutListener(tweepy.StreamListener):

    # def __init__(self):
    #     super(StdOutListener, self).__init__()
    #     self.num_tweets = 0
    #
    # def on_status(self, status):
    #     collection=[]
    #     text = status.text
    #     created = status.created_at
    #     record = {'Text': text, 'Created At': created}
    #     self.num_tweets = self.num_tweets + 1
    #     if self.num_tweets < 5:
    #         collection.append(record)
    #         return True
    #     else:
    #         return False


    def on_data(self, data):

        #print data
        fhand=open('./data_set/tweet_collection.txt','a')
        fhand.write(data)
        fhand.close()
        return True


    def on_error(self,status_code):
        print 'Encountered Error with Status Code:', status_code

    def on_timeout(self):
        print "Timeout....."
        return True

    def get_tweets(self):
        fhand = open('./data_set/tweet_collection.txt','w')
        l=StdOutListener()
        #l.stopAt=StopAtNum
        #Enter consumer_key, consumer_secret to create a OAuth handler
        auth=tweepy.OAuthHandler(consumer_key,consumer_secret)
        #access_token, access_token_secret
        auth.set_access_token(access_token,access_token_secret)
        stream=tweepy.Stream(auth, l, timeout=120)
        stream.filter(track=[sys.argv[1]])



l=StdOutListener()
l.get_tweets()



