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


listOfPostedTweets = []

@app.route('/twittersentiment', methods=['GET', 'POST'])
def tweet_sentiment():	

	listOfTweets = []
	tweetSentimentPercentage = []
	tweet_sentiment_dict = {}
	listOfTweetsInfo = []
	tweets_dict = {}
	tweetCount = 0

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


		print("len of list: " )
		print(len(listOfTweets))

		return render_template('twitter_sa.html', text=text, tweets=listOfTweets, tweetsInfo=listOfTweetsInfo)
	tweetCount += 1
	if request.method == 'POST':
		tweetPost = request.form.get('tweetPost')

		print(tweetPost)
		print(type(tweetPost))
		lasttweetIDindex = len(listOfPostedTweets)
		
		tweets_dict["tweetCount"] = lasttweetIDindex
		tweets_dict["tweet"] = tweetPost
		listOfPostedTweets.append(tweets_dict)
	
		return render_template('twitter_sa.html', postedTweet=tweetPost, tweets_dict=listOfPostedTweets)
	tweetCount += 1


@app.route('/newtweets')
def new_tweets_homepage():
	new_tweets_txtfile = os.path.realpath("data/new-tweets.txt") #get address of sentiment analysis
	with open(new_tweets_txtfile, "r") as f:
		text_list = []
		for everyLine in f:
			text_list.append(everyLine)

	return render_template('new_tweets.html', tweets=text_list)

@app.route('/posttweets', methods=['POST'])
def post_tweets():
	newTweet = request.form.get('tweetPost')
	new_tweets_txtfile = os.path.realpath("data/new-tweets.txt") #get address of sentiment analysis
	with open(new_tweets_txtfile, "a+") as newTweetsf:
		newTweetsf.write(newTweet + "\n")
	
	with open(new_tweets_txtfile, "r") as f:
		text_list = []
		for everyLine in f:
			text_list.append(everyLine)

	return render_template('new_tweets.html', tweets=text_list)

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