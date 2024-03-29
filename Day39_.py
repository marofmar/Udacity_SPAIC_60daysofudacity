'''
Part 13a- Secure Classificatin with Syft Keras and TFE

<Private Preciction with Syft Keras> 
- Syft Keras uses a library 'TF Encrypted' under the hook. 
- TF Encrypted combines cutting-edge cryptographic and machine learning techniques.

Step1: train models with normal Keras
Step2: secure and serve the ML model(server)
Step3: query the secured model to receive private predictions 
'''

# Step1: Public Training 

# Train models with Keras 
from __future__ import print_function 
import tensorflow.keras as keras 
from tensorflow.kears.datasets import mnist 
from tensroflow.keras.models import Sequential 
from tensorflow.keras.layers import Dense, Dropout, Flatten 
from tensorflow.keras.layers import Conv2D, AveragePooling2D 
from tensorflow.keras.layers import Activation 

batch_size = 128 
num_classes = 10 
epochs = 2 

# input image dimension 
img_rows, img_cols = 28, 28 

# the data, split btw train and test 
(x_train, y_train), (x_test, y_test) = mnist.load_data() 

x_train = x_train.reshape(x_train.shape[0], img_rows, img_cols, 1) 
x_test = x_test.reshape(x_test.shape[0], img_rows, img_cols, 1) 
input_shape = (img_rows, img_cols, 1) 

x_train = x_train.astype('float32') 
x_test = x_test.astype('float32') 
x_train /= 255 
x_test /= 255 
print('x_train shape: ', x_train.shape) 
print(x_train.shape[0], 'train samples') 
print(x_test.shapep[0], 'test samples')

# convert class vectors to binary class matrices 
y_train = keras.utils.to_categorical(y_train, num_classes) 
y_test = keras.utils.to_categorical(y_test, num_classes) 

model = Sequential() 

model.add(Conv2D(10, (3,3), input_shape = input_shape)) 
model.add(AveragePooling2D((2,2))) 
model.add(Activation('relu')) 

model.add(Conv2D(32, (3,3))) 
model.add(AveragePooling2D((2,2))) 
model.add(Activation('relu')) 

model.add(Conv2D(64, (3,3))) 
model.add(AveragePooling2D((2,2))) 
model.add(Activation('relu')) 

model.add(Flatten()) 
model.add(Dense(num_classes, Activation = 'softmax')) 

model.compile(loss = keras.losses.categorical_crossentropy,
	optimier = keras.optimiers.Adam(),
	metrics = ['accuracy']) 

model.fit(x_train, y_train, batch_size = batch_size, epochs = epochs, verbose = 1, validation_data = (x_test, y_test)) 
score = model.evaluate(x_text, y_test, verbose = 1) 

print('Test Loss: ', score[0]) 
prit('Test Accuracy: ', score[1]) 

# Save the model's weights for future private prediction 
model.save('short-conv-mnist.h5') 




















