'''
PSU vs PITT - Twitter Sentiment Analysis
Author: Andrew Warner
Nittany Data Labs
'''
import json
from collections import Counter
from nltk import ne_chunk, pos_tag, word_tokenize
from nltk.chunk import conlltags2tree, tree2conlltags

# Constants
PITT_ENTITIES = ['PITT', 'PITT', 'PANTHERS', 'UPITT',  'JOE', 'PA', 'DADDY DUZY']
PSU_ENTITIES = ['PENN', 'STATE', 'LIONS', 'NITTANY', 'STATE COLLEGE', 'UNIVERSITY PARK','EAT','SHIT', '#HangAHundredOnPitt']

# Read in file
fname = 'data/pitt_psu_sentiment.json'
with open(fname, 'r') as df:
	data = json.load(df)

class tweet():
	def __init__(self, time_stamp, sentiment, text):
		# self.PITT = ['PITT', 'PITT', 'PANTHERS',
		# 				'UPITT',  'JOE', 'PA', 'DADDY DUZY']
		# self.PSU = ['PENN', 'STATE', 'LIONS', 'NITTANY', 'STATE COLLEGE',
		# 			'UNIVERSITY PARK','EAT','SHIT', '#HangAHundredOnPitt']
		self.time = self.set_time(time_stamp)
		self.hour, self.minute = self.time.split(':')
		self.hour = int(self.hour)
		self.minute = int(self.minute)
		self.sentiment = sentiment
		self.text = self.set_text(text)
		self.bias = ''
	def set_time(self, time):
		T = time.rfind('T') + 1
		seconds = time.rfind(':')
		return str(time[T:seconds])
	def set_bias(self, bias):
		self.bias = bias
	def set_text(self, text):
		parsed = []
		for entry in text:
			try:
				entry = str(entry).upper()
				parsed.append(entry)
			except UnicodeEncodeError:
				# print "Cannot Encode Character %s" % entry
				pass
		return parsed


tweets = [tweet(d['timestamp'], d['sentiment'], d['text']) for d in data]

for tweet in tweets:
	counts = Counter(tweet.text)
	# print counts
	pitt = 0
	psu = 0
	for word, count in counts.items():
		if word in PITT_ENTITIES:
			pitt += 1
		if word in PSU_ENTITIES:
			psu += 1
	if pitt == psu:
		tweet.set_bias('neutral')
	elif pitt < psu:
		tweet.set_bias('pitt')
	elif pitt > psu:
		tweet.set_bias('psu')
	# print tweet.text, tweet.bias

tweets = [tweet for tweet in tweets if tweet.bias == 'psu' or tweet.bias == 'neutral']
# times = {'03:30':0, '03:45':0, '04:00':0, '04:15':0, '04:30':0, '04:45':0,
# 		'05:00':0, '05:15':0, '05:30':0, '05:45':0, '06:00':0, '06:15':0,
# 		'06:30':0, '06:45':0, '07:00':0}
times = ['03:00', '03:15', '03:30', '03:45', '04:00', '04:15', '04:30', '04:45', '05:00', '05:15', '05:30',
		'05:45', '06:00', '06:15', '06:30', '06:45', '07:00', '07:15', '07:30', '7:45', '8:00']
average_sentiment = {}
for time in times:
	# print time
	average_sentiment[time] = 0
	count = 0
	hour, minute = time.split(':')
	hour = int(hour)
	minute = int(minute)
	for tweet in tweets:
		if tweet.hour == hour:
			# print tweet.hour
			if tweet.minute < minute + 15:
				average_sentiment[time] += tweet.sentiment
				count += 1
	average_sentiment[time] = average_sentiment[time] / count

# Persist to File
output = open('data/temporal_sentiment.csv', 'wb')
for k, v in sorted(average_sentiment.items()):
	output.write(str(k) + ',' + str(v) +'\n')
output.close()
