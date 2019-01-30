from flask import Flask, render_template, request
from flask import redirect, url_for 
from flask_dance.contrib.twitter import make_twitter_blueprint, twitter #twitter
import requests
import os
import re
import html


app = Flask(__name__)

@app.route("/")
def index():
    if not twitter.authorized:
        return redirect(url_for("twitter.login"))
    resp = twitter.get("account/settings.json")
    assert resp.ok
    return "You are @{screen_name} on Twitter".format(screen_name=resp.json()["screen_name"])

app.secret_key = "supersekrit"
blueprint = make_twitter_blueprint(
    api_key="cW0YXg9qtZkpR7n35QEt6TE4l",
    api_secret="uEmz0ElHJcqbkQ18cqlTzLRoW8CsH04xHYvcxHNWDQgeD5nuIM",
)
app.register_blueprint(blueprint, url_prefix="/login")

#twitter = Twitter(
#            auth=OAuth(os.environ.get('OAUTH_TOKEN'), os.environ.get('OAUTH_SECRET'),
#                       os.environ.get('CONSUMER_KEY'), os.environ.get('CONSUMER_SECRET'))           

#           )


@app.route('/threetweets')
def main():

	# fetch 3 tweets from my account
	myTweets = twitter.statuses.user_timeline(count=10)

	# fetch 3 tweets from ITP_NYU
	itpTweets = twitter.statuses.user_timeline(screen_name='jassycodes', count=10)
	
	# app.logger.debug(itpTweets)

	templateData = {
		'title' : 'My last three tweets',
		'myTweets' : myTweets,
		'itpTweets' : itpTweets
	}
consumer_key = 'cW0YXg9qtZkpR7n35QEt6TE4l'
consumer_secret = 'uEmz0ElHJcqbkQ18cqlTzLRoW8CsH04xHYvcxHNWDQgeD5nuIM'
callback = 'http://127.0.0.1:5000/callback'

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
    session['token'] = (auth.access_token, auth.access_token_secret)

    return redirect('/app')

@app.route('/app')
def request_twitter():
    token, token_secret = session['token']
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret, callback)
    auth.set_access_token(token, token_secret)
    api = tweepy.API(auth)

    return api.me()

@app.route('/twittersentiment')
def tweet_sentiment():
	return render_template('twitter_sa.html')

@app.route('/', methods=['POST'])
def my_form_post():
	text = request.form['text']
	processed_text = text.upper()
	return processed_text

	# render_template('base.html')

#def get_tweets(searchitem):
#	url = 'https://api.twitter.com/1.1/search/tweets.json?q=%23{}&result_type=recent'.format(searchitem)
#	headers = {'authorization': 'Bearer <AAAAAAAAAAAAAAAAAAAAAC%2BR9QAAAAAAskoYJ290Ra9xcYfT6rp9e%2FJ7K2s%3DOgraEDCcAd6D6cCEmAtZSSql5B0uXlJ7oOCXsThCt5WxBr57yh>'}
#	res = requests.get(url, headers=headers)
#	print(searchitem)


#print(get_tweets("tweet"))
		
if __name__ == '__main__':
   app.run()


#curl -u 'cW0YXg9qtZkpR7n35QEt6TE4l:uEmz0ElHJcqbkQ18cqlTzLRoW8CsH04xHYvcxHNWDQgeD5nuIM' \
#  --data 'grant_type=client_credentials' \
#  'https://api.twitter.com/oauth2/token'