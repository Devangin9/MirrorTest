'''
Created on 12-Apr-2013

@author: Devangini

PyAudio Example: Make a wire between input and output (i.e., record a
few samples and play them back immediately).

This is the callback (non-blocking) version.

http://people.csail.mit.edu/hubert/pyaudio/#examples
'''
# http://www.swharden.com/blog/2011-07-09-sound-card-microcontrollerpc-communication/
import pyaudio
import time

WIDTH = 2
CHANNELS = 2
RATE = 44100


def recordAndPlay():
    p = pyaudio.PyAudio()
    
    def callback(in_data, frame_count, time_info, status):
        return (in_data, pyaudio.paContinue)
    
    stream = p.open(format=p.get_format_from_width(WIDTH),
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    output=True,
                    stream_callback=callback)
    
    stream.start_stream()
    
    while stream.is_active():
        time.sleep(0.1)
    
    stream.stop_stream()
    stream.close()
    
    p.terminate()
    
if __name__=="__main__":
    recordAndPlay()