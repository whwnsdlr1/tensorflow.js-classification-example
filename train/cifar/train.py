from tensorflow.compat.v1 import ConfigProto
import tensorflow as tf
import numpy as np
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.initializers import he_normal
import tensorflowjs as tfjs

class Model(object):
  def __init__ (self, inputs):
    super(Model, self).__init__()

    self._inputs = inputs
    self._conv1 = tf.keras.layers.Conv2D(filters = 16, kernel_size = 1, padding = 'same', activation = None, kernel_initializer = he_normal(), name = '1')
    self._lrelu1 = tf.keras.layers.LeakyReLU(name = '2')
    self._conv2 = tf.keras.layers.Conv2D(filters = 16, kernel_size = 3, padding = 'same', activation = None, kernel_initializer = he_normal(), name = '3')
    self._lrelu2 = tf.keras.layers.LeakyReLU(name = '4')
    self._conv3 = tf.keras.layers.Conv2D(filters = 64, kernel_size = 1, padding = 'same', activation = None, kernel_initializer = he_normal(), name = '5')
    self._lrelu3 = tf.keras.layers.LeakyReLU(name = '6')
    self._max_pool1 = tf.keras.layers.MaxPool2D(pool_size = (2, 2), name = '7')
    self._conv4 = tf.keras.layers.Conv2D(filters = 32, kernel_size = 1, padding = 'same', activation = None, kernel_initializer = he_normal(), name = '8')
    self._lrelu4 = tf.keras.layers.LeakyReLU(name = '9')
    self._conv5 = tf.keras.layers.Conv2D(filters = 32, kernel_size = 3, padding = 'same', activation = None, kernel_initializer = he_normal(), name = '10')
    self._lrelu5 = tf.keras.layers.LeakyReLU(name = '11')
    self._conv6 = tf.keras.layers.Conv2D(filters = 128, kernel_size = 1, padding = 'same', activation = None, kernel_initializer = he_normal(), name = '12')
    self._lrelu6 = tf.keras.layers.LeakyReLU(name = '13')
    self._max_pool2 = tf.keras.layers.MaxPool2D(pool_size = (2, 2), name = '14')
    self._conv7 = tf.keras.layers.Conv2D(filters = 64, kernel_size = 1, padding = 'same', activation = None, kernel_initializer = he_normal(), name = '15')
    self._lrelu7 = tf.keras.layers.LeakyReLU(name = '16')
    self._conv8 = tf.keras.layers.Conv2D(filters = 64, kernel_size = 3, padding = 'same', activation = None, kernel_initializer = he_normal(), name = '17')
    self._lrelu8 = tf.keras.layers.LeakyReLU(name = '18')
    self._conv9 = tf.keras.layers.Conv2D(filters = 256, kernel_size = 1, padding = 'same', activation = None, kernel_initializer = he_normal(), name = '19')
    self._lrelu9 = tf.keras.layers.LeakyReLU(name = '20')
    self._avg_pool = tf.keras.layers.AvgPool2D(pool_size = (8, 8), name = '21')
    
    self._flatten = tf.keras.layers.Flatten(name = '22')
    self._dropout1 = tf.keras.layers.Dropout(0.5, name = '23')
    self._dense1 = tf.keras.layers.Dense(512, activation = 'relu', kernel_initializer = he_normal(), name = '24')
    self._dense2 = tf.keras.layers.Dense(100, activation = 'softmax', kernel_initializer = he_normal(), name = '25')

  def get_model (self):
    def call (input, training = False):
      x = input
      x = self._conv1(x)
      x = self._lrelu1(x)
      x = self._conv2(x)
      x = self._lrelu2(x)
      x = self._conv3(x)
      x = self._lrelu3(x)
      x = self._max_pool1(x)      
      x = self._conv4(x)
      x = self._lrelu4(x)
      x = self._conv5(x)
      x = self._lrelu5(x)
      x = self._conv6(x)
      x = self._lrelu6(x)
      x = self._max_pool2(x)
      x = self._conv7(x)
      x = self._lrelu7(x)
      x = self._conv8(x)
      x = self._lrelu8(x)
      x = self._conv9(x)
      x = self._lrelu9(x)
      x = self._avg_pool(x)
      x = self._flatten(x)
      x = self._dropout1(x)
      x = self._dense1(x)
      x = self._dense2(x)
      return x
    return tf.keras.Model(inputs = self._inputs, outputs = call(self._inputs), name = 'CIFAR')

config = ConfigProto()
config.gpu_options.allow_growth = True
tf.keras.backend.set_session(tf.Session(config=config))

if __name__ == '__main__':
  output_tensorflowjs_model_path = r'../../frontend/public/cifar'

  (x_train, y_train), (x_test, y_test) = tf.keras.datasets.cifar100.load_data()
  x_train = x_train.astype(np.float32) / 255
  x_train, x_validation, y_train, y_validation = x_train[: 40000], x_train[40000: ], y_train[: 40000], y_train[40000: ]
  x_test = x_test.astype(np.float32) / 255

  model = Model(tf.keras.Input(shape = (32, 32, 3), name = '0'))
  keras_model1 = model.get_model()

  lr = 1e-3
  optimizer = tf.keras.optimizers.SGD(learning_rate = lr, momentum = 0.9, nesterov = True)
  keras_model1.compile(optimizer, loss = 'sparse_categorical_crossentropy', metrics = ['accuracy'])
  early_stopping = EarlyStopping(monitor = 'val_acc', patience = 30, verbose = 1, mode = 'max', restore_best_weights = True)
  keras_model1.fit(x_train, y_train, epochs = 500, batch_size = 32, validation_data = (x_validation, y_validation), callbacks = [early_stopping])
  print('\nTest')
  test_loss, test_acc = keras_model1.evaluate(x_test, y_test)
  tfjs.converters.save_keras_model(keras_model1, output_tensorflowjs_model_path)