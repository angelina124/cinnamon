#!/usr/bin/env python3

import nltk
nltk.download('punkt')
nltk.download('wordnet')
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import json
import pickle

import tensorflow as tf
from tensorflow import keras
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Dropout
from tensorflow.keras.optimizers import SGD
import random

class NLP:
    words = []
    classes = []
    documents = []
    ignore_words = ['?','!']
    intents = {}
    training = []

    def __init__(self):
        data_file = open('intents.json').read()
        self.intents = json.loads(data_file)['intents']

        for intent in self.intents:
            for pattern in intent['patterns']:
                w = nltk.word_tokenize(pattern)
                self.words.extend(w)
                self.documents.append((w, intent['tag']))

                if intent['tag'] not in self.classes:
                    self.classes.append(intent['tag'])

        # e.g. walking and walked both become "walk"
        self.words = [lemmatizer.lemmatize(w.lower()) for w in self.words if w not in self.ignore_words]
        self.words = sorted(list(set(self.words)))

        self.classes = sorted(list(set(self.classes)))

        pickle.dump(self.words,open('words.pkl','wb'))
        pickle.dump(self.classes,open('classes.pkl','wb'))

    def create_training_data(self):
        training = []

        for document in self.documents:
            output = [0] * len(self.classes)
            word_bag = []
            pattern_words = [lemmatizer.lemmatize(word.lower()) for word in document[0]]

            for word in self.words:
                word_bag.append(1) if word in pattern_words else word_bag.append(0)

            output_row = list(output)
            output_row[self.classes.index(document[1])] = 1

            training.append([word_bag, output_row])

        # shuffle our features and turn into np.array
        random.shuffle(training)
        self.training = np.array(training)
        # create train and test lists. X - patterns, Y - intents
        self.train_x = list(self.training[:,0])
        self.train_y = list(self.training[:,1])
        print("Training data created")

    def create_model(self):
        model = Sequential()
        model.add(Dense(128, input_shape=(len(self.train_x[0]),), activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(64, activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(len(self.train_y[0]), activation='softmax'))

        # compile model
        sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
        model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

        #fitting and saving the model
        np1 = np.array(self.train_x)
        np2 = np.array(self.train_y)

        hist = model.fit(np1, np2, epochs=200, batch_size=5, verbose=1)
        model.save('model.h5', hist)

        x = tf.keras.models.load_model('model.h5', compile=False)

        self.model = model

        print("model created")

if __name__ == '__main__':
    nlp = NLP()
    nlp.create_training_data()
    nlp.create_model()

