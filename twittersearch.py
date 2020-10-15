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
tweets_df['is_no_retweet'] = tweets_df['text'].apply(lambda x: x[:2]!='RT')

print('\n' + '------------------Dataframe Tweets final------------------' + '\n')
print(tweets_df)

# number of unique retweets
print('\n' + '------------------Tweets retweeted unicos------------------' + '\n')
print(tweets_df.loc[tweets_df['is_retweet']].text.unique())
print(tweets_df.loc[tweets_df['is_retweet']].text.unique().size)

# number of unique no retweets
print('\n' + '------------------Tweets no retweet unicos-----------------' + '\n')
print(tweets_df.loc[tweets_df['is_no_retweet']].text.unique())
print(tweets_df.loc[tweets_df['is_no_retweet']].text.unique().size)

# 10 most repeated tweets
print('\n' + '------------------10 most retweeted tweets------------------' + '\n')
print(tweets_df.groupby(['text']).size().reset_index(name='counts')\
  .sort_values('counts', ascending=False).head(10))

print('\n' + '------------------10 most retweeted tweets------------------' + '\n')
print(tweets_df.groupby(['text']).size().reset_index(name='counts')\
  .sort_values('counts', ascending=False).head(10))  

#print('ordered dataframe'+'\n')
#print(tweets_df)

print('\n' + '----------------tweets final sin duplicados----------------' + '\n')
#tweets_df_unique = tweets_df.drop_duplicates(subset=['text'])
tweets_df_unique = tweets_df.text.unique()
print(tweets_df_unique)
print(tweets_df_unique.size)

tweets_df_no_rt = tweets_df.loc[tweets_df['is_no_retweet']]
tweets_df_is_rt = tweets_df.loc[tweets_df['is_retweet']]

# --------------------------------------------------------------------------------
# Starting NLP process
# --------------------------------------------------------------------------------

# cleaning text data

from string import punctuation
from nltk import word_tokenize
from nltk.util import ngrams
from nltk.corpus import stopwords
from nltk import FreqDist

# Generación stoplist

additionalstopwords = ['https','proptech','amp']

stoplist = set(stopwords.words('english')) | \
           set(stopwords.words('spanish')) | \
           set(stopwords.words('french')) |  \
           set(punctuation) |                \
           set(additionalstopwords)

# Convierte a minúsculas todas las palabras

sentences = "".join(tweets_df_no_rt['text']).lower()
#print(sentences)

# Tokeniza extrayendo palabras a excluír

tokens = [token for token in word_tokenize(sentences) if token not in stoplist] # No stoplist
tokens = [token for token in tokens if token.isalpha()] # sólo caracteres alfabéticos

#print(tokens)

# Genera Bigrams

unigrams = ngrams(tokens, 1)
bigrams = ngrams(tokens, 2)

#for x in bigrams:
#  print(x)

print('\n' + '------------------Unigrams Frequency Distribution------------------' + '\n')
print(FreqDist(ngrams(tokens, 1)).most_common(25))

print('\n' + '------------------Bigrams Frequency Distribution-------------------' + '\n')
print(FreqDist(ngrams(tokens, 2)).most_common(25))

print('\n' + '------------------Trigrams Frequency Distribution------------------' + '\n')
print(FreqDist(ngrams(tokens, 3)).most_common(25))

#print(tweets_df.keys())
#print(tweets_df.loc[tweets_df['is_no_retweet']])
print('\n' + '------------------              Final            ------------------' + '\n')