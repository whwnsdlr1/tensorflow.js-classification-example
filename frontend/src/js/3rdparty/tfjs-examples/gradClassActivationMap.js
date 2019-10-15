/**
 * @license
 * Copyright 2019 Google LLC. All Rights Reserved.
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 * =============================================================================
 */

const { applyColorMap } = require('./applyColorMap.js')

export function gradClassActivationMap (model, classIndex, x) {
  const tf = window.tf
  // Try to locate the last conv layer of the model.
  let layerIndex = model.layers.length - 1;
  while (layerIndex >= 0) {
    if (model.layers[layerIndex].getClassName().startsWith('Conv')) {
      break;
    }
    layerIndex--;
  }
  tf.util.assert(
      layerIndex >= 0, `Failed to find a convolutional layer in model`);

  const lastConvLayer = model.layers[layerIndex];
  /*
  console.log(
      `Located last convolutional layer of the model at ` +
      `index ${layerIndex}: layer type = ${lastConvLayer.getClassName()}; ` +
      `layer name = ${lastConvLayer.name}`);
  */
  // Get "sub-model 1", which goes from the original input to the output
  // of the last convolutional layer.
  const lastConvLayerOutput = lastConvLayer.output;
  const subModel1 =
      tf.model({inputs: model.inputs, outputs: lastConvLayerOutput});

  // Get "sub-model 2", which goes from the output of the last convolutional
  // layer to the original output.
  const newInput = tf.input({shape: lastConvLayerOutput.shape.slice(1)});
  layerIndex++;
  let y = newInput;
  while (layerIndex < model.layers.length) {
    y = model.layers[layerIndex++].apply(y);
  }
  const subModel2 = tf.model({inputs: newInput, outputs: y});

  return tf.tidy(() => {
    // This function runs sub-model 2 and extracts the slice of the probability
    // output that corresponds to the desired class.
    const convOutput2ClassOutput = (input) =>
        subModel2.apply(input, {training: true}).gather([classIndex], 1);
    // This is the gradient function of the output corresponding to the desired
    // class with respect to its input (i.e., the output of the last
    // convolutional layer of the original model).
    const gradFunction = tf.grad(convOutput2ClassOutput);
    // Calculate the values of the last conv layer's output.
    const lastConvLayerOutputValues = subModel1.apply(x);
    // console.log(lastConvLayerOutputValues.dataSync())
    // Calculate the values of gradients of the class output w.r.t. the output
    // of the last convolutional layer.
    
    const gradValues = gradFunction(lastConvLayerOutputValues);
    // Pool the gradient values within each filter of the last convolutional
    // layer, resulting in a tensor of shape [numFilters].
    const pooledGradValues = tf.mean(gradValues, [0, 1, 2]);
    // Scale the convlutional layer's output by the pooled gradients, using
    // broadcasting.
    const scaledConvOutputValues =
        lastConvLayerOutputValues.mul(pooledGradValues);

    // Create heat map by averaging and collapsing over all filters.
    let heatMap = scaledConvOutputValues.mean(-1);

    // Discard negative values from the heat map and normalize it to the [0, 1]
    // interval.
    heatMap = heatMap.relu();
    heatMap = heatMap.div(tf.add(heatMap.max(), tf.tensor([1e-20], [], 'float32'))).expandDims(-1);
    

    // Up-sample the heat map to the size of the input image.
    heatMap = tf.image.resizeBilinear(heatMap, [x.shape[1], x.shape[2]]);

    // Apply an RGB colormap on the heatMap. This step is necessary because
    // the heatMap is a 1-channel (grayscale) image. It needs to be converted
    // into a color (RGB) one through this function call.
    heatMap = applyColorMap(heatMap);

    // To form the final output, overlay the color heat map on the input image.
    return heatMap.div(heatMap.max()).mul(255);
  });
}