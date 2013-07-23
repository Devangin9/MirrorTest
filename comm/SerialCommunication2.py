'''
Created on 17-May-2013

@author: Devangini
'''


# # import the serial library
import serial
import time


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
    
    
    def sendExpression(self, actuatorId, angle):
        # # Tell the arduino to blink!
        # for i in range(0, 9):
        self.ser.write("4")
        self.ser.write(str(actuatorId))
        self.ser.write(str(angle).zfill(3))
        
        
        print "told arduino"
    
    def readInput(self):
        # # Wait until the arduino tells us it 
        # # is finished blinking
        print "inside read"
        componentId = 0
        data = 0
        while 1:
            inputData = self.ser.read()
#             print inputData
#             if inputData == '0':
#         #     ser.read()
#                 print "arduino acknowledged"
            if inputData == '3':
#                 print "sensor data "
                try:
                    inputData = int(self.ser.read()) 
    #                 print inputData
                    while inputData != 27:
                        componentId = componentId * 10 + (inputData)
                        try:
                            inputData = int(self.ser.read()) 
                        except ValueError:
                            self.ser.read()
                            break
    #                     print inputData
#                     print "component id " + str(componentId)
                    inputData = int(self.ser.read())
    #                 print inputData
                    while inputData != 27:
                        data = data * 10 + (inputData)
                        try:
                            inputData = int(self.ser.read()) 
                        except ValueError:
                            break
    #                     print inputData
#                     print "sensor input" + str(componentId) + " " +str(data) 
 
                    self.processSensorInput(componentId, data)
                    
#                     break
                
                
                     
                except ValueError:
#                     break
                    continue  
                componentId =0
                data = 0
                
#                 return
                # take next input
            
    def endConnection(self):
    # # close the port and end the program
        self.ser.close()
        
        
    def processSensorInput(self, componentId, data):
        if componentId >= 0 and componentId < 5:
            if data > 90:
                print "capacitive touched " + str(componentId) + " " + str(data)
                self.capacitiveTouch(componentId)
        elif componentId >= 5 and componentId < 17:
            if data > 100:
                print "piezo touched " + str(componentId) + " " + str(data) 
        elif componentId >= 17 and componentId < 19:
            if data > 100:
                print "qtc touched " + str(componentId) + " " + str(data)    


    def capacitiveTouch(self, componentId):
        capacitive = ['Right cheek' , 'Forehead' , 'Chin' , 'Left cheek' , 'Eye lids']
        print "touched" + capacitive[componentId]
        
        if componentId == 0:
            print "happy"
            self.sendExpression(0, 180)
            self.sendExpression(1, 180)
            self.sendExpression(7, 180)
            self.sendExpression(8, 180)
            self.sendExpression(9, 180)
            
        elif componentId == 3:
            self.sendExpression(2, 180)
            self.sendExpression(3, 180)
            self.sendExpression(4, 180)
            self.sendExpression(5, 180)
            self.sendExpression(6, 180)
            
        elif componentId == 1:
            print "anger"
            self.sendExpression(2, 0)
            self.sendExpression(3, 0)
            self.sendExpression(4, 0)
            self.sendExpression(5, 0)
            self.sendExpression(6, 0)
            
        elif componentId == 2:
            print "surprise"
            self.sendExpression(0, 0)
            self.sendExpression(1, 0)
            self.sendExpression(7, 0)
            self.sendExpression(8, 0)
            self.sendExpression(9, 0)
            
        self.readInput()
        


if __name__ == '__main__':
    serialComm = SerialCommunication()
    serialComm.initiateSequence();
#     serialComm.sendExpression(5, 180)
    serialComm.readInput()
#     serialComm.sendExpression(3, 180)
#     serialComm.sendExpression(7, 180)
    
#     time.sleep(10)
    
#     serialComm.sendExpression(5, 0)
    
#     time.sleep(10)
#     serialComm.endConnection()
