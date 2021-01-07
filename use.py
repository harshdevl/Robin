import tensorflow as tf
from tensorflow.keras.models import load_model
import pickle
import nltk
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()
import numpy as np
import pandas as pd
import random
import json


model = load_model('jarvis.h5')

with open("intents.json") as file:
    data = json.load(file)

with open('jarvis-data.pickle', 'rb') as f:

    words,classes, train_x, train_y= pickle.load(f )


# pickle.load( {words,classes,train_x,train_y}, open( "jarvis-data.pkl", "rb" ) )

def classify_local(sentence):
    ERROR_THRESHOLD = 0.25
    
    # generate probabilities from the model
    input_data = pd.DataFrame([bow(sentence, words)], dtype=float, index=['input'])
    results = model.predict([input_data])[0]
    # filter out predictions below a threshold, and provide intent index
    results = [[i,r] for i,r in enumerate(results) if r>ERROR_THRESHOLD]
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append((classes[r[0]], str(r[1])))
    # return tuple of intent and probability
    
    return return_list
    

def clean_up_sentence(sentence):
    # tokenize the pattern - split words into array
    sentence_words = nltk.word_tokenize(sentence)
    # stem each word - create short form for word
    sentence_words = [stemmer.stem(word.lower()) for word in sentence_words]
    return sentence_words
# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence


def bow(sentence, words, show_details=True):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # bag of words - matrix of N words, vocabulary matrix
    bag = [0]*len(words)  
   
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s: 
                # assign 1 if current word is in the vocabulary position
                bag[i] = 1
   
    return(np.array(bag))

def classify(inp):
    
    result = bow(inp,words)

    inputvar = pd.DataFrame([result], dtype=float, index=['input'])

    ressult = model.predict(inputvar)
    result_index = np.argmax(ressult)
    tag = classes[result_index]

    for tags in data["intents"]:
        if tags['tag'] == tag:
            responses=tags['responses']

    return random.choice(responses)
        
