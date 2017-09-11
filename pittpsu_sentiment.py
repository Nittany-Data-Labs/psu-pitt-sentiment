'''
PSU vs PITT - Twitter Sentiment Analysis
Author: Yuya Ong (yuyajeremyong@gmail.com)
Nittany Data Labs
'''
from __future__ import print_function
import re
import json
from pprint import pprint

from sentiment import sentiment_score

# Preprocessing Routine
emoticons_str = r"""
    (?:
        [:=;] # Eyes
        [oO\-]? # Nose (optional)
        [D\)\]\(\]/\\OpP] # Mouth
    )"""

regex_str = [
    emoticons_str,
    r'<[^>]+>', # HTML tags
    r'(?:@[\w_]+)', # @-mentions
    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # hash-tags
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs

    r'(?:(?:\d+,?)+(?:\.?\d+)?)', # numbers
    r"(?:[a-z][a-z'\-_]+[a-z])", # words with - and '
    r'(?:[\w_]+)', # other words
    r'(?:\S)' # anything else
]

tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)
emoticon_re = re.compile(r'^'+emoticons_str+'$', re.VERBOSE | re.IGNORECASE)

def tokenize(s):
    return tokens_re.findall(s)

def preprocess(s, lowercase=False):
    tokens = tokenize(s)
    if lowercase:
        tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
    return tokens

# Unit Testing
if __name__ == '__main__':
    data = json.loads(open('data/pitt_psu_tweets.json', 'rb').read())
    print('Total Tweets: ' + str(len(data)))

    tweets = []
    data = sorted(data, key=lambda x: x['timestamp'])
    for d in data: tweets.append({'timestamp':d['timestamp'], 'text':preprocess(d['text']), 'sentiment':sentiment_score(d['text'])})
    # pprint(tweets)

    # Output to File
    output = open('pitt_psu_sentiment.json', 'wb')
    output.write(json.dumps(tweets))
    output.close()
