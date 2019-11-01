import json
import tensorflow as tf
import re
import struct
import numpy as np
import uuid
import cv2
import tensorflowjs as tfjs

def get_letterbox_image (im, w, h):
  if w / im.shape[1] < h / im.shape[0]:
    new_w = w
    new_h = int(im.shape[0] * w / im.shape[1])
  else:
    new_h = h
    new_w = int(im.shape[1] * h / im.shape[0])
  resized = cv2.resize(im, (new_w, new_h))
  boxed = np.full(fill_value = 127, shape = (h, w, 3), dtype = np.uint8)
  t = (h - new_h) // 2
  l = (w - new_w) // 2
  boxed[t : t + new_h, l : l + new_w] = resized
  return boxed

def convert (cfg_path, weight_path):
  with open(cfg_path, 'rt') as fin:
    ls = fin.readlines()
    ls = [l.strip() for l in ls]

  model_defs = []
  regex = re.compile(r'\[([a-zA-Z]+)\]')
  for i, l in enumerate(ls):
    match = regex.match(l)
    if match is not None:
      model_defs.append([i, match[1]])

  # print(model_defs)

  for i, model_def in enumerate(model_defs):
    s = model_def[0] + 1
    if i < len(model_defs) - 1:
      e = model_defs[i + 1][0]
    else:
      e = len(ls)

    params = ls[s : e]
    params = [param for param in params if len(param) > 0]
    model_def.append(params)

  # print(model_defs)
  for i, model_def in enumerate(model_defs):
    params = model_def[2]
    params = [param.split('=') for param in params if param[0] != '#']
    params = {param[0]: param[1] for param in params}
    model_defs[i] = {
      'name': model_def[1],
      **params
    }

  # print(model_defs)

  layers = []
  weights = {}
  with open(weights_path, 'rb') as fin:
    major, minor, revision, _ = struct.unpack('4i', fin.read(16))
    # print(major, minor, revision, _)

    B, H, W, C = [None] * 4
    lcnt = 0
    for model_def in model_defs:
      lcnt += 1
      if model_def['name'] == 'net':
        # B = int(model_def['batch'])
        B = 1
        H = int(model_def['height'])
        W = int(model_def['width'])
        C = int(model_def['channels'])
        layers.append(tf.keras.layers.Input(shape = [H, W, C], batch_size = B, dtype = tf.float32, name = '0'))
      elif model_def['name'] == 'convolutional':
        filters = int(model_def['filters'])
        size = int(model_def['size'])
        activation = model_def['activation']
        stride = int(model_def['stride'])
        pad = int(model_def['pad'])
        batch_normalize = model_def.pop('batch_normalize', None)
        if stride != 1 or stride != pad:
          raise ValueError('unsupported convolutional layer params')
        
        filter_weight_size = filters * C * size * size
        biases = np.array(struct.unpack(f'{filters}f', fin.read(filters * 4)), dtype = np.float32).reshape(filters)
        if batch_normalize is not None:
          scales = np.array(struct.unpack(f'{filters}f', fin.read(filters * 4)), dtype = np.float32).reshape(filters)
          moving_mean = np.array(struct.unpack(f'{filters}f', fin.read(filters * 4)), dtype = np.float32).reshape(filters)
          moving_variance = np.array(struct.unpack(f'{filters}f', fin.read(filters * 4)), dtype = np.float32).reshape(filters)
        filter_weight = np.array(struct.unpack(f'{filter_weight_size}f', fin.read(filter_weight_size * 4)), dtype = np.float32).reshape(filters, C, size, size).transpose([2, 3, 1, 0])
        # filter_weight = np.array(struct.unpack(f'{filter_weight_size}f', fin.read(filter_weight_size * 4)), dtype = np.float32).reshape(C, filters, size, size).transpose([2, 3, 0, 1])

        # id = str(uuid.uuid4())
        id = str(len(layers))
        layers.append(tf.keras.layers.Conv2D(
          filters = filters,
          kernel_size = size,
          strides = stride,
          padding = 'same',
          activation = None,
          use_bias = False if batch_normalize is not None else True,
          name = id
        )(inputs = layers[-1]))
        weights[id] = [filter_weight, *([] if batch_normalize is not None else [biases])]

        if batch_normalize is not None:
          # id = str(uuid.uuid4())
          id = str(len(layers))
          layers.append(tf.keras.layers.BatchNormalization(
            momentum = 0.9,
            epsilon = 1e-5,
            trainable = False,
            fused = True,
            name = id
          )(inputs = layers[-1]))
          weights[id] = [scales, biases, moving_mean, moving_variance]
        
        if model_def['activation'] == 'leaky':
          layers.append(tf.keras.layers.LeakyReLU(alpha = 0.1, name = str(len(layers)))(inputs = layers[-1]))
        elif model_def['activation'] == 'linear':
          pass
        else:
          raise ValueError('unsupported acitvation.')
        C = filters
      elif model_def['name'] == 'maxpool':
        layers.append(tf.keras.layers.MaxPool2D(
          pool_size = int(model_def['size']),
          strides = int(model_def['stride']),
          padding = 'same',
          name = str(len(layers))
        )(inputs = layers[-1]))
        H = H // 2
        W = W // 2
      elif model_def['name'] == 'avgpool':
        layers.append(tf.keras.layers.AvgPool2D(
          pool_size = (H, W),
          strides = (H, W),
          padding = 'same',
          name = str(len(layers))
        )(inputs = layers[-1]))
        H = 1
        W = 1
      elif model_def['name'] == 'softmax':
        layers.append(tf.keras.layers.Flatten(name = str(len(layers)))(layers[-1]))
        layers.append(tf.keras.layers.Softmax(name = str(len(layers)))(inputs = layers[-1]))
        break
      else:
        raise ValueError('unsupported layer')
      # print(fin.tell())
    if lcnt != len(model_defs):
      print(lcnt)
      print(len(model_defs))
      raise ValueError('last layer must be `softmax`')

  # model = tf.keras.Sequential(layers)
  model = tf.keras.Model(inputs = layers[0], outputs = layers[-1])
  for layer in model.layers:
    if layer.name in weights.keys():
      layer.set_weights(weights[layer.name])
  
  return model
    

if __name__ == '__main__':
  cfg_path = r'C:\Projects\tensorflow.js-classification-example\train\imagenet\tiny.cfg'
  weights_path = r'C:\Projects\tensorflow.js-classification-example\train\imagenet\tiny.weights'
  output_tensorflowjs_model_path = r'..\..\frontend\public\imagenet'
  test_image_path = r'C:\Users\jijo\Documents\eagle.jpg'

  model = convert(cfg_path, weights_path)
  model.compile(optimizer = tf.keras.optimizers.Adam(learning_rate = 1e-9), loss = 'sparse_categorical_crossentropy', metrics = ['accuracy'])
  tfjs.converters.save_keras_model(model, output_tensorflowjs_model_path)

  if test_image_path is not None:
    src = cv2.imread(test_image_path, cv2.IMREAD_COLOR)
  if src is not None:  
    with open('darknet_imagenet_classname.json', 'rt') as f:
      class_names = json.load(f)
    src = get_letterbox_image(src, 224, 224)
    src = src[..., ::-1]
    src = src.astype(np.float32)
    src /= 255
    res = model.predict(src[np.newaxis, ...], batch_size = 1)
    top_5 = np.argsort(np.squeeze(res))[::-1][:5]
    print(np.array(class_names)[top_5])