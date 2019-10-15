import tensorflow as tf
import numpy as np

class Model(object):
  def __init__ (self, inputs):
    super(Model, self).__init__()
    
    self._inputs = inputs
    self._conv1 = tf.keras.layers.Conv2D(input_shape = (28, 28, 1), filters = 16, kernel_size = 3, padding = 'same', activation = 'relu', name = '1')
    self._max_pool1 = tf.keras.layers.MaxPool2D(pool_size = (2, 2), name = '2')
    self._conv2 = tf.keras.layers.Conv2D(filters = 32, kernel_size = 3, padding = 'same', activation = 'relu', name = '3')
    self._max_pool2 = tf.keras.layers.MaxPool2D(pool_size = (2, 2), name = '4')
    self._flatten = tf.keras.layers.Flatten(input_shape = (7, 7, 32), name = '5')
    self._dense1 = tf.keras.layers.Dense(40, activation = 'relu', name = '6')
    self._dense2 = tf.keras.layers.Dense(10, activation = 'softmax', name = '7')

  def get_model (self):
    def call (input, training = False):
      x = input
      x = self._conv1(x)
      x = self._max_pool1(x)
      x = self._conv2(x)
      x = self._max_pool2(x)
      x = self._flatten(x)
      x = self._dense1(x)
      x = self._dense2(x)
      return x
    return tf.keras.Model(inputs = self._inputs, outputs = call(self._inputs), name = 'MNIST')