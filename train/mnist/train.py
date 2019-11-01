import tensorflow as tf
import numpy as np
from tensorflow.keras.callbacks import EarlyStopping
import tensorflowjs as tfjs

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

if __name__ == '__main__':
  output_tensorflowjs_model_path = r'../../frontend/public/mnist'

  (x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()
  x_train = x_train[..., np.newaxis].astype(np.float32) / 255
  x_train, x_validation, y_train, y_validation = x_train[: 50000], x_train[50000: ], y_train[: 50000], y_train[50000: ]
  x_test = x_test[..., np.newaxis].astype(np.float32) / 255

  model = Model(tf.keras.Input(shape = (28, 28, 1), name = '0'))
  keras_model1 = model.get_model()
    
  keras_model1.compile(optimizer = 'adam', loss = 'sparse_categorical_crossentropy', metrics = ['accuracy'])
  early_stopping = EarlyStopping(monitor = 'val_loss', patience = 10, verbose = 1, mode = 'min', restore_best_weights = True)
  keras_model1.fit(x_train, y_train, epochs = 100, batch_size = 32, validation_data = (x_validation, y_validation), callbacks = [early_stopping])
  print('\nTest')
  test_loss, test_acc = keras_model1.evaluate(x_test, y_test)
  tfjs.converters.save_keras_model(keras_model1, output_tensorflowjs_model_path)
