__author__ = 'sanjiv'

import re
from preprocess_tweet import process_tweet
import csv
import nltk
from nltk.classify.util import apply_features
import pickle
import json
import pandas as pd
from pyelasticsearch import ElasticSearch
from es_indexer import es_indexer


# Some Rules
# Stop words - a, is, the, with etc. The full list of stop words can be found at Stop Word List.
# These words don't indicate any sentiment and can be removed.
# Punctuation - we can remove punctuation such as comma, single/double quote, question marks at the start and end of each
# word. E.g. beautiful!!!!!! replaced with beautiful
# Words must start with an alphabet - For simplicity sake, we can remove all those words which
# don't start with an alphabet. E.g. 15th, 5.34am


#read stopwords from file and return it
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


def getFeatureList(file):
    fl = []
    fread = open(file)
    for each in fread:
        fl.append(each.strip())
    return fl

#Storing the feature vector in a list that can be used to train the classifier
featureList = getFeatureList('./data_set/full_feature_list.txt')

#Remove featureList duplicate
unique_featureList=list(set(featureList))


#Extracting words in a proper format that are relevant to tweets
def extract_features(tweet):
    tweet_words = set(tweet)
    features = {}
    for word in unique_featureList:
        features['contains(%s)' % word] = (word in tweet_words)
    return features




def tweet_data():
    tweets_lst=[]
    fhand=open('./data_set/netneutrality.txt')
    tweets_data=[]
    for line in fhand:
        try:
            tweet=json.loads(line)
            tweets_data.append(tweet)
        except:
            continue
    print" Analyzing %d tweets" %len(tweets_data)
    
    #Use pandas to simplify data manipulation:
    #Creating a data frame : Its a row-column data structure
    tweets=pd.DataFrame()

    tweets["text"] = map(lambda tweet:tweet["text"],tweets_data)
    for i in range(len(tweets)):
        tweets_lst.append(tweets['text'][i])
    fhand.close()
    return tweets_lst


def main():
    #Train the Naive Bayes Classifier
    f=open('./data_set/naivebayes_trained_model.pickle')
    NBClassifier=pickle.load(f)

    #ElasticSearch- Call the es_indexer file to create 'sentiment_analysis' index and store
    #the contents of the tweet file in that Index
    
    es=ElasticSearch('http://localhost:9200/')
    es_indexer()
    ############Indexing into Elasticsearch############
    i=0
    for each in tweet_data():
        i+=1
        testTweet= each
        processedTestTweet=process_tweet(testTweet)
        sentiment=NBClassifier.classify(extract_features(build_feature_vector(processedTestTweet)))
    
        
        es.index("sentiment_analysis","document",{
                     "text": testTweet,
                     "sentiment": sentiment
                         },id=i)
    print "Indexing completed."

    es.refresh(index="sentiment_analysis")
    print "Index refreshed."

    f.close()

if __name__ == '__main__':
    main()
