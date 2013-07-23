'''
Created on 17-May-2013

@author: Devangini
'''


# # import the serial library
import serial
import time
import numpy as np
from speak import Speak

class SerialCommunication:
    
   
    
    def initiateSequence(self):
        # # Boolean variable that will represent 
        # # whether or not the arduino is connected
        self.connected = False
        
        # # open the serial port that your ardiono 
        # # is connected to.
        self.ser = serial.Serial("COM8", 9600)
        
        # # loop until the arduino tells us it is ready
        while not self.connected:
            serin = self.ser.read()
            self.connected = True
            print "connecting"
            
        self.sensorValues = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        self.speak = Speak.Speak()
        self.speak.sayIntroduction()
    
    
    def sendExpression1(self, actuatorId, angle):
        # # Tell the arduino to blink!
        # for i in range(0, 9):
        self.ser.write("4")
        self.ser.write(str(actuatorId))
        self.ser.write(str(angle).zfill(3))
        
        
        print "told arduino"
        
    def sendExpression(self, actuatorCount, actuatorValues):
        # # Tell the arduino to blink!
        # for i in range(0, 9):
        self.ser.write("4")
        self.ser.write(str(actuatorCount))
        for i in range(0, 10):
            if actuatorValues[i] != -1:
                self.ser.write(str(i))
                self.ser.write(str(actuatorValues[i]).zfill(3))        
        print "told arduino"
    
    def readInput(self):
        # # Wait until the arduino tells us it 
        # # is finished blinking
#         print "inside read"
        componentId = 0
        data = 0
        sensorCount = 0
        while 1:
            inputData = self.ser.read()
#             print inputData
#             if inputData == '0':
#         #     ser.read()
#                 print "arduino acknowledged"
            if inputData == '3':
#                 print "sensor data "
               
                inputData = self.ser.read() 
#                 print inputData
#                 print "x" + str((inputData.decodehex"))) + "x"
                while inputData != " ":
                    sensorCount = sensorCount * 10 + int(inputData)
                    print sensorCount
                    inputData = self.ser.read() 

#                 print "count  " + str(sensorCount)
                for i in range(0, sensorCount):
                    inputData = self.ser.read()
    #                 print inputData
                    while inputData != " ":
                        componentId = componentId * 10 + int(inputData)
                        inputData = self.ser.read() 
                        
#                     print "component id " + str(componentId)
                    inputData = self.ser.read()
    #                 print inputData
                    while inputData != " ":
                        data = data * 10 + int(inputData)
                        inputData = self.ser.read()
                        
#                     print "sensor input" + str(componentId) + " " +str(data) 

                    self.sensorValues[componentId] = data
#                     self.processSensorInput(componentId, data)
                    
                    componentId =0
                    data = 0
                    
#                     break
                if sensorCount != 0:
                    serialComm.processSensorInput()
                     
#                 except ValueError:
# #                     break
#                     continue  
                sensorCount = 0
                break
            
#                 return
                # take next input
            
    def endConnection(self):
    # # close the port and end the program
        self.ser.close()
        
        
    def processSensorInput(self):
        maxCapacitiveSensor = -1
        maxCapacitiveValue = -1
        for i in range(0, 20):
            data =  self.sensorValues[i]
            if i >= 0 and i < 5:
                if data > 90:
                    print "capacitive touched " + str(i) + " " + str(data)
                    if data > maxCapacitiveValue:
                        maxCapacitiveValue = data
                        maxCapacitiveSensor = i
                    
#             elif i >= 5 and i < 17:
#                 if data > 100:
#                     print "piezo touched " + str(i) + " " + str(data) 
#             elif i >= 17 and i < 19:
#                 if data > 100:
#                     
#                     print "qtc touched " + str(i) + " " + str(data)    

        if maxCapacitiveSensor != -1:
            self.capacitiveTouch(maxCapacitiveSensor)
         
         
    def capacitiveTouch(self, componentId):
        capacitive = ['Right cheek' , 'Forehead' , 'Chin' , 'Left cheek' , 'Eye lids']
        print "touched" + capacitive[componentId]
        
        if componentId == 0:
            print "happy"
            self.speak.saySentence("You have touched my right cheek. I'm happy.")
            self.sendExpression(7, [180, 180, 180, -1, -1, -1, -180, 180, 180, 180])
#             self.sendExpression(0, 180)
#             self.sendExpression(1, 180)
#             self.sendExpression(7, 180)
#             self.sendExpression(8, 180)
#             self.sendExpression(9, 180)
            
        elif componentId == 3:
            self.speak.saySentence("You have touched my left cheek. I'm sad.")
#             self.sendExpression(2, 180)
#             self.sendExpression(3, 180)
#             self.sendExpression(4, 180)
#             self.sendExpression(5, 180)
#             self.sendExpression(6, 180)
            self.sendExpression(7, [0, 0, 0, -1, -1, -1, -0, 0, 0, 0 ])
        elif componentId == 1:
            self.speak.saySentence("You have touched my forehead. I'm angry.")
            print "anger"
#             self.sendExpression(2, 0)
#             self.sendExpression(3, 0)
#             self.sendExpression(4, 0)
#             self.sendExpression(5, 0)
#             self.sendExpression(6, 0)
            self.sendExpression(5, [-1, -1, 0, 0, 0, 0, 0, -1, -1, -1])
        elif componentId == 2:
            self.speak.saySentence("You have touched my chin. I'm surprised.")
            print "surprise"
#             self.sendExpression(0, 0)
#             self.sendExpression(1, 0)
#             self.sendExpression(7, 0)
#             self.sendExpression(8, 0)
#             self.sendExpression(9, 0)
            self.sendExpression(5, [0, 0, -1, -1, -1, -1, -1, 0, 0, 0])
            
        self.readInput()
        


if __name__ == '__main__':
    serialComm = SerialCommunication()
    serialComm.initiateSequence();
#     serialComm.sendExpression(5, 180)
    while 1:
        serialComm.readInput()
    
#     serialComm.sendExpression(3, 180)
#     serialComm.sendExpression(7, 180)
    
#     time.sleep(10)
    
#     serialComm.sendExpression(5, 0)
    
#     time.sleep(10)
#     serialComm.endConnection()
