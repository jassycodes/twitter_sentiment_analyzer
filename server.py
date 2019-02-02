from flask import Flask, render_template, request
from flask import redirect, url_for 
from flask import jsonify
import requests
import os
import re
import html
import SentimentAnalyzer



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

	tweets_dict = get_tweets(text)
	#print(tweets_dict.keys()) #to check the keys names of tweets_dict 
	listOfTweets = []
	tweetSentimentPercentage = []
	tweet_sentiment_dict = {}
	listOfTweetsInfo = []
	#words_set = set()
	#word_freq_dict = {}

	for t in tweets_dict['statuses']:
		listOfTweets.append(t['text'])

	for tweet in listOfTweets:
		tweetToAnalyze = SentimentAnalyzer.SentimentToAnalyze(tweet)
		tweetSentiment = tweetToAnalyze.analyzeSentiment()
		#print(tweetToAnalyze.getInfo())
		tweetInfo = tweetToAnalyze.getInfo()
		#print(type(tweetInfo['positivePercentage']))
		listOfTweetsInfo.append(tweetInfo)
	
	#for word in words_set:
	#	word_freq_dict['word'] = 


		#positivePercentage = tweetToAnalyze.getPositivePercentage()
		#negativePercentage = tweetToAnalyze.getNegativePercentage()
		#positiveResult = "Positive %: " + "{:.2f}".format(positivePercentage) + "%"
		#negativeResult = "Negative %: " + "{:.2f}".format(negativePercentage) + "%"
		#print(tweetSentiment)
		#tweetSentimentPercentage.append(positiveResult + " and " + negativeResult)







	print("len of list: " )
	print(len(listOfTweets))

	return render_template('twitter_sa.html', text=text, tweets=listOfTweets, tweetsInfo=listOfTweetsInfo)

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