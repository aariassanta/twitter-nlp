# Get Tweets by Search Term 
# Usage: Python twitter_get_search_term.py <search_term>
# Return: file with name search_term_<search_term>.jsonl

import sys 
import json 
from tweepy import Cursor 
from twitter_client import get_twitter_client 
 
if __name__ == '__main__': 
  search_term = sys.argv[1] 
  client = get_twitter_client() 
 
  fname = "search_term_{}.jsonl".format(search_term) 
 
  with open(fname, 'w') as f: 
    for page in Cursor(client.search,
                       q=search_term,
                       #since='2020-09-01', 
                       #until='2020-10-05',  
                       count=5000,
                       monitor_rate_limit=True,
                       wait_on_rate_limit=True,
                       wait_on_rate_limit_notify=True).pages(): 
        for status in page: 
            f.write(json.dumps(status._json)+"\n")