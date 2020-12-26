#!/usr/bin/env python3

import speech_recognition as sr
from predictor import Predictor
import pyttsx3


class Cinnamon:
    def __init__(self):
        self.r = sr.Recognizer()
        self.mic = sr.Microphone(device_index=0)
        self.predictor = Predictor()


        self.engine=pyttsx3.init('nsss')
        self.voices=self.engine.getProperty('voices')

    def select_voice(self):
        temp_engine = self.engine

        if self.voices is not None:
            for voice in self.voices:
                print("------------------------")
                print("ID: %s" %voice.id) 
                print("Name: %s" %voice.name) 
                print("Gender: %s" %voice.gender) 
                print("Languages Known: %s" %voice.languages) 
                temp_engine.setProperty('voice',str(voice.id))
                self.speak(f"Hello I am {voice.name}", engine=temp_engine)
                self.speak("Would you like me to be your personal assistant? Yes or No?", engine=temp_engine)

                try:
                    response = self.process_audio()
                    print(f"You said {response}")
                    if "yes" in response:
                        self.engine = temp_engine
                        return
                    if "quit" in response or "exit" in response:
                        return

                    self.speak("Ouch. That's harsh.", engine=temp_engine)

                except Exception as e:
                    print("Oops! Didn't get that!")
                

    def speak(self, sentence, engine=None):
        try:
            if engine == None:
                engine = self.engine

            engine.say(sentence)
            engine.runAndWait()
        except Exception as e:
            print("It appears I have forgotten how to speak! Sorry!")

    def process_audio(self):
        
        with self.mic as source:
            self.r.adjust_for_ambient_noise(source)
            audio = self.r.listen(source, timeout=5)
            print("taking in audio")

        response = "" if audio is None else self.r.recognize_google(audio)
        return response

    def chat(self):
        response = ""
        while not ('quit' in response or 'exit' in response):
            print("start speaking!")
            self.speak("start speaking")

            try:
                response = self.process_audio()
                print(f"You said {response}")
                self.speak(response)
                print(self.predictor.predict_intent(response))

                if "change voice" in response:
                    self.select_voice()

            except Exception as e:
                print("Oops! Didn't get that!")

if __name__ == "__main__":
    cinnamon = Cinnamon()
    cinnamon.chat()