from Tkinter import *
import Image
import demo


global Command
class Application(Frame):
    

    def createWidgets(self):
#         self.text = Text(self, bd = 10, height = 5)
#         self.text.pack({"side": "top"})

        self.textField = Entry(self)
        
        self.textField.delete(0, END)
        self.textField.insert(0, "goto wessex Ln, southampton, uk")
        self.textField.pack()
        
        def search():
            print type(self.textField)
            print self.textField.get()
    #         Command = textbox.get(1, 30)
            demo.call(self.textField.get())

#         self.go_there = Button(self)
#         self.go_there["text"] = "Goooo!",
#         self.go_there["command"] = self.search(self.textField.get())

        self.go_there = Button(self, text="Go", width = 100, command = search)
        
        self.go_there.pack({"side": "bottom"})

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

root = Tk()
app = Application(master=root)
app.master.title('3-thd EyE')
app.master.maxsize(1000, 800)
app.mainloop()
root.destroy()