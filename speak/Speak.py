'''
Created on 09-May-2013

@author: Devangini
'''
'''
Created on Apr 28, 2013

@author: sriram
'''
# from googlemaps import *

import pyttsx
import time

# import googlemaps2
class Speak:
    

    def setup(self):
        self.engine = pyttsx.init()
        self.engine.setProperty('rate', 130)
    def sayIntroduction(self):
        self.setup()
        
        
    # start = 'southampton university, uk'
    # end   = 'SO182NU, UK'
        speak = "Charlie is happy to be at service."
        self.engine.say(speak)
        self.engine.runAndWait()
        time.sleep(2);
        
    #     try:
    #         dirs  = gmaps.directions(start, end)
    #     except:
        
#         name = "Shreeraaaam"
#         caller = "Devangeenee"
#         
#         speak = "Hi, " + name + ". This is " + caller + "."
#         self.engine.say(speak)
#         self.engine.runAndWait()
#         time.sleep(10);
        
    def saySentence(self, sentence):
        self.engine.say(sentence)
        self.engine.runAndWait()


if __name__ == '__main__':
    speak = Speak()
    speak.setup()
    speak.saySentence("hello, everyone.")
    speak.saySentence("my name is charlie.")
