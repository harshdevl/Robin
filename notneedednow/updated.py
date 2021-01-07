import nltk
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Dropout
from tensorflow.keras.optimizers import SGD
import pandas as pd
import pickle
import json
import random

with open("intents.json") as file:
    data = json.load(file)

words = []
classes = []
documents = []
ignore_words = ['?']

for intent in data['intents']:
    for pattern in intent['patterns']:
        w = nltk.word_tokenize(pattern)
        words.extend(w)
        documents.append((w, intent['tag']))

        if intent['tag'] not in classes:
            classes.append(intent['tag'])

words = [stemmer.stem(w.lower()) for w in words if w not in ignore_words]
words = sorted(list(set(words)))
classes = sorted(list(set(classes)))


training = []
output_empty = [0] * len(classes)
for doc in documents:
    bag = []
    pattern_words = doc[0]
    pattern_words = [stemmer.stem(word.lower()) for word in pattern_words]
    for w in words:
        bag.append(1) if w in pattern_words else bag.append(0)
    
    output_row = list(output_empty)
    output_row[classes.index(doc[1])] = 1
    
    training.append([bag, output_row])

random.shuffle(training)
training = np.array(training)
train_x = list(training[:,0])
train_y = list(training[:,1])

model = Sequential()
model.add(Dense(128, input_shape=(len(train_x[0]),), activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]), activation='softmax'))

sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

model.fit(np.array(train_x), np.array(train_y), epochs=200, batch_size=5, verbose=1)


model.save('jarvis.h5')

with open("jarvis-data.pickle", "wb") as f:
    pickle.dump((words, classes,train_x, train_y), f)

print('model is ready to deply')

# def clean_up_sentence(sentence):
#     # tokenize the pattern - split words into array
#     sentence_words = nltk.word_tokenize(sentence)
#     # stem each word - create short form for word
#     sentence_words = [stemmer.stem(word.lower()) for word in sentence_words]
#     return sentence_words
# # return bag of words array: 0 or 1 for each word in the bag that exists in the sentence
# def bow(sentence, words, show_details=True):
#     # tokenize the pattern
#     sentence_words = clean_up_sentence(sentence)
#     # bag of words - matrix of N words, vocabulary matrix
#     bag = [0]*len(words)  
#     for s in sentence_words:
#         for i,w in enumerate(words):
#             if w == s: 
#                 # assign 1 if current word is in the vocabulary position
#                 bag[i] = 1
                
                    
#     return(np.array(bag))
# def classify():
    
#     print("initiation JARVIS 2.0...")
#     while True:
#         inp = input("You: ")
#         if inp.lower() == "quit":
#             break
#         result = bow(inp,words)
#         inputvar = pd.DataFrame([result], dtype=float, index=['input'])
#         ressult = model.predict(inputvar)
#         result_index = np.argmax(ressult)
#         tag = classes[result_index]
    
#         for tags in data["intents"]:
#             if tags['tag'] == tag:
#                 responses=tags['responses']

#         print(random.choice(responses))
            
