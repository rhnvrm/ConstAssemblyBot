import os
import tweepy

from flask import Flask, redirect, request
app = Flask(__name__)

callback = 'http://localhost:8000/callback'
session = {}
consumer_key = os.getenv("CONSUMER_KEY")
consumer_secret = os.getenv("CONSUMER_SECRET")

@app.route('/auth')
def auth():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret, callback)
    url = auth.get_authorization_url()
    session['request_token'] = auth.request_token
    return redirect(url)

@app.route('/callback')
def twitter_callback():
    request_token = session['request_token']
    del session['request_token']

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret, callback)
    auth.request_token = request_token
    verifier = request.args.get('oauth_verifier')
    auth.get_access_token(verifier)
    print(auth.access_token, auth.access_token_secret)

    return redirect('/app')

if __name__ == '__main__':
    app.run(port=8000)
