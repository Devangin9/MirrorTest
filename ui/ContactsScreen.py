'''
Created on 08-May-2013

@author: Devangini
'''

import Tkinter as tk  # # Python 2.x
from Tkinter import StringVar
import ttk  # combobox
import VideoCall

class ContactsScreen:
    def openContactsScreen(self,topWindow):
        
        self.topWindow = topWindow
        self.frame = tk.Frame(topWindow)
        self.frame.grid()
        test_label = tk.Label(self.frame, text="Contacts : ")
        test_label.grid(row=1, column=0)
        
        
        self.contactsTable = ttk.Treeview(self.frame)
        # Inserted at the root, program chooses id:
        self.contactsTable.insert('', 'end', 'mom', text='mom')
         
        # Same thing, but inserted as first child:
        self.contactsTable.insert('', 0, 'Sriram', text='Sriram')
        
        # Treeview chooses the id:
        id = self.contactsTable.insert('', 'end', 'dad', text='dad')
        
        # Inserted underneath an existing node:
        #contactsTable.insert('widgets', 'end', text='Canvas')
        #contactsTable.insert(id, 'end', text='Tree')
        
       # contactsTable.column('status', width=1, anchor='center')
       # contactsTable.heading('status', text='status')
        
        
        #contactsTable.set('widgets', 'status', '12KB')
        #size = contactsTable.set('widgets', 'status')
        self.contactsTable['columns'] = ('status')
        
        self.contactsTable.column('status', width=100, anchor='center')
        self.contactsTable.heading('status', text='status')
        self.contactsTable.set('Sriram', 'status', 'online')
        #size = contactsTable.set('widgets', 'status')
        #contactsTable.insert('', 'end', text='Listbox', values=('15KB Yesterday mark'))
            
        #contactsTable.insert('', 'end', text='Listbox', values=('15KB Yesterday mark'))
        
        self.contactsTable.grid(row = 2, column = 0)
        
        
        
        call_button = tk.Button(self.frame, text="Call", \
                                     command=self.callPerson)
        call_button.grid(row=10, column=0)
            
        
        return self.frame

    def callPerson(self):
        print "calling sriram...."
        call = VideoCall.VideoCall();
        call.openCallWindow(self.topWindow);
