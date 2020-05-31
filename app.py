# -*- coding: utf-8 -*-
"""PiKot.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/17JjZJ1Ep9todhhla-yHBfSGyHZiQH29C
"""

import io
import random
import string
import warnings
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import warnings
warnings.filterwarnings('ignore')
import requests

from flask import Flask,render_template,url_for,request
app = Flask(__name__)

import nltk
from nltk.stem import WordNetLemmatizer
nltk.download('popular', quiet=True)
nltk.download('punkt')
nltk.download('wordnet')

f=open('harry_potter.txt','r',errors = 'ignore')
raw=f.read()
raw = raw.lower()

sent_tokens = nltk.sent_tokenize(raw) 
word_tokens = nltk.word_tokenize(raw)

lemmer = nltk.stem.WordNetLemmatizer()

def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]
remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)

def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))

GREETING_INPUTS = ("hello", "hi", "greetings", "sup", "what's up","hey",)
GREETING_RESPONSES = ["hi", "hey", "*nods*", "hi there", "hello", "I am Mr. PiKot. Ask me about Harry Potter"]
def greeting(sentence):
 
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)

def response(user_input):
    robo_response=''
    sent_tokens.append(user_input)
    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
    tfidf = TfidfVec.fit_transform(sent_tokens)
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx=vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]
    if(req_tfidf==0):
        robo_response=robo_response+"I am sorry! I can't help you with that."
        return robo_response
    else:
        robo_response = robo_response+sent_tokens[idx]
        return robo_response


@app.route("/")
def home():
	return render_template('test.html', greet = "My name is Mr. PiKot. I will answer your queries about harry potter. If you want to exit, type Bye!")

def Pikot(user_input):

	user_input=user_input.lower()
	if(user_input!='bye'):
		if(user_input=='thanks' or user_input=='thank you'):
			flag=False
			data = "PiKot: You are welcome.."
		else:
			if(greeting(user_input)!=None):
				print("PiKot: "+greeting(user_input))
			else:
				data = "PiKot: " + response(user_input)
				sent_tokens.remove(user_input)
	else:
		flag=False
		data = "PiKot: Good Bye! Talk to you soon."
	return data				

@app.route("/answer", methods=['POST'])
def answer():
	user_input=""
	if request.method=='POST':
		text = request.form['inputtext']
		user_input = text
	output = Pikot(user_input)	
	return render_template('test.html', data = output)	
	
if __name__ == '__main__':
	app.debug = True
	app.run()