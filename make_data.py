import numpy as np
from random import shuffle
from tqdm import tqdm
import os
from PIL import Image

categories = {}
dataset= [] 
rcategories = {}

def makeset(ncategories, foldername = "gdataset"):
	global categories, rcategories, dataset
	i = 0
	for v in tqdm(sorted(os.listdir(os.path.join(os.getcwd(), foldername)))):
		if v == ".DS_Store":
			continue
		if os.path.isdir(os.path.join(os.path.join(os.getcwd(), foldername), v)):
			continue
		try:
			temp = np.load(os.path.join(os.path.join(os.getcwd(), foldername), v))
		except:
			print("")
		name = v.split(".")[0]
		categories[name] = i
		rcategories[i] = name
		category = [0]*ncategories
		category[i] = 1
		i = i+1
		for x in temp:
			dataset.append([np.reshape(x, (28,28)), category])
	shuffle(dataset)
	print(categories)
	print("\n\n\n\n", rcategories, "\n\n\n\n")
	dataset = dataset[:510000]
	shuffle(dataset)

def getc(foldername = "gdataset"):
	i = 0
	for v in tqdm(sorted(os.listdir(os.path.join(os.getcwd(), foldername)))):
		if v == ".DS_Store":
			continue
		if os.path.isdir(os.path.join(os.path.join(os.getcwd(), foldername), v)):
			continue
		rcategories[i] = v.split(".")[0]
		categories[v.split(".")[0]] = i
		i = i+1

def check():
	print(categories)
	r = dataset[20]
	Image.fromarray(r[0]).show()
	for i in range(len(r[1])):
		if r[1][i] == 1:
			print(rcategories[i])


