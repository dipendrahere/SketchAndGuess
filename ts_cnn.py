import tensorflow as tf
import tflearn 
from tflearn.layers.conv import conv_2d, max_pool_2d
from tflearn.layers.core import input_data, fully_connected, dropout, flatten
from tflearn.layers.estimator import regression
import numpy as np 
from random import shuffle
import cv2
model = None
convnet = None
imageSize = None

def getmodel():
	global model
	return model

def makenet(ncategories, learning_rate = 1e-03, image_size = 28):
	global model, convnet, imageSize
	imageSize = image_size
	convnet = input_data(shape=[None, image_size, image_size, 1], name='input')

	convnet = conv_2d(convnet, 64, 2, activation='relu')
	convnet = max_pool_2d(convnet, 2)

	convnet = conv_2d(convnet, 32, 2, activation='relu')
	convnet = max_pool_2d(convnet, 2)


	# convnet = conv_2d(convnet, 32, 3, activation='relu ')
	# convnet = max_pool_2d(convnet, 2)

	# convnet = conv_2d(convnet, 32, 2, activation='relu')
	# convnet = max_pool_2d(convnet, 2)

	# convnet = conv_2d(convnet, 32, 2, activation='relu')
	# convnet = max_pool_2d(convnet, 2)

		#   convnet = conv_2d(  convnet, 32, 2, activation='relu')
		#   convnet = max_pool_2d(  convnet, 2)

		#   convnet = conv_2d(  convnet, 64, 2, activation='relu')
		#   convnet = max_pool_2d(  convnet, 2)

		#   convnet = fully_connected(  convnet, 128, activation='relu')
		#   convnet = dropout(  convnet, 0.8)

	convnet = fully_connected(convnet, 200, activation='relu')
	convnet = dropout(convnet, 0.8)
#	convnet = dropout(convnet, 0.2)

	convnet = fully_connected(convnet, ncategories, activation='softmax')

	convnet = regression(convnet, optimizer='adam', learning_rate=learning_rate, 
			loss='categorical_crossentropy', name='targets')

#with tf.device("/gpu:0"):

	model = tflearn.DNN(convnet, tensorboard_dir = 'log')

	return model


# with tf.device('/gpu:0'):
# 		model = tflearn.DNN(convnet, tensorboard_dir = 'log')

# with tf.device("/gpu:0"):
   #      model.fit({'input':X}, {'targets':Y}, n_epoch=n_epoch, validation_set=({'input':test_x}, {'targets':test_y}),
			# snapshot_step=snapshot_step, show_metric=True, run_id=name)
def predict(val):
	global model
	return model.predict(val)


def makemodel(data, name = 'ts_cnn_basic', validation_count = 1000, n_epoch = 1, snapshot_step = 1000):
	global model, convnet, imageSize

	if(validation_count > len(data)):
		print("Impossible to train without no dataset")
		return

	train = data[validation_count:]
	test = data[:validation_count]

	shuffle(train)
	shuffle(test)

	X = np.array([i[0] for i in train]).reshape(-1,   imageSize,   imageSize, 1)
	Y = [i[1] for i in train]

	test_x = np.array([i[0] for i in test]).reshape(-1,  imageSize,   imageSize, 1)
	test_y = [i[1] for i in test]

#	with tf.device("/gpu:0"):
	model.fit({'input':X}, {'targets':Y}, n_epoch=n_epoch, validation_set=({'input':test_x}, {'targets':test_y}),
			snapshot_step=snapshot_step, show_metric=True, run_id=name)

	model.save(name+".model")
	return model
		
def loadmodel(name):
	global model
	print("MODEL LOADED")
	model.load(name)
	return model

