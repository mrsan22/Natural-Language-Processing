# Natural-Language-Processing
Twitter_Sentiment_Analyzer

Designed a Twitter Sentiment Analyzer using NLTK, Elastisearch and Kibana. I used Naive Bayes Classifier as ML classifier for classifying the tweets as positive, negative and neutral. Initially, I trained the classifier with a large data set of 21k tweets and then streamed live tweets by using twitter  API (tweepy) about a topic and perfomed cleaning of tweets so as to make it understandable to Naive Bayes, which then can classify tweets as positive, negative and neutral. I   indexed the sentiments using Elasticsearch and used Kibana for drawing graphs depicting the sentiments over a period of time.
