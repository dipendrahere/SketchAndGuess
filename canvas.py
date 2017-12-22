from tkinter import *
import threading as thread
from PIL import Image, ImageTk
from PIL import ImageDraw
import tkinter as tk
from tkinter import filedialog
import os
import shutil 
import numpy as np
import cv2

img = Image.new('L', (450, 450), 'white')
draw = ImageDraw.Draw(img)

class mycanvas(Frame):
	def __init__(self, parent, width=300, height=300):
		Frame.__init__(self, parent)
		self.__b1 = "up"
		self.__check = False
		self.__xold, self.__yold = None, None
		self.__image = None
		self.__mode = 0
		# self.__control_frame = Frame(self, width = 300)
		# self.__control_frame.grid(row = 0, column = 0, pady = (20,0))
		self.__control_frame = Frame(self)
		self.__control_frame.grid(row = 0, column = 0, sticky = N+W, pady=(30,90), columnspan=2)
		self.__labelhelp = Label(self.__control_frame, font = ('Helvetica', 30), text = '?', anchor=W, fg='#aaaaaa')
		self.__labelhelp.grid(row= 0, column = 0, sticky = N+W)

		self.__browse = Label(self.__control_frame, font = ('Helvetica', 30), text = '', anchor=W, fg='#aaaaaa')
		self.__browse.grid(row= 0, column = 1, sticky = E, padx=(950,0))
		self.__browse.bind("<1>", self.__browseevent)
		self.__canvas = Canvas(self, height = 450, width = 450, bg = '#ffffff', bd=2, relief='ridge')
		self.__canvas.grid(row=1, column = 0, padx=50, pady = 0, sticky = W)
		self.__help = None
		# self.__pencil = Button(self.__control_frame, text = "Pencil", width = 21)
		# self.__pencil.grid(row = 0, column = 0, pady = 0)
		# self.__eraser = Button(self.__control_frame, text = "Eraser", width = 22)
		# self.__eraser.grid(row=0, column = 1, pady = 0)
		# self.__reset = Button(self.__control_frame, text = "Reset", width = 21)
		# self.__reset.grid(row=0, column = 2, pady = 0)
		self.__prediction = Frame(self, width = 10)
		self.__prediction.grid(row = 1, column = 1, sticky=W+E+S+N, pady = (0,0), padx = 0)
		self.pfirst = Label(self.__prediction, font = ("chalkduster", 50),text="tree", anchor = W, width = 18)
		self.pfirst.grid(row=0, column=0, pady=(105, 0), sticky=W)
		#self.__pfirst.grid(row=0,column=0, sticky = N+E+W+S)
		self.psecond = Label(self.__prediction, font = ("chalkduster", 40), text="bird bulb alarm clock", anchor = W, width = 22)
		#self.__psecond.pack()
		self.psecond.grid(row=1,column=0, sticky =W,)
		self.pthird = Label(self.__prediction, font = ("chalkduster", 30), text="sun moon ceiling fan flower", anchor = W, width = 29)
		#self.__pthird.pack()
		self.pthird.grid(row=2,column=0, sticky = W,)
		self.pfourth = Label(self.__prediction, font = ("chalkduster", 20), text="cat car snake train banana nose circle line", anchor = W, width = 45)
		#self.__pthird.pack()
		self.pfourth.grid(row=3,column=0, sticky =W,)
		self.__clear(0)
		#self.__psecond = Label(self.__prediction, font = ("chalkduster",  ))


	def getCanvas(self):
		return self.__canvas


	def clearpre(self):
		self.pfirst.config(text = "")
		self.psecond.config(text = "")
		self.pthird.config(text = "")
		self.pfourth.config(text = "")
	
	def __erase(self, event):
		global draw
		if self.__mode == 1:
			return 
		if self.__b1 == "down":
			event.widget.create_rectangle(event.x-9, event.y-9,event.x+9, event.y+9, fill = 'white', outline='white',)
			draw.rectangle(((event.x-9,event.y-9),(event.x+9,event.y+9)), fill="white", outline = "white")
			
	def activate_pencil(self):
		#self.__unbind_canvas(self.__canvas)
		self.__canvas.bind("<B1-Motion>", self.__draw)
		self.__canvas.bind("<Button-1>", self.__down_button)
		self.__canvas.bind("<ButtonRelease-1>", self.__up_button)
		

	def getimage(self):
		return self.__image
	def __browseevent(self, event):
		root = Tk()
		root.withdraw()
		self.__help.destroy()
		currdir = os.getcwd()
		tempfile = filedialog.askopenfilename(title='Please select a directory', 
			filetypes=[ ('All','*')])
		
		#print(tempfile)
		if tempfile == '':
			return 

		self.__mode = 1
		shutil.copy(tempfile, os.path.join(os.getcwd(),"test.jpg"))
		img =  cv2.imread('test.jpg')
		img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
		thresh = cv2.resize(img, (450,450))
		img=Image.fromarray(thresh)
		self.__image = ImageTk.PhotoImage(image=img) 
		self.__canvas.create_image(230,230,image = self.__image)
		self.__check = True

	def setcheck(self, value):
		self.__check = value

	def getcheck(self):
		return self.__check




	#TODO: getters and setters for the labels of the message predicton


	





	def __clear(self, event):
		self.clearpre()
		self.__canvas.create_rectangle(0,0,1000,1000 , fill = 'white', outline='white')
		
		draw.rectangle(((0,0),(1000,1000)), fill="white", outline = "white")
		try:
			self.__check = False
			os.remove("test.jpg")
			self.__image = None
			self.__mode = 0
		except:
			exist = None
	# def __unbind_canvas(self,canvas):
	# 	self.__canvas.unbind("<Motion>")
	# 	self.__canvas.unbind("<ButtonPress-1>")
	# 	self.__canvas.unbind("<ButtonRelease-1>")

	def __draw(self, event):
		global draw
		if self.__mode == 1:
			return 
		if self.__b1 == "down":
			if self.__xold is not None and self.__yold is not None:
				event.widget.create_line(self.__xold,self.__yold,event.x,event.y, width = 4)
				draw.line([self.__xold, self.__yold, event.x, event.y], width=4)
			self.__xold = event.x
			self.__yold = event.y

	def __down_button(self, event):
		if self.__mode == 1:
			return 
		self.__b1 = "down"

	def __up_button(self, event):
		if self.__mode == 1:
			return 
		self.__b1 = "up"
		self.__xold = None
		self.__yold = None
		img.save("test.jpg")
		self.__image = img
		self.__check = True

	def activate_eraser(self):
		self.__canvas.bind("<B2-Motion>", self.__erase)
		self.__canvas.bind("<ButtonPress-2>", self.__down_button)
		self.__canvas.bind("<ButtonRelease-2>", self.__up_button)

	def __showhelp(self, event, t, w, h, x, y):
		self.__help = floatinghelp()
		self.__help.geometry('%dx%d+%d+%d' % (w, h, x, y))
		self.__help.overrideredirect(True)
		self.__help.config(bg="#ffffaa")
		helpmsg = Message(self.__help, text= t
			,width=1000, bg='#ffffaa', font=('candara', 16))
		helpmsg.grid(row=0,column=0, sticky=N+W+E+S, padx=10, pady=10)
		
	def __destroyhelp(self, event):
		self.__help.destroy()

	def activate_escape(self, root):
		root.bind("<Escape>", self.__clear)

	def activate_toplevel(self):
		self.__labelhelp.bind("<Enter>", lambda event, t = "Click and draw on the canvas, Right or middle click to erase and Press Esc to reset.",
			w=570, h=52, x=100, y =100
			: self.__showhelp(event, t, w, h, x, y))
		self.__labelhelp.bind("<Leave>", self.__destroyhelp)

		self.__browse.bind("<Enter>", lambda event, t = "Click on browse to predict for a captured image.",
			w=350, h=52, x=700, y =100
			: self.__showhelp(event, t, w, h, x, y))
		self.__browse.bind("<Leave>", self.__destroyhelp)

	def activate_all(self, root):
		self.activate_pencil()
		self.activate_eraser()
		self.activate_escape(root)
		self.activate_toplevel()

class floatinghelp(Toplevel):
	def __init__(self, *args):
		Toplevel.__init__(self, *args)
		self.overrideredirect(True)




# root = Tk()
# root.geometry("{}x{}+0+0".format(
# 	root.winfo_screenwidth()-3,root.winfo_screenheight()-3))
# x = mycanvas(root, 600,700)
# x.activate_all()

# x.pack()

# root.mainloop()


