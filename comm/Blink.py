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

## Tell the arduino to blink!
# for i in range(0, 9):
ser.write("4")
ser.write("1")
ser.write("4")
ser.write("000")


print "told arduino"

## Wait until the arduino tells us it 
## is finished blinking
# while ser.read() == '0':
# #     ser.read()
#     print "arduino acknowledged"

## close the port and end the program
ser.close()