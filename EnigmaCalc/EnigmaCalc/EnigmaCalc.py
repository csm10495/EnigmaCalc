#This file is part of EnigmaCalc
#Team Enigma - RPI SDD - Fall 2014


import pylab     #graphing library, part of matplotlib
import Tkinter   #GUI library, standard Python


class Function:
    def __init__(self, function_text = ""):
        self.function_text = function_text
    
    def formatFunction(self):       
        #User can input sin(x) or Sin(x), etc. - Luke
        self.function_text = self.function_text.replace("^", "**").replace("S", "s").replace("C", "c").replace("T", "t")
        self.function_text = self.function_text + "+x-x"
        
    
class Gui:
    
    def __init__(self):
        self.safe_dict = {}
        self.safe_list= []
        self.root = None
   
    def startUp(self):
        self.safe_dict = self.getSafeDict()
    
        # create window contents
        root = Tkinter.Tk()
    
        #set window title
        root.wm_title("EC")
    
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
        b = Tkinter.Button(root, text="Graph!", command = lambda: self.graph(graph_entry.get(), self.safe_dict))
        b.pack()
        
        #mainloop needs to be run
        #Every GUI is a loop...
        root.mainloop()
        

    #graphs a function by grabbing from e.get()
    def graph(self, function_text, safe_dict):
        x = pylab.arange(-10, 10, .01)
        safe_dict['x'] = locals().get('x')
    

        function = Function(function_text)
        function.formatFunction()
        
        print "What? " + function.function_text
    
        y = eval(function.function_text, {"__builtins__":None}, safe_dict) 
    
        #sinx instead of sin(x) 
        #Maybe just add '(' x ')' parenthesis to all x's?
    
        print "Graphing: Y =", function_text
        pylab.plot(x, y, label = ("y = " + function_text))
    
        #make the graph legend appear
        pylab.legend(loc='upper right')
    
        pylab.show()

    #call this once!
    #gets a dictionary of functions allowed to be called by eval
    def getSafeDict(self):
        safe_list = ['sin', 'cos', 'tan'] #todo -> add more functions from pylab to this list
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
