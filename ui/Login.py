'''
Created on 08-May-2013

@author: Devangini
'''
import Tkinter as tk  # # Python 2.x
from Tkinter import StringVar
import ttk  # combobox
import ContactsScreen


class Login():
    def __init__(self, top):
        self.top = top
        self.top.geometry("+10+10")
        self.frame = tk.Frame(self.top)
        self.frame.grid()
        test_label = tk.Label(self.frame, text="Username : ")
        test_label.grid(row=1, column=0)
        
        usernamesVar = StringVar()
        self.usernames = ttk.Combobox(self.frame)
        self.usernames['values'] = ('Devangini', 'Sriram')
        self.usernames.current(0)
        self.usernames.grid(column=0, row=2)
        
        self.password = tk.Entry(self.frame)
        self.password.pack()
        #password.delete(0, END)
        self.password.insert(0, "a default value")
        self.password.grid(column=0, row=3)
        
        login_button = tk.Button(self.frame, text="Login", \
                                 command=self.loginUser)
        login_button.grid(row=4, column=0)
        
        
        destroy_button = tk.Button(self.frame, text="Destroy Frame", \
                                 command=self.destroy)
        destroy_button.grid(row=10, column=0)
        exit_button = tk.Button(self.top, text="Exit", command=top.quit)
        exit_button.grid(row=10, column=0)
        
        
        
    def destroy(self):
        
        self.frame.destroy()
#         self.new_toplevel=tk.Toplevel(self.top, takefocus=True)
#         self.new_toplevel.geometry("+50+50")
#         self.new_toplevel.grid()
#         lbl=tk.Label(self.new_toplevel, text="New Toplevel")
#         lbl.grid()
        
        
        self.frame = tk.Frame(self.top)
        # self.frame.geometry("+50+50")
        self.frame.grid()
        lbl = tk.Label(self.frame, text="New Toplevel")
        lbl.grid()
        
    def loginUser(self):
        
        #check the password
        passwordValue = self.password.get()
        if(self.usernames.get() == "Devangini" and passwordValue == "hello"):
        
            self.frame.destroy()
    #         self.new_toplevel=tk.Toplevel(self.top, takefocus=True)
    #         self.new_toplevel.geometry("+50+50")
    #         self.new_toplevel.grid()
    #         lbl=tk.Label(self.new_toplevel, text="New Toplevel")
    #         lbl.grid()
            
            mainScreen = ContactsScreen.ContactsScreen();
            self.frame = mainScreen.openContactsScreen(self.top)
            # self.frame.geometry("+50+50")
            self.frame.grid()
        
        else:
            dialog = tk.Toplevel(self.frame)
            test_label = tk.Label(dialog, text="Password wrong")
            test_label.grid(row=1, column=0)
        
        
        
root = tk.Tk()
login = Login(root)
root.mainloop()
