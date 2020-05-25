import os
import tweepy
import logging
import re

MAX_CHAR_FOR_TWEET = 240
logging.basicConfig(filename='bot.log',level=logging.DEBUG)

def create_api():
    consumer_key = os.getenv("CONSUMER_KEY")
    consumer_secret = os.getenv("CONSUMER_SECRET")
    access_token = os.getenv("ACCESS_TOKEN")
    access_token_secret = os.getenv("ACCESS_SECRET")

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True, 
        wait_on_rate_limit_notify=True)
    try:
        api.verify_credentials()
    except Exception as e:
        logging.error("Error creating API", exc_info=True)
        raise e
    logging.info("API created")
    return api

   
api = create_api()

# read all lines
f_data=open('data.txt')
lines=f_data.readlines()
f_data.close()

# read last line
f=open('last_line.txt')
last_line_data = f.readlines()
f.close()

# get line to tweet
line_to_tweet = int(last_line_data[0])
line_char = int(last_line_data[1])


# check for ignorable lines
while True:
    line = lines[line_to_tweet]  
    if line == "\n":
        line_to_tweet+=1
    elif re.match("^\d*\.\d*\.\d*", line):
        line_to_tweet+=1
    else:
        break

pending_tweet = lines[line_to_tweet]
# create tweet
if len(pending_tweet) > MAX_CHAR_FOR_TWEET:
    new_line_char = min(line_char+MAX_CHAR_FOR_TWEET, len(pending_tweet)) 

    new_pending_tweet = pending_tweet[line_char:new_line_char]
    
    if new_line_char == len(pending_tweet):
        line_char = 0
        line_to_tweet += 1
    else:
        line_char = new_line_char

    pending_tweet = new_pending_tweet
else:
    line_to_tweet +=1
    
logging.info("sending tweet: "+pending_tweet)
api.update_status(status=pending_tweet)

of = open('last_line.txt', "w")
of.writelines([str(line_to_tweet), '\n', str(line_char)])
of.close()
