#

import sys
from collections import Counter
import json
from stop_words import get_stop_words
import pandas as pd

additional_stop_words = ['https','-','amp','&amp;']
stop_words = get_stop_words('english') \
    + get_stop_words('spanish') \
    + get_stop_words('french') \
    + additional_stop_words


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


def get_tweet_id(tweet):
    retweeted = tweet.get('retweeted_status', {})
    id = retweeted.get('id_str', [])
    return id


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
    # print(name)
    for tag, count in name.most_common(20):
        print("{}: {}".format(tag, count))

    # Save to file

    df = pd.DataFrame(name.items(), columns=['User', 'Freq'])
    df.to_csv("./csv/users.csv", sep=',', index=False)

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
    # print(name)
    for tag, count in name.most_common(20):
        print("{}: {}".format(tag, count))

    # Save to file

    df = pd.DataFrame(name.items(), columns=['User', 'Freq'])
    df.to_csv("./csv/retweeted_users.csv", sep=',', index=False)

    print('\n')

# Get most retweeted tweets

    with open(fname, 'r') as f:
        name = Counter()
        #name = {}
        for line in f:
            tweet = json.loads(line)
            if tweet['text'][:2] == 'RT':
                id = get_tweet_id(tweet)
                name.update([str(id) + ' ' + tweet['text']])

    print('\n' + '------------ 20 most retweeted tweets' + '\n')
    # print(name)
    for tag, count in name.most_common(20):
        print("{}: {}".format(tag, count))

    df = pd.DataFrame(name.items(), columns=['Tweet', 'Freq'])

    # Separa Id del tweet retuiteado del tecto del mismo y crea
    # columna adicional Id con el número

    splitted = df['Tweet'].str.split(n=1, expand=True)
    # print(splitted)
    df['Tweet'] = splitted[1]
    df['Id'] = splitted[0]

    # Save to file

    df.to_csv("./csv/retweeted.csv", sep=',', index=False)

    print('\n')

# Get most mentioned users

    with open(fname, 'r') as f:
        name = Counter()
        for line in f:
            tweet = json.loads(line)
            name_in_tweet = get_mentioned_name(tweet)
            name.update(name_in_tweet)

    print('\n' + '------------ 20 most mentioned users' + '\n')
    # print(name)
    for tag, count in name.most_common(20):
        print("{}: {}".format(tag, count))

    # Save to file

    df = pd.DataFrame(name.items(), columns=['Mentioned', 'Freq'])
    df.to_csv("./csv/mentions.csv", sep=',', index=False)

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

    df = pd.DataFrame(hashtags.items(), columns=['Hashtag', 'Freq'])
    df.to_csv("./csv/hashtags.csv", sep=',', index=False)

    print('\n')

    # Get most repeated words from list of tweets

    with open(fname, 'r') as f:
        name = Counter()
        #name = {}
        for line in f:
            tweet = json.loads(line)
            #[ name.update([word]) for word in tweet['text'][4:].lower().split() if not word in stop_words ]
            [name.update([word]) for word in tweet['text'][4:].lower().split() if (
                (not word in stop_words) & (word[0] is not '#'))]

    print('\n' + '------------ 20 most repeated words' + '\n')
    for tag, count in name.most_common(20):
        print("{}: {}".format(tag, count))

    # Save to file

    df = pd.DataFrame(name.items(), columns=['Word', 'Freq'])
    df.to_csv("./csv/words.csv", sep=',', index=False)

    print('\n')

    # Get most frequent locations from list of tweets

    with open(fname, 'r') as f:
        name = Counter()
        for line in f:
            tweet = json.loads(line)

            # Si localizacion está vacia no hacer split para evitar error

            if (get_user_location(tweet) is not None):
                location = get_user_location(tweet).split(',')[0]
            else:
                location = get_user_location(tweet)

            name.update([location])

    print('\n' + '------------ 20 most used locations' + '\n')
    # print(name)
    for tag, count in name.most_common(20):
        if tag == '':
            tag = 'No Location'
        print("{}: {}".format(tag, count))

    # Save to file

    df = pd.DataFrame(name.items(), columns=['Location', 'Freq'])
    df.to_csv("./csv/locations.csv", sep=',', index=False)

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

    df = pd.DataFrame(urls.items(), columns=['URL', 'Freq'])
    df.to_csv("./csv/urls.csv", sep=',', index=False)


# Get last created tweet

    with open(fname, 'r') as f:
        #name = Counter()
        last_updated = ''
        for line in f:
            tweet = json.loads(line)
            if tweet['created_at'] > last_updated:
                last_updated = tweet['created_at']

    print('\n' + '------------ last created date tweet' + '\n')
    
    print("Fecha último tweet creado: {}".format(last_updated))

    # Separa Id del tweet retuiteado del tecto del mismo y crea
    # columna adicional Id con el número

    #splitted = df['Tweet'].str.split(n=1, expand=True)
#   
    df_last_updated = pd.DataFrame()
    df_last_updated['last_updated'] = [last_updated]
    #df['Id'] = splitted[0]

    # Save to file

    df_last_updated.to_csv("./csv/last_updated.csv", sep=',', index=False)

    print('\n')



# --------------------------------------------------------------------------------
# Starting NLP process
# --------------------------------------------------------------------------------

from string import punctuation
from nltk import word_tokenize
from nltk.util import ngrams
#from nltk.corpus import stopwords
from nltk import FreqDist

# cleaning text data

# Generación stoplist

#additionalstopwords = ['https','proptech','amp']

#stoplist = set(stopwords.words('english')) | \
#           set(stopwords.words('spanish')) | \
#           set(stopwords.words('french')) |  \
#           set(punctuation) |                \
#           set(additionalstopwords)


# Get not retweeted tweets

tweets_df = pd.read_json (fname, orient='records', lines=True)

tweets_df['is_no_retweet'] = tweets_df['text'].apply(lambda x: x[:2]!='RT')
tweets_df_no_rt = tweets_df.loc[tweets_df['is_no_retweet']]

# Convierte a minúsculas todas las palabras

sentences = "".join(tweets_df_no_rt['text']).lower()

# Tokeniza extrayendo palabras a excluír

tokens = [token for token in word_tokenize(sentences) if token not in stop_words] # No stoplist
tokens = [token for token in tokens if token.isalpha()] # sólo caracteres alfabéticos

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
