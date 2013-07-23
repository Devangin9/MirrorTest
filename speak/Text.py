'''
Created on 10-May-2013

@author: Devangini
'''
import time
import speech

def blockListen():
    while True:
        phrase = speech.input()
        speech.say("You said %s" % phrase)
        print "You said " + phrase
        if phrase == "turn off":
            break

def response(phrase, listener):
    speech.say("You said %s" % phrase)
    print phrase
    if phrase == "turn off":
        listener.stoplistening()
        
def unblockListen():

    listener = speech.listenforanything(response)

# Your program can do whatever it wants now, and when a spoken phrase is heard,
# response() will be called on a separate thread.

    while listener.islistening():
        time.sleep(1)
        print "Still waiting..."
        
        
unblockListen()