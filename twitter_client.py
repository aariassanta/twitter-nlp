# Chap02-03/twitter_client.py 
import os 
import sys 
from credentials import *
from tweepy import API 
from tweepy import OAuthHandler 
 
def get_twitter_auth(): 
  """Setup Twitter authentication. 
 
  Return: tweepy.OAuthHandler object 
  """ 
  
  auth = OAuthHandler(consumer_key, consumer_secret) 
  auth.set_access_token(access_token, access_secret) 
  return auth 
 
def get_twitter_client(): 
  """Setup Twitter API client. 
 
  Return: tweepy.API object 
  """ 
  auth = get_twitter_auth() 
  client = API(auth) 
  return client 