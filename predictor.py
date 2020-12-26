#!/usr/bin/env python3

import nltk
nltk.download('punkt')
nltk.download('wordnet')
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()

import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import load_model
import json
import random
import pickle

class Predictor:
    ERROR_THRESHOLD = 0.2

    def __init__(self):
        self.model = tf.keras.models.load_model("model.h5")
        self.intents = json.loads(open('intents.json').read())
        self.words = pickle.load(open('words.pkl','rb'))
        self.classes = pickle.load(open('classes.pkl','rb'))

    # cleans input by tokenizing words and making them lowercase
    def clean_input(self, phrase):
        tokenized_words = [lemmatizer.lemmatize(word.lower()) for word in nltk.word_tokenize(phrase)]
        return tokenized_words

    # given the words in our model, determines which words in 'phrase' are in the model
    def word_matrix(self, phrase):
        tokenized_words = self.clean_input(phrase)

        word_bag = [0] * len(self.words)
        for word in tokenized_words:
            for index, vocab_word in enumerate(self.words):
                if word == vocab_word:
                    word_bag[index] = 1

        return np.array(word_bag)

    def predict_intent(self, phrase):
        word_bag = self.word_matrix(phrase)
        results = self.model.predict(np.array([word_bag]))[0]
        print(results)

        results = [[index, res] for index,res in enumerate(results) if res > self.ERROR_THRESHOLD]

        # higher probability results first
        results.sort(key=lambda x: x[1], reverse=True)

        formatted_results = []

        for result in results:
            formatted_results.append({
                "intent": self.classes[result[0]],
                "probability": str(result[1])
            })

        return formatted_results

    
