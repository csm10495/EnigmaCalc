#This file is part of EnigmaCalc
#Team Enigma - RPI SDD - Fall 2014

from pylab import * 
from Tkinter import *

root = Tk()



def callback():
    x = arange(-10, 10, .01)
    
    function = e.get().replace("^", "**")
    safe_list = ['acos', 'asin', 'atan', 'atan2', 'ceil', 'cos', 'cosh', 'degrees', 'e', 'exp', 'fabs', 'floor', 'fmod', 'frexp', 'hypot', 'ldexp', 'log', 'log10', 'modf', 'pi', 'pow', 'radians', 'sin', 'sinh', 'sqrt', 'tan', 'tanh', '+', '-', '*', '/', '**', 'x']
    safe_dict = dict([ (k, locals().get(k, None)) for k in safe_list ])
    y = eval(function, {"__builtins__":None}, safe_dict) 

                      #also need to handle simple user errors like using ^
                      #instead of **
                      #sinx instead of sin(x) 
                      #Maybe just add '(' x ')' parenthesis to all x's?
    print "Trying to Graph!"
    plot(x,y)
    show()

# create window contents as children to root...
w = Label(text = "Input Function\n Y = ")
w.pack()
e = Entry()
e.pack()

e.delete(0, END)
e.insert(0, "")
b = Button(text="Graph!", command=callback)
b.pack()

root.mainloop()
