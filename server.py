from flask import Flask, render_template, request, Response, make_response
from flask import redirect, url_for 
from flask import jsonify
import requests
import os
import re
import html
import SentimentAnalyzer
import sqlite3
import datetime
from functools import wraps

app = Flask(__name__)

now = datetime.datetime.now()

####SQL CONNETION####
connection = sqlite3.connect('data/twitter.db')

c = connection.cursor()
# c.execute('''DROP TABLE IF EXISTS tweets''')
# c.execute('''DROP TABLE IF EXISTS users''')

c.execute('''CREATE TABLE IF NOT EXISTS tweets 
			 (id INTEGER PRIMARY KEY AUTOINCREMENT, tweet text NOT NULL, date_posted default CURRENT_DATE, user_id INTEGER, FOREIGN KEY(user_id) REFERENCES users(id))''')
c.execute('''CREATE TABLE IF NOT EXISTS users
			 (id INTEGER PRIMARY KEY AUTOINCREMENT, username text NOT NULL, password VARCHAR(12) NOT NULL, fname text, lname text, birthday date)''')
c.execute("SELECT * FROM tweets")
	 
connection.commit()
connection.close()

@app.route("/twitter_clone")
def twitterClone():
	return render_template('tweets_in_db.html')

@app.route("/tweet-posted", methods=['POST'])
def tweetPosted():
	tweet = request.form.get('tweetPost')
	username = request.form.get('username')

	status = ""
	user_tweets_list = []
	connection = sqlite3.connect('data/twitter.db')
	c = connection.cursor()

	userFound = True

	c.execute("SELECT username FROM users WHERE username='{}'".format(username))
	query = "SELECT * FROM users WHERE username='{}'".format(username)
	print(query)
	print("c.fetchone()")
	print(c.fetchall()[0][0])
	print(type(c.fetchall()))
	print(len(c.fetchall()))

	if type(c.fetchall()) == type(list):
		c.execute("SELECT username FROM users WHERE username='{}'".format(username))
		username_in_db = c.fetchall()[0]
		print(username_in_db)
		c.execute("SELECT id FROM users WHERE username=?",(username,))
		userID_in_db = c.fetchall()[0]
		print(userID_in_db)
		c.execute("INSERT INTO tweets(user_id, tweet) VALUES(?,?);", (userID_in_db, tweet))
		status = "'" + username + "' already exists"
	else:
		userFound = False

	c.execute("SELECT tweet FROM tweets, users WHERE users.id = user_id and username=?",(username,))
	user_tweets = c.fetchall()

	if c.fetchall() is tuple:
		for user_tweet in user_tweets:
			user_tweets_list.append(user_tweet[0])
			print(user_tweet[0])

	connection.commit()
	connection.close()

	return render_template('tweets_in_db.html', status_PostTweet=status, userTweets=user_tweets_list, username=username+"'s")

@app.route("/create-new-user", methods=['POST'])
def new_user():
	username = request.form.get('username')
	password = request.form.get('pword')

	status = ""
	connection = sqlite3.connect('data/twitter.db')
	c = connection.cursor()

	userFound = True

	c.execute("SELECT username FROM users WHERE username=?",(username,))
	
	if c.fetchone() is tuple:
		username_in_db = c.fetchone()[0]
		if username_in_db != username:
			userFound = False
			c.execute("INSERT INTO users(username, password) VALUES(?,?);", (username, password))
			status = "Succesfully created your account!"
		else:
			userFound = True
			status = "'" + username + "' already exists"
	else:
		userFound = False
		c.execute("INSERT INTO users(username, password) VALUES(?,?);", (username, password))
		status = "Succesfully created your account!"

	connection.commit()
	connection.close()

	return render_template('tweets_in_db.html', status_CreateUser=status)

@app.route('/')
def homepage():
	return render_template('twitter_sa.html')

def get_tweets(searchitem):
	url = 'https://api.twitter.com/1.1/search/tweets.json?q=%23{}&result_type=recent'.format(searchitem)
	headers = {'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAAC%2BR9QAAAAAAskoYJ290Ra9xcYfT6rp9e%2FJ7K2s%3DOgraEDCcAd6D6cCEmAtZSSql5B0uXlJ7oOCXsThCt5WxBr57yh'}
	res = requests.get(url, headers=headers)
	return res.json()

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

if __name__ == '__main__':
   app.run()
