'''
Created on 09-May-2013

@author: Devangini
'''
import Tkinter as tk
from PIL import ImageTk, Image

path = 'E:\python workspace\CharlieCode\emoticon_smile.png'

root = tk.Tk()
img = ImageTk.PhotoImage(Image.open(path))
# panel = tk.Label(root, image = img)
# panel.pack(side = "bottom", fill = "both", expand = "yes")
smileButton = tk.Button(root, image = img)
smileButton.grid(row=0, column=0)
labelName = tk.Label(root, text="Hello, world!")
labelName.grid(column = 0, row = 3)
root.mainloop()