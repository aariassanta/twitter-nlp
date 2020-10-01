import tweepy
from credentials import *   ## all my twitter API credentials are in this file, this should be in the same directory as is this script
import json
#from nltk.tokenize import word_tokenize
import pandas as pd
#from pandas.io.json import json_normalize
import csv
import json
 
#print(pd.__version__)

## set API connection

auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)                    
api = tweepy.API(auth, wait_on_rate_limit=True)    # set wait_on_rate_limit =True; as twitter may block you from querying if it finds you exceeding some limits

# Importa datos del archivo JSON de Tweets Stream 

tweets_json = pd.read_json ('./proptech/stream_proptech.json', orient='records', lines=True)
#print(json_normalize(tweets_json['user'])['screen_name'])

print('--------- tweets_json --------------/n')
print(tweets_json)

# Genera Nuevo Dataframe extrayendo campos útiles que están en diccionarios en columnas del DF

tweets_json2 = pd.DataFrame()
tweets_json2['user_name'] = pd.json_normalize(tweets_json['user'])['screen_name']
tweets_json2['location'] = pd.json_normalize(tweets_json['user'])['location']
tweets_json2['hashtags'] = pd.json_normalize(tweets_json['entities'])['hashtags']

# Agrega los diferentes Hashtags en cada tweet en una sola lista por tweet

res = []
for row in tweets_json2['hashtags']:
  tmp = []
  #print(row)
  for list in row:
    tmp.append(list['text'])
  res.append(tmp)
print(res)
tweets_json2['hashtags'] = res
print(len(res))

tweets_df = pd.concat([tweets_json, tweets_json2], axis=1)

#pd.set_option('display.max_colwidth', None)
print('--------- tweets_json2 --------------/n')
print(tweets_json2)
print(tweets_df)

# make a new column to highlight retweets
tweets_df['is_retweet'] = tweets_df['text'].apply(lambda x: x[:2]=='RT')
tweets_df['is_retweet'].sum()  # number of retweets

print(tweets_df)

# number of unique retweets
print(tweets_df.loc[tweets_df['is_retweet']].text.unique().size)

# 10 most repeated tweets
print(tweets_df.groupby(['text']).size().reset_index(name='counts')\
  .sort_values('counts', ascending=False).head(10))
#
#print('ordered dataframe'+'\n')
#print(tweets_df)

# Starting process

from sklearn.feature_extraction.text import TfidfVectorizer
from collections import Counter

#corpus = tweets_df['text']

# We can use the TfidfVectorizer to find ngrams for us
vect = TfidfVectorizer(ngram_range=(2,5), stop_words='english')

# Pulls all of trumps tweet text's into one giant string
summaries = "".join(tweets_df['text'])
ngrams_summaries = vect.build_analyzer()(summaries)

print(Counter(ngrams_summaries).most_common(20))

#cleaning text data
from string import punctuation
from nltk import word_tokenize
from nltk.util import ngrams
from nltk.corpus import stopwords

additionalstopwords = ['https']

stoplist = set(stopwords.words('english')) | \
           set(stopwords.words('spanish')) | \
           set(stopwords.words('french')) |  \
           set(punctuation) |                \
           set(additionalstopwords)

words = "".join(tweets_df['text']).lower()

#tokens = [token for token in word_tokenize("".join(tweets_df['text'])) if token not in stoplist] # No stoplist
tokens = [token for token in word_tokenize(words) if token not in stoplist] # No stoplist
tokens = [token for token in tokens if token.isalpha()] # sólo caracteres alfabéticos

print(tokens)
bigrams = ngrams(tokens, 2)

for x in bigrams:
  print(x)

print(stopwords.words('english'))