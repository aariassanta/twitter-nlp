# 

import sys 
from collections import Counter 
import json 
from stop_words import get_stop_words
import pandas as pd

additional_stop_words =['-','&amp;']
stop_words = get_stop_words('english') + get_stop_words('spanish') + additional_stop_words
 
def get_screen_name(tweet): 
  user = tweet.get('user', {})  
  name = user.get('screen_name', []) 
  return name 

def get_user_location(tweet): 
  user = tweet.get('user', {})  
  name = user.get('location', []) 
  return name 
 
def get_mentioned_name(tweet): 
  entities = tweet.get('entities', {}) 
  mentions = entities.get('user_mentions', []) 
  return [tag['screen_name'].lower() for tag in mentions] 

def get_hashtags(tweet): 
  entities = tweet.get('entities', {}) 
  hashtags = entities.get('hashtags', []) 
  return [tag['text'].lower() for tag in hashtags] 

def get_urls(tweet): 
  entities = tweet.get('entities', {}) 
  urls = entities.get('urls', []) 
  return [tag['expanded_url'] for tag in urls] 

if __name__ == '__main__': 
    fname = sys.argv[1] 

# Get most active users from list of tweets 

    with open(fname, 'r') as f: 
        name = Counter() 
        for line in f: 
            tweet = json.loads(line) 
            name_in_tweet = get_screen_name(tweet) 
            name.update([name_in_tweet]) 

    print('\n' + '------------ 20 most common users' + '\n')
    #print(name)
    for tag, count in name.most_common(20): 
        print("{}: {}".format(tag, count)) 

    # Save to file

    df = pd.DataFrame(name.items(), columns=['User','Freq'])
    df.to_csv("./csv/Users.csv", sep=',',index=False)

    print('\n')

# Get most retweeted users from list of tweets

    with open(fname, 'r') as f: 
        name = Counter() 
        #name = {}
        for line in f: 
            tweet = json.loads(line) 
            if tweet['text'][:2] == 'RT':
                name.update([tweet['text'][4:].split(':')[0]])

    print('\n' + '------------ 20 most retweeted users' + '\n')
    #print(name)
    for tag, count in name.most_common(20): 
      print("{}: {}".format(tag, count)) 

    # Save to file

    df = pd.DataFrame(name.items(), columns=['User','Freq'])
    df.to_csv("./csv/Retweeted_Users.csv", sep=',',index=False)

    print('\n')

# Get most retweeted tweets

    with open(fname, 'r') as f: 
        name = Counter() 
        #name = {}
        for line in f: 
            tweet = json.loads(line) 
            if tweet['text'][:2] == 'RT':
                name.update([tweet['text']])

    print('\n' + '------------ 20 most retweeted tweets' + '\n')
    #print(name)
    for tag, count in name.most_common(20): 
      print("{}: {}".format(tag, count)) 

    # Save to file

    df = pd.DataFrame(name.items(), columns=['Tweet','Freq'])
    df.to_csv("./csv/Retweeted.csv", sep=',',index=False)

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

    # Save to file

    df = pd.DataFrame(name.items(), columns=['Mentioned','Freq'])
    df.to_csv("./csv/mentions.csv", sep=',',index=False)

    print('\n')

# Gest most common hashtags

    with open(fname, 'r') as f: 
        hashtags = Counter() 
        for line in f: 
            tweet = json.loads(line) 
            hashtags_in_tweet = get_hashtags(tweet) 
            hashtags.update(hashtags_in_tweet) 

    print('\n' + '------------ 20 most common hashtags' + '\n')
    for tag, count in hashtags.most_common(20): 
        print("{}: {}".format(tag, count)) 

    # Save to file

    df = pd.DataFrame(hashtags.items(), columns=['Location','Freq'])
    df.to_csv("./csv/hashtags.csv", sep=',',index=False)

    print('\n')

    # Get most repeated words from list of tweets

    with open(fname, 'r') as f: 
        name = Counter() 
        #name = {}
        for line in f: 
            tweet = json.loads(line) 
            [ name.update([word]) for word in tweet['text'][4:].lower().split() if not word in stop_words ]

    print('\n' + '------------ 20 most repeated words' + '\n')
    for tag, count in name.most_common(20): 
        print("{}: {}".format(tag, count)) 

    # Save to file

    df = pd.DataFrame(name.items(), columns=['Words','Freq'])
    df.to_csv("./csv/words.csv", sep=',',index=False)

    print('\n')

    # Get most frequent locations from list of tweets 

    with open(fname, 'r') as f: 
        name = Counter() 
        for line in f: 
            tweet = json.loads(line) 
            location = get_user_location(tweet).split(',')[0] 
            name.update([location]) 

    print('\n' + '------------ 20 most used locations' + '\n')
    #print(name)
    for tag, count in name.most_common(20):
        if tag == '':
            tag = 'No Location' 
        print("{}: {}".format(tag, count)) 

    # Save to file

    df = pd.DataFrame(name.items(), columns=['Location','Freq'])
    df.to_csv("./csv/locations.csv", sep=',',index=False)

    print('\n')

# Gest most common urls

    with open(fname, 'r') as f: 
        urls = Counter() 
        for line in f: 
            tweet = json.loads(line) 
            urls_in_tweet = get_urls(tweet) 
            urls.update(urls_in_tweet) 

    print('\n' + '------------ 20 most common urls' + '\n')
    for tag, count in urls.most_common(20): 
        print("{}: {}".format(tag, count)) 

    print('\n')

    # Save to file

    df = pd.DataFrame(urls.items(), columns=['URL','Freq'])
    df.to_csv("./csv/urls.csv", sep=',',index=False)

    