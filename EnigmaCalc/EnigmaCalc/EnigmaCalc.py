#This file is part of EnigmaCalc
#Team Enigma - RPI SDD - Fall 2014

import matplotlib
matplotlib.use('TkAgg')

import pylab        #graphing library, part of matplotlib
import Tkinter      #GUI library, standard Python
import tkMessageBox #Used to make the error box

class Function:
    def __init__(self, function_text = ""):
        self.function_text = function_text
    
    def formatFunction(self):       
        #All input is converted to lower so no caps matter
        self.function_text = self.function_text.replace("^", "**").lower()

        #add a * between a number and letter (ex: 2x)
        #or x and a letter (ex: xsin)
        for i in range(len(self.function_text)):
            if self.function_text[i].isdigit() and self.function_text[i+1].isalpha()\
                or self.function_text[i]== 'x' and self.function_text[i+1].isalpha():
                self.function_text = self.function_text[:i+1]+ '*' + self.function_text[i+1:]
        
        self.function_text = self.function_text + "+x-x"

        self.function_text = self.function_text.replace("csc", "1/sin")
        self.function_text = self.function_text.replace("sec", "1/cos")
        self.function_text = self.function_text.replace("cot", "1/tan")

class Gui:
    
    def __init__(self):
        self.safe_dict = {}
        self.safe_list= []
        self.root = None
        
    def startUp(self):
        self.safe_dict = self.getSafeDict()
    
        # create window contents
        self.root = Tkinter.Tk()
    
        #set window title
        self.root.wm_title("EC")
    
        #instruction text
        instr = Tkinter.Label(self.root, text = "Input Function")
        instr.pack()
    
        #Y = text
        yequals = Tkinter.Label(self.root, text = "Y = ")
        yequals.pack(side = Tkinter.LEFT)
    
        #inputbox for function
        self.graph_entry = Tkinter.Entry(self.root, text = "")
        self.graph_entry.pack(side = Tkinter.LEFT)
        self.graph_entry.focus_set()     #focus on this entry
    
        #graph button
        self.b = Tkinter.Button(self.root, text="Graph!", command = lambda: self.graph(self.graph_entry.get(), self.safe_dict))
        self.b.pack()

        #enter calls self.graph
        self.root.bind("<Return>", lambda event: self.EnterKey())

        #clear button
        self.c = Tkinter.Button(self.root, text="Clear", command = lambda: self.graph_entry.delete(0,Tkinter.END))
        self.c.pack(side = Tkinter.RIGHT)
        
        #mainloop needs to be run
        #Every GUI is a loop...
        self.root.mainloop()

    def EnterKey(self):
        if self.root.focus_get() == self.c:
            self.graph_entry.delete(0,Tkinter.END)
        elif self.root.focus_get() == self.graph_entry or self.b:
            self.graph(self.graph_entry.get(), self.safe_dict)
        

    #graphs a function by grabbing from e.get()
    def graph(self, function_text, safe_dict):
            
        x = pylab.arange(-10, 10, .01)
        safe_dict['x'] = locals().get('x')
    

        function = Function(function_text)
        function.formatFunction()
        
        print "What? " + function_text
    
        try:
            y = eval(function.function_text, {"__builtins__":None}, safe_dict) 
    
            #sinx instead of sin(x) 
            #Maybe just add '(' x ')' parenthesis to all x's?
    
            print "Graphing: Y =", function_text
            pylab.plot(x, y, label = ("y = " + function_text))
    
            #make the graph legend appear
            pylab.legend(loc='upper right')

            pylab.show()
            
        except:
            print function_text, "is not a valid function"

            tkMessageBox.showinfo("Error", function_text + " is not a valid function")
            
    #call this once!
    #gets a dictionary of functions allowed to be called by eval
    def getSafeDict(self):
        safe_list = ['sin', 'cos', 'tan', 'arcsin', 'arcsinh', 'sinh', 'arccos', 'arccosh', 'cosh', 'arctan', 'arctanh', 'tanh', 'e', 'log', 'log2', 'log10', 'sqrt', 'pi']
        safe_dict = dict((k, getattr(pylab, k)) for k in safe_list)
    
        # adding some more things to safe_dict that are not in pylab
        # we can't add x yet because it isn't set
        safe_dict['+'] = locals().get('+')
        safe_dict['-'] = locals().get('-')
        safe_dict['/'] = locals().get('/')
        safe_dict['*'] = locals().get('*')
        safe_dict['**'] = locals().get('**')
    
        return safe_dict
    
def main():
    GUI = Gui()
    GUI.startUp()
    
main()
