from flask import Flask, render_template, request
from flask import redirect, url_for 
from flask import jsonify
import requests
import os
import re
import html



app = Flask(__name__)

@app.route("/getusername")
def index():
	if not twitter.authorized:
		return redirect(url_for("twitter.login"))
	resp = twitter.get("account/settings.json")
	assert resp.ok
	return "You are @{screen_name} on Twitter".format(screen_name=resp.json()["screen_name"])


@app.route('/')
def homepage():
	return render_template('twitter_sa.html')

def get_tweets(searchitem):
	url = 'https://api.twitter.com/1.1/search/tweets.json?q=%23{}&result_type=recent'.format(searchitem)
	headers = {'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAAC%2BR9QAAAAAAskoYJ290Ra9xcYfT6rp9e%2FJ7K2s%3DOgraEDCcAd6D6cCEmAtZSSql5B0uXlJ7oOCXsThCt5WxBr57yh'}
	res = requests.get(url, headers=headers)
	return res.json()

#print(get_tweets("hello"))


@app.route('/twittersentiment', methods=['GET'])
def tweet_sentiment():
	if request.method == 'GET':
		text = request.args.get('text')
	def printSomething():
		print(text)
	printSomething()
	tweets_dict = get_tweets(text)
	listOfTweets = []
	print(type(tweets_dict['statuses'][:5]))
	print(tweets_dict['statuses'][:1])
	for t in tweets_dict['statuses'][:50]:
	#	print(tweets_dict['statuses'])
		#print()
		#print(t.get('statuses'))#listOfTweets.append(t.get('text'))
		listOfTweets.append(t['text'])
		#print(type(t))

	return render_template('twitter_sa.html', text=text, tweets=listOfTweets)

@app.route('/gettext', methods=['POST'])
def my_form_post():
	text = request.form['text']
	processed_text = text.upper()
	return render_template('/')


#print(get_tweets("tweet"))
		
if __name__ == '__main__':
   app.run()

#token : {"token_type":"bearer","access_token":"AAAAAAAAAAAAAAAAAAAAAC%2BR9QAAAAAAskoYJ290Ra9xcYfT6rp9e%2FJ7K2s%3DOgraEDCcAd6D6cCEmAtZSSql5B0uXlJ7oOCXsThCt5WxBr57yh"}


#curl -u 'cW0YXg9qtZkpR7n35QEt6TE4l:uEmz0ElHJcqbkQ18cqlTzLRoW8CsH04xHYvcxHNWDQgeD5nuIM' \
#  --data 'grant_type=client_credentials' \
#  'https://api.twitter.com/oauth2/token'