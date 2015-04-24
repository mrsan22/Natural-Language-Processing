__author__ = 'sanjiv'

import re
from preprocess_tweet import process_tweet
import csv
import nltk
from nltk.classify.util import apply_features
import time
import pickle
import json
import pandas as pd
import matplotlib.pyplot as plt
from pyelasticsearch import ElasticSearch
#from es_indexer import es_indexer


# Some Rules
# Stop words - a, is, the, with etc. The full list of stop words can be found at Stop Word List.
# These words don't indicate any sentiment and can be removed.
# Punctuation - we can remove punctuation such as comma, single/double quote, question marks at the start and end of each
# word. E.g. beautiful!!!!!! replaced with beautiful
# Words must start with an alphabet - For simplicity sake, we can remove all those words which
# don't start with an alphabet. E.g. 15th, 5.34am

#look for two or more repetitive char and replace with single ch

#read stopwords from file and return it
start=time.clock()
def stop_word_list(stopword_file):
    stopWords = []
    stopWords.append('AT_USERNAME')
    stopWords.append('URL')

    fhandle = open(stopword_file)
    fread = fhandle.readline()

    while fread:
        word = fread.strip()
        stopWords.append(word)
        fread = fhandle.readline()
    fhandle.close()
    return stopWords
print "stop_word_list",'->',time.clock() - start

start1=time.clock()
def build_feature_vector(tweet):
    featureVector = []
    #split tweet into words
    result = []
    result = stop_word_list('stopwords.txt')
    words = tweet.split()
    for w in words:
        #replace two or more char with two occurrences
        #w=replace_rep_char(w)
        #strip punctuation
        w = w.strip('\'"?.,')
        #check if word start with alphabet
        val = re.search(r'^[a-zA-Z][a-zA-Z0-9]*$', w)
        #ignore if it's stop word
        #print result
        if w in result or val is None:
            continue
        else:
            featureVector.append(w.lower())
    return featureVector
print "build_feature_vector",'->',time.clock() - start1

start2=time.clock()
def getFeatureList(file):
    fl = []
    fread = open(file)
    for each in fread:
        fl.append(each.strip())
    return fl
print "get_feature_list",'->',time.clock() - start2
#Storing the feature vector in a list that can be used to train the classifier
featureList = getFeatureList('./data_set/full_feature_list.txt')
#Remove featureList duplicate
unique_featureList=list(set(featureList))

start3=time.clock()
#Extracting words in a proper format that are relevant to tweets
def extract_features(tweet):
    tweet_words = set(tweet)
    features = {}
    for word in unique_featureList:
        features['contains(%s)' % word] = (word in tweet_words)
    return features
print "extract_features",'->',time.clock() - start3

start4=time.clock()

def tweet_data():
    tweets_lst=[]
    fhand=open('./data_set/test_obama.txt')
    tweets_data=[]
    for line in fhand:
        try:
            tweet=json.loads(line)
            tweets_data.append(tweet)
        except:
            continue
    #print len(tweets_data) #:Number of tweets: 32620

    #Use pandas to simplify data manipulation:
    #Creating a data frame : Its a row-column data structure
    tweets=pd.DataFrame()

    tweets['text'] = map(lambda tweet:tweet['text'],tweets_data)
    #for each in tweets.index.tolist():
    for i in range(len(tweets)):
        tweets_lst.append(tweets['text'][i])
    return tweets_lst


def main():
    #Open the below file for writing
    #fhand = open('./data_set/full_feature_list.txt', 'w')
    #Below is the list of tuples tweet words, sentiment
    # tweets = []
    # #featureList=[]
    # input_tweets = csv.reader(open('./data_set/full_training_dataset _main.csv', 'rb'), delimiter=',')#, quotechar='|')
    # #initial_tweets=open('./data_set/train_data.csv', 'rU')
    # #input_tweets = csv.reader((line.replace('\0','') for line in initial_tweets), delimiter=",")
    # start6=time.clock()
    # print 'start-time','->',start6
    # for row in input_tweets:
    #     sentiment = row[0]
    #     tweet = row[1]
    #     #Callin process_tweet method to pre process the tweet
    #     processed_tweet = process_tweet(tweet)
    #     #Calling build_feature_list that returns the list of feature vector
    #     featureVector = build_feature_vector(processed_tweet)
    #     #featureList.append(featureVector)
    #     # for each in featureVector:
    #     #     fhand.write(each)
    #     #     fhand.write('\n')
    #     tweets.append((featureVector, sentiment))
    # print 'end-time','->',time.clock()-start6
    # #fhand.close()

    #Extract feature vector for all tweets. In below function the inputs are extract features function and all
    #tweets, the extract features function picks one tweet from list if tweets and create feature vector.
    # start7=time.clock()
    # print 'start-time-training-time','->',start7
    # training_set=apply_features(extract_features,tweets)
    # print type(training_set)
    # print 'end-time-training-time','->',time.clock()-start7
    #Train the Naive Bayes Classifier
    start8=time.clock()
    print 'start-time-NB','->',start8
    f=open('./data_set/naivebayes_trained_model.pickle')
    NBClassifier=pickle.load(f)
    print 'end-time-NB','->',time.clock()-start8
    #NBClassifier =  nltk.NaiveBayesClassifier.train(training_set)
    #f=open('./data_set/NBClassifier_trained_21k_tweets.pickle','wb')
    #pickle.dump(NBClassifier,f)
    #print 'end-time-NB','->',time.clock()-start8
    #Print most informative features about the classifier
    #print NBClassifier.show_most_informative_features(10)

    #Test the  classifier

    #ElasticSearch- Call the es_indexer file to create 'sentiment_analysis' index
    #es_indexer()
    es=ElasticSearch('http://localhost:9200/')
    i=0
    #testTweet = 'I will get internship happy!!!'
    for each in tweet_data():
        i+=1
        testTweet= each
        processedTestTweet=process_tweet(testTweet)
        sentiment=NBClassifier.classify(extract_features(build_feature_vector(processedTestTweet)))
        #print sentiment
    ############Indexing into Elasticsearch############
        es.index("sentiment_analysis","document",{
                     "text": testTweet,
                     "sentiment": sentiment
                         },id=i)
    print "Indexing completed."

    es.refresh(index="sentiment_analysis")
    print "Index refreshed."


    #print extract_features(tweets[0][0])
    f.close()
print "main",'->',time.clock() - start4

if __name__ == '__main__':
    main()
    tweet_data()

print "main-end",'->',time.clock() - start4

##def es_indexer():
##    es=ElasticSearch('http://localhost:9200/')
##    tweets=['dsdsd','dsdsds','dsdsdsdsds','ewewewewe']
##    i=0
##    for each in tweets:
##        i+=1
##        es.index("sentiment_analysis","document",{
##                 "text": each,
##                 "sentiment": 'positive'
##                     },id=i)
##    print "Indexing completed."
##
##    es.refresh(index="sentiment_analysis")
##    print "Index refreshed."
##
##    
    
    #Delete index 'sentiment_analysis' if it already exists
##    es.create_index(index='sentiment_analysis')
##    print "Deleted Index 'sentiment_analysis' if it already existed"
##
##    #Create index in elasticsearch and configure setting and mappings
##    print "Creating index sentiment_analysis ...."
##    es.create_index(index="sentiment_analysis",
##                        body={
##                            'settings': {
##                                'index': {
##                                    'store': {
##                                        'type': "default"
##                                    },
##                                    'number_of_shards': 1,
##                                    'number_of_replicas': 1
##                                },
##                                'analysis': {
##                                    'analyzer': {
##                                        'default_english': {
##                                            'type': 'english'
##                                        }
##                                    }
##                                }
##                            },
##                            "mappings": {
##                                "document": {
##                                    "properties": {
##                                        "text": {
##                                            "type": "string",
##                                            "store": True,
##                                            "index": "analyzed",
##                                            "term_vector": "with_positions_offsets_payloads",
##                                            "analyzer": "default_english"
##                                        },
##                                        "sentiment": {
##                                            "type": "string",
##                                            "store": True,
##                                            "index": "analyzed",
##                                            "analyzer": "default_english"
##                                        }
##                                    }
##                                }
##                            }
##                        })
##    print "Created index 'sentiment_analysis' with type 'document' and an analyzed field 'text'."

#es_indexer()
