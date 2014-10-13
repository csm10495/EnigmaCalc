#This file is part of EnigmaCalc
#Team Enigma - RPI SDD - Fall 2014

import pylab 
from Tkinter import *

root = Tk()


def callback():
    x = pylab.arange(-10, 10, .01)
    
    function = e.get().replace("^", "**")
    function = function + "+x-x"
    safe_list = ['sin', 'cos', 'tan'] #todo -> add more functions from pylab to this list
    safe_dict = dict((k, getattr(pylab, k)) for k in safe_list)

    # ading some more things to safe_dict that are not in pylab
    safe_dict['x'] = x
    safe_dict['+'] = locals().get('+')
    safe_dict['-'] = locals().get('-')
    safe_dict['/'] = locals().get('/')
    safe_dict['*'] = locals().get('*')
    safe_dict['**'] = locals().get('**')
    #

    y = eval(function, {"__builtins__":None}, safe_dict) 


    #sinx instead of sin(x) 
    #Maybe just add '(' x ')' parenthesis to all x's?

    print "Trying to Graph!"
    pylab.plot(x,y)
    pylab.show()

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
