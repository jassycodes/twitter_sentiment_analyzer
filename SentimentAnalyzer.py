import os
import re


class SentimentToAnalyze():
			def __init__(self, text):
				self.text = text
				self.positiveWordsSet = set()#0 #int
				self.negativeWordsSet = set() #0 #int
				self.positivetxt = os.path.realpath("data/positive-words.txt") #get address of positive-words.txt
				self.negativetxt = os.path.realpath("data/negativewords.txt") #get address of negative-words.txt
				self.positiveWordsStr = ""
				self.negativeWordsStr = ""
				self.sentiment = self.analyzeSentiment()
				self.positiveWordsList = list(self.positiveWordsSet)
				self.negativeWordsList = list(self.negativeWordsSet)
				self.PosNegTotal = len(self.positiveWordsSet) + len(self.negativeWordsSet)
				self.positivePercentage = 0
				self.negativePercentage = 0
				self.allInfo = {}
				self.setInfo()

			#a function that analyzes a sentiment of a text and returns a string: "positive", "negative" or "neutral"
			def analyzeSentiment(self): 
				tweetStripped = self.text.strip() #remove whitespaces 
				#print("Analyzing. . . . . \n " + ' " ' + tweetStripped + ' " ' + "\n") #check -> SentimentText: value 
				tweetWords = tweetStripped.split() 
				self.positiveWordsSet = self.createSetOfWords(tweetWords, self.positivetxt) #list of positive words
				self.negativeWordsSet = self.createSetOfWords(tweetWords, self.negativetxt) #list of negative words
				#print(self.positiveWordsSet)
				#print(self.negativeWordsSet)

				if len(self.positiveWordsSet) > len(self.negativeWordsSet):
					return "positive"
				elif len(self.positiveWordsSet) < len(self.negativeWordsSet):
					return "negative"
				else:
					return "inconclusive"

			def createSetOfWords(self, strList, txtFile):
				setOfWords = set()
				regex = re.compile('[^a-zA-Z]')

				for wordTweet in strList: #a function that creates a set (no duplicates) of words
					textAllAlpha = regex.sub('', wordTweet).strip() #strip the words to only have letters (no special characters)

					with open(txtFile, "r") as txtLines: #open the file that contains strings you're comparing each word in the strList to
						for everyWord in txtLines:
							if textAllAlpha.lower() == everyWord.strip() and textAllAlpha.lower() != "":
								setOfWords.add(everyWord.strip()) #add to the set of words in the current srting

				return setOfWords

			#changes the source of positive words for comparison.
			#newPositivetxt - a parameter; should be a variable containing the path to the new positive words txt source
			def changePositiveDictSource(self, newPositivetxt):
				self.positivetxt = newPositivetxt

			#changes the source of negative words for comparison.
			#newNegativetxt - a parameter; should be a variable containing the path to the new negative words txt source
			def changePositiveDictSource(self, newNegativetxt):
				self.negativetxt = newNegativetxt

			def getPositivePercentage(self):
				if(self.PosNegTotal > 0):
					self.positivePercentage = (len(self.positiveWordsSet)/self.PosNegTotal)*100
				return self.positivePercentage

			def getNegativePercentage(self):
				if(self.PosNegTotal > 0):
					self.posnegTotal = len(self.positiveWordsSet) + len(self.negativeWordsSet)
					self.negativePercentage = (len(self.negativeWordsSet)/self.PosNegTotal)*100
				return self.negativePercentage

			def getPositiveWords(self):
				return self.positiveWordsSet

			def getNegativeWords(self):
				return self.negativeWordsSet

			def setInfo(self):
				self.allInfo['text'] = self.text
				self.allInfo['sentiment'] = self.analyzeSentiment()
				self.allInfo['positivePercentage'] = "{:.2f}%".format(self.getPositivePercentage())
				self.allInfo['negativePercentage'] = "{:.2f}%".format(self.getNegativePercentage())
				
				if len(self.positiveWordsList) != 0:
					for i in range(0,len(self.positiveWordsList)):
						self.positiveWordsStr = ", ".join(self.positiveWordsList[0:len(self.positiveWordsList)])
					self.allInfo['positiveWords'] = self.positiveWordsStr
				else:
					self.allInfo['positiveWords'] = "NONE"
				
				if len(self.negativeWordsList) != 0:
					for i in range(0,len(self.negativeWordsList)):
						self.negativeWordsStr = ", ".join(self.negativeWordsList[0:len(self.negativeWordsList)])
					self.allInfo['negativeWords'] = self.negativeWordsStr
				else:
					self.allInfo['negativeWords'] = "NONE"

			def getInfo(self):

				return self.allInfo




	#### END -- Class: SentimentToAnalyze ######
	########################################