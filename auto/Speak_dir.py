'''
Created on Apr 28, 2013

@author: sriram
'''
# from googlemaps import *
from auto.googlemaps2 import GoogleMaps 
import pyttsx
import time

# import googlemaps2
def get_direction(start, end):
    engine = pyttsx.init()
    engine.setProperty('rate', 130)
    gmaps = GoogleMaps()
    
# start = 'southampton university, uk'
# end   = 'SO182NU, UK'
    speak = "One is happy to be at service"
    engine.say(speak)
    engine.runAndWait()
    time.sleep(2);
    
    try:
        dirs  = gmaps.directions(start, end)
    except:
        None;
  #  dirs = None
#     print dirs
    try:
        t  = dirs['Directions']['Duration']['seconds']
        
        t = t / 60
    except:
        t = 5
    try:
        dist  = dirs['Directions']['Distance']['meters']
        print dist
    except:
        dist = 1000
    speak = "The destination is approximately "+str(dist)+"meters away and it will approximately take " +str(t)+"minutes to reach."
    engine.say(speak)
    engine.runAndWait()
    time.sleep(2)
    
    print dirs
    
    route = dirs['Directions']['Routes'][0]
#     print route
    for step in route['Steps']:
#     print step['Point']['coordinates'][1::-1]
        d = step['Distance']['meters']
#         if d == 0:
#             d = 2
#         else:
#             d = d+2
        s = step['Duration']['seconds']
#         if s == 0:
#             s = 3
#         else:
#             s = s+1
        des = step['descriptionHtml']
        
        
        des = des.replace("<b>","")
        des = des.replace("</b>","")
        try:
            des = des[:des.index('<div ')]
        except ValueError:
#             print "Oops!  That was no valid number.  Try again..."
            None
        des2 = des
#         take  the div off first
        if des2.find("<div>") != - 1:
#             index1 = des2.find("<div>")
#             index2 = des2.find("</div>")
            des2 = des2.replace("<div>(.*)</div>","")
#          while des2.contains("<b>") :
            
#         print des
#         print des2
        
        speak = "Please "+str(des)+" and walk "+str(d)+" meters"
        engine.say(speak)
        engine.runAndWait()
        time.sleep(s);

    