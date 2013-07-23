'''
Created on 17-May-2013

@author: Devangini
'''


## import the serial library
import serial

## Boolean variable that will represent 
## whether or not the arduino is connected
connected = False

## open the serial port that your ardiono 
## is connected to.
ser = serial.Serial("COM8", 9600)

## loop until the arduino tells us it is ready
while not connected:
    serin = ser.read()
    connected = True
    print "connecting"



## Wait until the arduino tells us it 
## is finished blinking
while 1:
    input = ser.read()
#     ser.read()
    print "arduino acknowledged" + str(input)

## close the port and end the program
ser.close()