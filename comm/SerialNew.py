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
        
        time.sleep(2)
        
        # send 0 for ready
        self.ser.write("0")
        
        
        # # loop until the arduino tells us it is ready
        while not self.connected:
            print "connecting"
            serin = self.ser.read()
            if serin != -1 and int(serin) == 1:
                self.connected = True
                
        print "connected"
            
        self.isSendOver = True
        self.isReceiveOver = True
        self.canSendStart = False
        self.sendIndex = -1;
        self.receiveIndex = -1
        self.controlCode = -1
        self.componentId = -1
        self.data = -1
        self.sensorCount = -1
        self.actuatorCount = -1
        
        
        self.sensorValues = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        self.actuatorValues = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        self.speedValues = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        self.speak = Speak.Speak()
        self.speak.sayIntroduction()
        print "starting"
    
    
   
        
    def sendExpression(self):
        # 
        if self.isSendOver:
            print "told arduino"
            self.isSendOver = False
            self.sendIndex = -1
        
#         send control code and actuator count
        if self.sendIndex == -1:
            self.ser.write("4")
            self.ser.write(str(self.actuatorCount))
            
            if self.actuatorCount == 0:
                self.isSendOver = True
#        send the component id and data
        else:
#             find first value to send
            i = 0
            for i in range(self.sendIndex , 10):
                
                if self.actuatorValues[i] != -1:
                    self.ser.write(str(i))
                    self.ser.write(str(self.actuatorValues[i]).zfill(3)) 
                    self.ser.write(str(self.speedValues[i]).zfill(3))
                    self.sendIndex = i
            if(i == 10):
                self.isSendOver = True       
        
                
        
        
    def initializeMessage(self):
        self.isReceiveOver = False
        self.receiveIndex = -1
        self.controlCode = -1
        self.componentId = -1
        self.data = -1
        self.sensorCount = -1    
        
    
    def readInput(self):
        if(self.isReceiveOver):
            self.initializeMessage()
       
        inputData = self.ser.read()
#         print "-> " + str(inputData)
        
        if(self.controlCode == -1):
            self.controlCode = inputData
            print "got control code " + str(self.controlCode) + ";"
            
        elif self.controlCode == '3':
            if self.receiveIndex == -1:
#                 get count of sensors being sent
                self.sensorCount = 0
                while inputData != " ":
                    self.sensorCount = self.sensorCount * 10 + int(inputData)
#                     print "inputData " + str(inputData) + " -> " + str(self.sensorCount)
                    inputData = self.ser.read()
                print "sensorCount" + str(self.sensorCount)
                if self.sensorCount == 0:
                    self.isReceiveOver = True
                else:
                    self.receiveIndex = 0
            elif self.sensorCount > 0:
#                get component id
                self.componentId = 0
                while inputData != " ":
                    self.componentId = self.componentId * 10 + int(inputData)
                    inputData = self.ser.read()
#                 print "componentId " + str(self.componentId)
                
                
#                get data  
                self.data = 0              
                inputData = self.ser.read()
                while inputData != " ":
                    self.data = self.data * 10 + int(inputData)
                    inputData = self.ser.read()
               
#                 print "data " + str(self.data)
                        
                print "sensor input" + str(self.componentId) + " " + str(self.data) 

                self.sensorValues[self.componentId] = self.data
#                     self.processSensorInput(componentId, data)
                    
                self.receiveIndex = self.receiveIndex + 1
#                is sending over i.e. have we got all sensor values
                if self.receiveIndex == self.sensorCount:
                    self.isReceiveOver = True
           
            
    def endConnection(self):
    # # close the port and end the program
        self.ser.close()
        
        
    def processSensorInput(self):
        maxCapacitiveSensor = -1
        maxCapacitiveValue = -1
        for i in range(0, 20):
            data = self.sensorValues[i]
            if i >= 0 and i < 5:
                if data > 100:
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
        else:
            self.actuatorCount = 0
            
         
         
    def capacitiveTouch(self, componentId):
        capacitive = ['Right cheek' , 'Forehead' , 'Chin' , 'Left cheek' , 'Eye lids']
        print "touched" + capacitive[componentId]
        
        normalSpeed = 3
        
        if componentId == 0:
            print "happy"
            self.speak.saySentence("You have touched my right cheek. I'm happy.")
            self.actuatorCount = 7
            self.actuatorValues = np.array([180, 180, 180, -1, -1, -1, -180, 180, 180, 180])
            self.speedValues = np.array([normalSpeed, normalSpeed, normalSpeed, -1, -1, -1, normalSpeed, normalSpeed, normalSpeed, normalSpeed])
            
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
            self.actuatorCount = 7
            self.actuatorValues = np.array([0, 0, 0, -1, -1, -1, 0, 0, 0, 0 ])
            self.speedValues = np.array([normalSpeed, normalSpeed, normalSpeed, -1, -1, -1, normalSpeed, normalSpeed, normalSpeed, normalSpeed ])
        elif componentId == 1:
            self.speak.saySentence("You have touched my forehead. I'm angry.")
            print "anger"
#             self.sendExpression(2, 0)
#             self.sendExpression(3, 0)
#             self.sendExpression(4, 0)
#             self.sendExpression(5, 0)
#             self.sendExpression(6, 0)
            self.actuatorCount = 5
            self.actuatorValues = np.array([-1, -1, 0, 0, 0, 0, 0, -1, -1, -1])
            self.speedValues = np.array([-1, -1, normalSpeed, normalSpeed, normalSpeed, normalSpeed, normalSpeed, -1, -1, -1])
        elif componentId == 2:
            self.speak.saySentence("You have touched my chin. I'm surprised.")
            print "surprise"
#             self.sendExpression(0, 0)
#             self.sendExpression(1, 0)
#             self.sendExpression(7, 0)
#             self.sendExpression(8, 0)
#             self.sendExpression(9, 0)
            self.actuatorCount = 5
            self.actuatorValues = np.array([0, 0, -1, -1, -1, -1, -1, 0, 0, 0])
            self.actuatorValues = np.array([normalSpeed, normalSpeed, -1, -1, -1, -1, -1, normalSpeed, normalSpeed, normalSpeed])

        self.canSendStart = True
        


if __name__ == '__main__':
    serialComm = SerialCommunication()
    serialComm.initiateSequence();
#     serialComm.sendExpression(5, 180)
    while 1:
        serialComm.readInput()
        
        if serialComm.isReceiveOver:
            serialComm.processSensorInput()
     
        if serialComm.canSendStart:
            serialComm.sendExpression()
        
            
        
    
#     serialComm.sendExpression(3, 180)
#     serialComm.sendExpression(7, 180)
    
#     time.sleep(10)
    
#     serialComm.sendExpression(5, 0)
    
#     time.sleep(10)
#     serialComm.endConnection()
