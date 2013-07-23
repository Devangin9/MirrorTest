'''
Created on Apr 28, 2013

@author: sriram
'''

import Speak_dir


# Command = 'goto waterloo station,uk'
def call(Command):
    comm = Command[:4]
    if comm == 'goto':
        start = 'Southampton University, Southampton, UK'
    
        end   = Command[5:]
        print end
        Speak_dir.get_direction(start, end)
# elif comm == 'Read':
#     