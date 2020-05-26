import os
import tweepy
import logging
import re

# Config
MAX_CHAR_FOR_TWEET = 240
BOTNAME = "@ConstAssembly"

logging.basicConfig(filename="bot.log", level=logging.DEBUG)


def create_api():
    consumer_key = os.getenv("CONSUMER_KEY")
    consumer_secret = os.getenv("CONSUMER_SECRET")
    access_token = os.getenv("ACCESS_TOKEN")
    access_token_secret = os.getenv("ACCESS_SECRET")

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    try:
        api.verify_credentials()
    except Exception as e:
        logging.error("Error creating API", exc_info=True)
        raise e
    logging.info("API created")
    return api


# -*- coding: utf-8 -*-
alphabets = "([A-Za-z])"
prefixes = "(Mr|St|Mrs|Ms|Dr)[.]"
suffixes = "(Inc|Ltd|Jr|Sr|Co)"
starters = "(Mr|Mrs|Ms|Dr|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
websites = "[.](com|net|org|io|gov)"


def split_into_sentences(text):
    text = " " + text + "  "
    text = text.replace("\n", " ")
    text = re.sub(prefixes, "\\1<prd>", text)
    text = re.sub(websites, "<prd>\\1", text)
    if "Ph.D" in text:
        text = text.replace("Ph.D.", "Ph<prd>D<prd>")
    text = re.sub("\s" + alphabets + "[.] ", " \\1<prd> ", text)
    text = re.sub(acronyms + " " + starters, "\\1<stop> \\2", text)
    text = re.sub(
        alphabets + "[.]" + alphabets + "[.]" + alphabets + "[.]",
        "\\1<prd>\\2<prd>\\3<prd>",
        text,
    )
    text = re.sub(alphabets + "[.]" + alphabets + "[.]", "\\1<prd>\\2<prd>", text)
    text = re.sub(" " + suffixes + "[.] " + starters, " \\1<stop> \\2", text)
    text = re.sub(" " + suffixes + "[.]", " \\1<prd>", text)
    text = re.sub(" " + alphabets + "[.]", " \\1<prd>", text)
    if "”" in text:
        text = text.replace(".”", "”.")
    if '"' in text:
        text = text.replace('."', '".')
    if "!" in text:
        text = text.replace('!"', '"!')
    if "?" in text:
        text = text.replace('?"', '"?')
    text = text.replace(".", ".<stop>")
    text = text.replace("?", "?<stop>")
    text = text.replace("!", "!<stop>")
    text = text.replace("<prd>", ".")
    sentences = text.split("<stop>")
    sentences = sentences[:-1]
    sentences = [s.strip() for s in sentences]
    return sentences


api = create_api()

# read all lines
f_data = open("data.txt")
lines = f_data.readlines()
f_data.close()

# read last line
f = open("last_line.txt")
last_line_data = f.readlines()
f.close()

# get line to tweet
line_to_tweet = int(last_line_data[0])
line_char = int(last_line_data[1])

pending_tweet = ""

# check for ignorable lines
while True:
    line = lines[line_to_tweet]
    if line == "\n":
        line_to_tweet += 1
    else:
        break

# if it matches with 1.1.1 format, skip line, add name, save to file
if re.match("^\d*\.\d*\.\d*", line):
    line_to_tweet += 1
    pending_tweet = lines[line_to_tweet]
    line_to_tweet += 1
    of = open("last_line.txt", "w")
    of.writelines([str(line_to_tweet), "\n", str(line_char)])
    of.close()

# check if it is a sentence
sentences = split_into_sentences(lines[line_to_tweet][line_char:])

if len(sentences) > 0:
    first_sentence = sentences[0]

    if len(first_sentence) != len(lines[line_to_tweet]):
        line_char = lines[line_to_tweet].find(first_sentence) + len(first_sentence)

    pending_tweet += first_sentence

    if len(sentences) == 1:
        line_char = 0
        line_to_tweet += 1
else:
    pending_tweet += lines[line_to_tweet]
    line_to_tweet += 1
    line_char = 0

# create tweet
logging.info("sending tweet: ===\n" + pending_tweet + "\n===")

out_tweet = ""
prev_status = None
while True:
    out_tweet = pending_tweet[:240]
    try:
        if prev_status == None:
            prev_status = api.update_status(status=out_tweet)
        else:
            prev_status = api.update_status(
                status=out_tweet, in_reply_to_status_id=prev_status.id
            )
    except tweepy.TweepError as error:
        if error.api_code == 187:
            # Do something special
            api.update_status(status=out_tweet + ".")
        else:
            raise error

    pending_tweet = pending_tweet[240:]
    if len(pending_tweet) == 0:
        break

of = open("last_line.txt", "w")
of.writelines([str(line_to_tweet), "\n", str(line_char)])
of.close()
