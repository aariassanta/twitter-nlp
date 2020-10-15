# 

import sys 
from collections import Counter 
import json 
from stop_words import get_stop_words

additional_stop_words =['-','&amp;']
stop_words = get_stop_words('english') + get_stop_words('spanish') + additional_stop_words
 
def get_screen_name(tweet): 
  user = tweet.get('user', {})  
  name = user.get('screen_name', []) 
  return name 
 
def get_mentioned_name(tweet): 
  entities = tweet.get('entities', {}) 
  mentions = entities.get('user_mentions', []) 
  return [tag['screen_name'].lower() for tag in mentions] 

def get_hashtags(tweet): 
  entities = tweet.get('entities', {}) 
  hashtags = entities.get('hashtags', []) 
  return [tag['text'].lower() for tag in hashtags] 

if __name__ == '__main__': 
    fname = sys.argv[1] 

# Get most active users from list of tweets 

    with open(fname, 'r') as f: 
        name = Counter() 
        for line in f: 
            tweet = json.loads(line) 
            name_in_tweet = get_screen_name(tweet) 
            #print(name_in_tweet)
            name.update([name_in_tweet]) 

    print('\n' + '------------ 20 most common users' + '\n')
    #print(name)
    for tag, count in name.most_common(20): 
        print("{}: {}".format(tag, count)) 

    print('\n')

# Get most retweeted users from list of tweets

    with open(fname, 'r') as f: 
        name = Counter() 
        #name = {}
        for line in f: 
            tweet = json.loads(line) 
            #print(name_in_tweet)
            if tweet['text'][:2] == 'RT':
                name.update([tweet['text'][4:].split(':')[0]])

    print('\n' + '------------ 20 most retweeted users' + '\n')
    #print(name)
    for tag, count in name.most_common(20): 
      print("{}: {}".format(tag, count)) 

    print('\n')

# Get most retweeted tweets

    with open(fname, 'r') as f: 
        name = Counter() 
        #name = {}
        for line in f: 
            tweet = json.loads(line) 
            #print(name_in_tweet)
            if tweet['text'][:2] == 'RT':
                name.update([tweet['text']])

    print('\n' + '------------ 20 most retweeted users' + '\n')
    #print(name)
    for tag, count in name.most_common(20): 
      print("{}: {}".format(tag, count)) 

    print('\n')

# Get most mentioned users 

    with open(fname, 'r') as f: 
        name = Counter() 
        for line in f: 
            tweet = json.loads(line) 
            name_in_tweet = get_mentioned_name(tweet)
            name.update(name_in_tweet) 

    print('\n' + '------------ 20 most mentioned users' + '\n')
    #print(name)
    for tag, count in name.most_common(20): 
        print("{}: {}".format(tag, count)) 

    print('\n')

    with open(fname, 'r') as f: 
        hashtags = Counter() 
        for line in f: 
            tweet = json.loads(line) 
            hashtags_in_tweet = get_hashtags(tweet) 
            hashtags.update(hashtags_in_tweet) 

    print('\n' + '------------ 20 most common hashtags' + '\n')
    for tag, count in hashtags.most_common(20): 
        print("{}: {}".format(tag, count)) 

    print('\n')

    # Get most repeated words from list of tweets

    with open(fname, 'r') as f: 
        name = Counter() 
        #name = {}
        for line in f: 
            tweet = json.loads(line) 
            #print(name_in_tweet)
            [ name.update([word]) for word in tweet['text'][4:].lower().split() if not word in stop_words ]
            #if tweet['text'][:2] == 'RT':
            #    name.update([tweet['text'][4:].split(':')[0]])

    print('\n' + '------------ 20 most repeated words' + '\n')
    for tag, count in name.most_common(20): 
        print("{}: {}".format(tag, count)) 

    print('\n')

    #filtered_sentence = [w for w in word_tokens if not w in stop_words] 