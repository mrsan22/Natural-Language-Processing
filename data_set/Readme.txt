To save:

import pickle
f = open('my_classifier.pickle', 'wb')
pickle.dump(classifier, f)
f.close()
To load later:

import pickle
f = open('my_classifier.pickle')
classifier = pickle.load(f)
f.close()

TextBlob :
TextBlob is a Python (2 and 3) library for processing textual data. It provides a simple API for diving into common natural language processing (NLP) tasks such as part-of-speech tagging,
noun phrase extraction, sentiment analysis, classification, translation, and more.