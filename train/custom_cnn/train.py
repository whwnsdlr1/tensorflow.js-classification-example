import train
import tensorflow as tf
import numpy as np
from PIL import Image
import time
import os
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
import tensorflowjs as tfjs

from model import Model

if __name__ == '__main__':
  output_tensorflowjs_model_path = r'../../frontend/public/custom_cnn'

  (x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()
  x_train = x_train[..., np.newaxis].astype(np.float32) / 255
  x_train, x_validation, y_train, y_validation = x_train[: 50000], x_train[50000: ], y_train[: 50000], y_train[50000: ]
  x_test = x_test[..., np.newaxis].astype(np.float32) / 255

  model = Model(tf.keras.Input(shape = (28, 28, 1), name = '0'))
  keras_model1 = model.get_model()
    
  keras_model1.compile(optimizer = 'adam', loss = 'sparse_categorical_crossentropy', metrics = ['accuracy'])
  early_stopping = EarlyStopping(monitor = 'val_loss', patience = 10, verbose = 1, mode = 'min', restore_best_weights = True)
  # mcp_save = ModelCheckpoint(filepath = './custom_cnn.hdf5', monitor = 'val_loss', save_best_only = True, mode = 'min')
  keras_model1.fit(x_train, y_train, epochs = 100, batch_size = 32, validation_data = (x_validation, y_validation), callbacks = [early_stopping])
  print('\nTest')
  test_loss, test_acc = keras_model1.evaluate(x_test, y_test)
  tfjs.converters.save_keras_model(keras_model1, output_tensorflowjs_model_path)
