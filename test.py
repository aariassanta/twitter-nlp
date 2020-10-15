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

print(tweets_json['entities'])

with open('./proptech/stream_proptech.json') as f1: 
    reach1 = [] 
    reach2 = [] 
    for line in f1: 
      profile = json.loads(line)
      reach1.append(profile)
print(reach1)
