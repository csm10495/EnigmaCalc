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

        #add support for several common user shortcuts
        strlen = len(self.function_text)-1
        i=0
        while i < strlen:
            if self.function_text[i].isdigit() and self.function_text[i+1].isalpha()\
            or self.function_text[i]== 'x' and self.function_text[i+1].isalpha():
                self.function_text = self.function_text[:i+1]+ '*' + self.function_text[i+1:]
                strlen += 1
            i+=1
        
        
        self.function_text = self.function_text + "+x-x"

        self.function_text = self.function_text.replace("csc", "1/sin")
        self.function_text = self.function_text.replace("sec", "1/cos")
        self.function_text = self.function_text.replace("cot", "1/tan")

class Gui:
    
    def __init__(self):
        self.safe_dict = {}
        self.safe_list= []
        self.root = None
        self.is_deg = False
        
    def startUp(self):
        self.safe_dict = self.getSafeDict()
    
        # create window contents
        self.root = Tkinter.Tk()
    
        #set window title
        self.root.wm_title("Enigma Calc")
        self.root.minsize(width=250, height = 50)
    
        #instruction text
        instr = Tkinter.Label(self.root, text = "Input Function")
        instr.pack()
    
        #Y = text
        y_equals = Tkinter.Label(self.root, text = "Y = ")
        y_equals.pack(side = Tkinter.LEFT)
    
        #inputbox for function
        self.graph_entry = Tkinter.Entry(self.root, text = "")
        self.graph_entry.pack(side = Tkinter.LEFT)
        self.graph_entry.focus_set()     #focus on this entry
    
        #graph button
        self.b = Tkinter.Button(self.root, text="Graph!", command = lambda: self.graph(self.graph_entry.get(), self.x_axis_min.get(), self.x_axis_max.get(), self.safe_dict))
        self.b.pack(side = Tkinter.LEFT)

        #enter calls self.graph
        self.root.bind("<Return>", lambda event: self.EnterKey())

        #clear button
        self.c = Tkinter.Button(self.root, text="Clear", command = lambda: self.graph_entry.delete(0,Tkinter.END))
        self.c.pack(side = Tkinter.RIGHT)

        #degree vs radian button
        self.dvr = Tkinter.Button(self.root, text="Graphing in Radians", command = lambda: self.flipDegRad())
        self.dvr.pack(side = Tkinter.RIGHT)
        
        #define axis range
        self.x_axis_range = Tkinter.Label(self.root, text = "X axis on")
        self.x_axis_range.pack(side = Tkinter.LEFT)
        self.x_axis_min = Tkinter.Entry(self.root, width = 5, text = "")
        self.x_axis_min.pack(side = Tkinter.LEFT)
        self.x_axis_max = Tkinter.Entry(self.root, width = 5, text = "")
        self.x_axis_max.pack(side = Tkinter.LEFT)
        
        #mainloop needs to be run
        #Every GUI is a loop...
        self.root.mainloop()

    #flips is_deg variable
    def flipDegRad(self):
        self.is_deg = not self.is_deg
        if self.is_deg:
            self.dvr["text"] = "Graphing in Degrees"
        else:
            self.dvr["text"] = "Graphing in Radians"
             

    def EnterKey(self):
        if self.root.focus_get() == self.c:
            self.graph_entry.delete(0,Tkinter.END)
        elif self.root.focus_get() == self.graph_entry or self.b:
            self.graph(self.graph_entry.get(), self.x_axis_min.get(), self.x_axis_max.get(), self.safe_dict)
        

    #graphs a function by grabbing from e.get()
    def graph(self, function_text, xmin, xmax, safe_dict):
		try:
		    #allow custom x ranges
			try:
				if xmin == "pi":
					xmin = pylab.pi
				elif xmin == "-pi":
					xmin = -pylab.pi
				elif xmin == "":
					xmin = -10.0
				else:	
					xmin = float(self.x_axis_min.get())
			except:
				print xmin, "is not a valid input."
				tkMessageBox.showinfo("Error", xmin + " is not a valid value for a range")
				raise
			try:
				if xmax == "pi":
					xmax = pylab.pi
				elif xmax == "-pi":
					xmax = -pylab.pi
				elif xmax == "":
					xmax = 10.0
				else:
					xmax = float(self.x_axis_max.get())
				print "Xmin:", xmin, "Xmax:", xmax
			except:
				print xmax, "is not a valid input."
				tkMessageBox.showinfo("Error", xmax + " is not a valid value for a range")
				raise
			#check for invalid ranges
			if xmin >= xmax:
				tkMessageBox.showinfo("Error",  "Invalid range. Xmin is not less than Xmax")
				exit()
			#pass function to Function class for evaluation
			try:
				x = pylab.arange(xmin, xmax, .01)
				safe_dict['x'] = locals().get('x')
				function = Function(function_text)
				function.formatFunction()
			except:
				print "Error occurred during function formatting."
				tkMessageBox.showinfo("Error", "Error occurred during function formatting")
				raise
			#attempt to graph a function
			try:
				y = eval(function.function_text, {"__builtins__":None}, safe_dict) 
				#sinx instead of sin(x) 
				#Maybe just add '(' x ')' parenthesis to all x's?
		
				print "Graphing: Y =", function_text

				if self.is_deg:
					pylab.plot(pylab.rad2deg(x), y, label = ("y = " + function_text))
				else:
					pylab.plot(x, y, label = ("y = " + function_text))
		
				#make the graph legend appear
				pylab.legend(loc='upper right')
				pylab.show()
			except:
				print function_text, "is not a valid function"
				tkMessageBox.showinfo("Error", function_text + " is not a valid function")
				raise
		except:
			print "An error occurred during graphing."
            
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
