#This file is part of EnigmaCalc
#Team Enigma - RPI SDD - Fall 2014


import pylab     #graphing library, part of matplotlib
import Tkinter   #GUI library, standard Python


#call this once!
#gets a dictionary of functions allowed to be called by eval
def getSafeDict():
    safe_list = ['sin', 'cos', 'tan'] #todo -> add more functions from pylab to this list
    safe_dict = dict((k, getattr(pylab, k)) for k in safe_list)

    # ading some more things to safe_dict that are not in pylab
    # we can't add x yet because it isn't set
    safe_dict['+'] = locals().get('+')
    safe_dict['-'] = locals().get('-')
    safe_dict['/'] = locals().get('/')
    safe_dict['*'] = locals().get('*')
    safe_dict['**'] = locals().get('**')

    return safe_dict


#graphs a function by grabbing from e.get()
def graph(function_text, safe_dict):
    x = pylab.arange(-10, 10, .01)
    safe_dict['x'] = locals().get('x')

    function = function_text.replace("^", "**")
    function = function + "+x-x"

    y = eval(function, {"__builtins__":None}, safe_dict) 

    #sinx instead of sin(x) 
    #Maybe just add '(' x ')' parenthesis to all x's?

    print "Graphing: Y =", function_text
    pylab.plot(x, y, label = function_text)

    #make the graph legend appear
    pylab.legend(loc='upper right')

    pylab.show()


#function that needs to be run for the program to start (like a main)
def startUp():
    safe_dict = getSafeDict()



    # create window contents
    root = Tkinter.Tk()

    #instruction text
    instr = Tkinter.Label(root, text = "Input Function")
    instr.pack()

    #Y = text
    yequals = Tkinter.Label(root, text = "Y = ")
    yequals.pack(side = Tkinter.LEFT)

    #inputbox for function
    graph_entry = Tkinter.Entry(root, text = "")
    graph_entry.pack(side = Tkinter.LEFT)

    #graph button
    b = Tkinter.Button(root, text="Graph!", command = lambda: graph(graph_entry.get(), safe_dict))
    b.pack()
    
    #mainloop needs to be run
    #Every GUI is a loop...
    root.mainloop()


startUp()