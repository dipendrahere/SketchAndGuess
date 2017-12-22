import ts_cnn
import pyttsx
import make_data
import threading
import time
import cv2
from tkinter import *
from PIL import Image
from PIL import ImageDraw
from canvas import mycanvas
import subprocess

import numpy as np
import tkinter as tk

import os


class SayThread(threading.Thread):
	def __init__(self, text):
		threading.Thread.__init__(self)
		self.text = text
		#self.engine = pyttsx.init()

	def run(self):
		subprocess.call('say ' + "I see "+self.text, shell=True)


class PredictorThread(threading.Thread):

	def __init__(self, mod, gui, cat, rcat):
		threading.Thread.__init__(self)
		self.mod = mod
		self.gui = gui
		self.cat = cat
		self.rcat = rcat

	def run(self):
		while True:
			if self.gui.getcheck() == True:
				self.gui.setcheck(False)
				img =  cv2.imread('test.jpg')
				gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
				#print(gray)
				thresh = cv2.adaptiveThreshold(gray,255,1,1,5,2)
				thresh = cv2.resize(thresh, (28,28), interpolation = cv2.INTER_AREA)
				ans = self.mod.predict(thresh.reshape(-1,28, 28, 1))
				ans = ans[0]
				answer = []
				for i in range(len(ans)):
					answer.append([ans[i],rcat[i]])
				answer = sorted(answer)[::-1]
				print(answer)
				self.gui.pfirst.config(text = answer[0][1])
				second = ""
				count = 1
				for i in range(1,len(answer)):
					if len(second+answer[i][1]) > 22:
						count = i-1
						self.gui.psecond.config(text = second)
						break
					second = second + answer[i][1]+" "
				second = ""
				for i in range(count+1, len(answer)):
					if len(second+answer[i][1]) > 29:
						count = i-1
						self.gui.pthird.config(text = second)
						break
					second = second + answer[i][1]+" "
				second=""
				for i in range(count+1, len(answer)):
					if len(second+answer[i][1]) > 45:
						count = i-1
						self.gui.pfourth.config(text = second)
						break
					second = second + answer[i][1]+" "
				SayThread(answer[0][1]).start()

size = 28
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'

#temp = make_data.makeset(57)
#print("making",make_data.rcategories)
make_data.getc()

cat = make_data.categories
rcat = make_data.rcategories
print(rcat)
#print(rcat)
data = make_data.dataset
mod = ts_cnn.makenet(57,image_size = 28)
#mod = ts_cnn.makemodel(data)
mod = ts_cnn.loadmodel("ts_cnn_basic.model")
root = Tk()
root.geometry("{}x{}+0+0".format(
	root.winfo_screenwidth()-3,root.winfo_screenheight()-3))
x = mycanvas(root, 600,700)
x.activate_all(root)
x.pack()
try:
	thread = PredictorThread(mod, x, cat, rcat)
	thread.daemon = True
	thread.start()
except:
	print("Fallen")


root.mainloop()

