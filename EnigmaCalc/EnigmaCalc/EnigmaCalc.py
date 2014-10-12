#This file is part of EnigmaCalc
#Team Enigma - RPI SDD - Fall 2014

from pylab import * 
from Tkinter import *

root = Tk()



def callback():
    x = arange(-10, 10, .01)
    
    function = e.get().replace("^", "**")
    y = eval(function) #Very very evil. We need to do this a lot better; should be a way to only
                      #whitelist certain functions 

                      #sinx instead of sin(x) 
                      #Maybe just add '(' x ')' parenthesis to all x's?
    print "Trying to Graph!"
    plot(x,y)
    show()

# create window contents as children to root...
w = Label(text="Input Function\n Y = ")
w.pack()
e = Entry()
e.pack()

e.delete(0, END)
e.insert(0, "")
b = Button(text="Graph!", command=callback)
b.pack()

root.mainloop()
