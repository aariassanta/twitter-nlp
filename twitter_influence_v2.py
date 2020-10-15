# Chap02-03/twitter_influence.py 
import sys 
import os
import json 
import csv 

from collections import Counter

# Navega por directorio de users y coge nombre de los subdirectorios
# asociados a cada user

subfolders = [ f.path for f in os.scandir('./users') if f.is_dir() ]
users = [ subfolder.split('/')[-1] for subfolder in subfolders ]
#print(users)

# Obtiene ratios relevantes de cada usuario existente en subdirectorios

results = []

for user in users:
    followers_file = 'users/{}/followers.jsonl'.format(user)
    with open(followers_file) as f:
        reach = []
        for line in f:
            profile = json.loads(line)
            reach.append((profile['screen_name'],
                         profile['followers_count']))
    #print(user)

    profile_file = 'users/{}/user_profile.json'.format(user) 
    with open(profile_file) as f: 
      profile = json.load(f) 
      followers = profile['followers_count'] 
      tweets = profile['statuses_count']  
    sum_reach = sum([x[1] for x in reach]) 
    avg_followers = round(sum_reach / followers, 2) 
    #print(sum_reach)

    timeline_file = 'user_timeline_{}.jsonl'.format(user) 
    with open(timeline_file) as f: 
       favorite_count, retweet_count = [], [] 
       for line in f: 
            tweet = json.loads(line) 
            favorite_count.append(tweet['favorite_count']) 
            retweet_count.append(tweet['retweet_count']) 
    avg_favorite = round(sum(favorite_count) / tweets, 2) 
    avg_retweet = round(sum(retweet_count) / tweets, 2) 
    favorite_per_user = round(sum(favorite_count) / followers, 2) 
    retweet_per_user = round(sum(retweet_count) / followers, 2) 
    
    # almacena frecuencia de retweets por tweet
    # si hay 3 tweets que se retweetean 10 veces 
    # se representará como (10 : 3)

    retweets_freq = Counter(retweet_count)

# Imprime en pantalla sumario de los resultados

    print("----- Stats {} -----".format(user)) 
    print("{:,} followers".format(int(followers))) 
    print("{:,} users reached by 1-degree  \
      connections".format(sum_reach)) 
    print("Average number of followers for {}'s followers:  \
      {}".format(user, avg_followers)) 
    print("Favorited {:,} times ({} per tweet, {} per  \
      user)".format(sum(favorite_count), avg_favorite,  
      favorite_per_user)) 
    print("Retweeted {:,} times ({} per tweet, {} per  \
      user)".format(sum(retweet_count), avg_retweet,  
      retweet_per_user)) 
    
    results.append([user, followers, sum_reach, avg_followers, 
                            sum(favorite_count), avg_favorite, favorite_per_user,
                            sum(retweet_count), avg_retweet, retweet_per_user])

    # Presenta tabla histograma de frecuencia retweets por tweet
    # ordenanda de menor a mayor número de retweets

    print('\n') 
    print('# retweets : # tweets' + '\n')
    print(sorted(retweets_freq.items()))
    print('\n')

    # Obtiene los 10 tweets con más retweets de cada usuario y los ordena de mayor a menor

    with open(timeline_file) as f: 
       retweets_per_tweet = [] 
       for line in f: 
            tweet = json.loads(line)
            tweet['is_retweet'] = tweet['text'][:2] == 'RT'
            retweets_per_tweet.append([tweet['retweet_count'], tweet['text'], tweet['is_retweet']]) 
    
    retweets_per_tweet.sort(key=lambda tup: tup[0], reverse=True)

    print('10 most retweeted tweets' + '\n')
    [ print(element) for element in retweets_per_tweet[:10] ]
    print('\n')
    
    print('10 most retweeted ORIGINAL tweets' + '\n')
    res = [ element for element in retweets_per_tweet if not element[2] ]
    [ print(element) for element in res[:10] ]
    print('\n')
    

# Escribe fichero CSV con los resultados

with open('twitter_influence_v2.csv', mode='w') as users_file:
    users_writer = csv.writer(users_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    users_writer.writerow(['user', 'followers', 'sum_reach', 'avg_followers', 
                            'favourite_count', 'avg_favorite', 'favorite_per_user',
                            'retweet_count', 'avg_retweet', 'retweet_per_user' ])
    for user in results:
        users_writer.writerow(user)

       