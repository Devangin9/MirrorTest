'''
Created on 16-May-2013

@author: Devangini
'''
class CommunicationMessage:
    terminalCharacter = "-1"
    controlNumber = 0
    data = ""
    
    def send(self):
        return self.controlNumber + self.data + self.terminalCharacter