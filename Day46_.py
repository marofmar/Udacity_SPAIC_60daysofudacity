# -*- coding: utf-8 -*-
"""Conv_VAE.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1r0fd_cMkyubUBfgFsYKYc_brvlqeEeNV

## How to generate images of handwritten digits with AutoEncoder
[CVAE](https://www.tensorflow.org/beta/tutorials/generative/cvae)
"""

# for gif 
!pip install -q imageio

# Commented out IPython magic to ensure Python compatibility.
# import libraries
from __future__ import absolute_import, division, print_function, unicode_literals

try: 
#   %tensorflow_version 2.x 
except Exception:
  pass 
import tensorflow as tf 

import os 
import time
import numpy as np 
import glob 
import matplotlib.pyplot as plt 
import PIL 
import imageio 

from IPython import display

# load MNIST 
'''
- vector of 784 int
- each int btw 0-255 
- model each pixel with a Bernoulli distribution, and statically binarize the dataset (WOW)
'''
(train_images, _), (test_images, _) = tf.keras.datasets.mnist.load_data()

train_images.shape

train_images = train_images.reshape(train_images.shape[0], 28, 28, 1).astype('float32') 
test_images = test_images.reshape(test_images.shape[0], 28, 28, 1).astype('float32') 

# normalize images ot the range of [0,1] 
train_images /= 255. 
test_images /= 255.

# binarize
train_images[train_images >= .5] = 1. 
train_images[train_images < .5] = 0.
test_images[test_images >= .5] = 1. 
test_images[test_images < .5] = 0.

TRAIN_BUF = 60000 
BATCH_SIZE = 100 
TEST_BUF = 10000

# use tf.data to create batches and shuffle the dataset 
train_dataset = tf.data.Dataset.from_tensor_slices(train_images).shuffle(TRAIN_BUF).batch(BATCH_SIZE) 
test_dataset = tf.data.Dataset.from_tensor_slices(test_images).shuffle(TEST_BUF).batch(BATCH_SIZE)

# wire up the generative and inference network with tf.kears.Sequential 
# NOTE: common practice to avoid using batch normalization when training VAEs,
# since the additional stochasticity due to using mini-batches may aggravate instability on top of the stochasticity from smapling

class CVAE(tf.keras.Model):
  def __init__(self, latent_dim):
    super(CVAE, self).__init__() 
    self.latent_dim = latent_dim 
    self.inference_net = tf.keras.Sequential(
    [
        tf.keras.layers.InputLaeyr(input_shape = (28, 28, 1)),
        tf.keras.layers.Conv2D(filters = 32, kernel_size = 3, strides = (2,2), activation = 'relu'),
        tf.keras.layers.Conv2D(filters = 64, kernel_size = 3, strides = (2,2), activation = 'relu'),
        tf.keras.layers.Flatten(),
        #no activation
        tf.keras.layers.Dense(latent_dim + latent_dim),    
    ]
    )
    
    self.generative_net = tf.keras.Sequential(
    [
        tf.keras.layers.InputLayer(input_shape = (latent_dim,)),
        tf.keras.layers.Dense(units=7*7*32, activation = tf.nn.relu),
        tf.keras.layers.Reshape(target_shape = (7,7,32)),
        tf.keras.layers.Conv2DTranspose(filter = 64, kernel_size = 3, stirdes = (2,2), padding = 'SAME', activation = 'relu'),
        tf.keras.layers.Conv2DTranspose(filter = 32, kernel_size = 3, strides = (2,2), padding = "SAME", activation = 'relu'),
        # no activation 
        tf.keras.layers.Conv2DTranspose(filter = 1, kernel_size = 3, strides = (1,1), padding = 'SAME'),
    ]
    )
    
    @tf.function 
    def sample(self, eps = None):
      if eps is None:
        eps = tf.random.normal(shape = (100, self.latent_dim)) 
      return self.decode(eps, apply_sigmoid = True) 
    
    def encode(self, x):
      mean, logvar = tf.split(self.inference_net(x), num_or_size_splits = 2, axis = 1) 
      return mean, logvar 
    
    def reparameterize(self, mean, logvar):
      eps = tf.random.normal(shape = mean.shape)
      return eps*tf.exp(logvar*.5) + mean 
    
    def decode(self, z, apply_sigmoid = False):
      logits = self.generative_net(z) 
      if apply_sigmoid:
        probs = tf.sigmoid(logits)
        return probs 
      return logits
