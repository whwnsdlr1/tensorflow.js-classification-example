<template>
<div class="main">
  <title-bar :page="currentPath" @vue-move="listen__x__onmove" />
  <div class="content">
    <div class="inference">
      <h1>Demo<i>&nbsp;- Inference</i></h1>
      <div class="block">
        <div class="run input">
          <div class="title">Input</div>
          <div class="content">
            <vue-canvas v-if="currentPath == '/mnist'" ref="vue-canvas" :width='224' :tool-height='25' :canvas-height='224' :layer-msg="'draw!'" />
            <vue-upload-canvas v-if="currentPath == '/imagenet'" ref="vue-upload-canvas" :width='224' :tool-height='25' :canvas-height='224' :layer-msg="'upload!'" />
            <button ref="btn-inference-run">
              <span v-show="isRunning == false">run !!</span>
              <div v-show="isRunning == true" class=w-spinner><div class=spinner></div></div>
            </button>
          </div>
        </div>
        <div class="vb"><img src="@/assets/images/outline_double_arrow_black_48dp.png" /></div>
        <div class="run model">
          <div class="title">
            Model
          </div>
          <div class="content">
            <div class="w-view-model">
              <div class="view-model" ref="view-model">
              </div>
              <div class="buttons">
                <div class="btn refresh" title="refresh" @click="listen__view_model_refresh__onclick">&#x1f5d8;</div>
                <div class="btn help" title="help" @click="listen__view_model_help__onclick">&#63;</div>
              </div>
            </div>
          </div>
        </div>
        <div class="vb"><img src="@/assets/images/outline_double_arrow_black_48dp.png" /></div>
        <div class="run result">
          <div class="title">Result</div>
          <div class="content">
            <div>
              <h4>probability</h4>
              <bar-chart v-if="currentPath == '/mnist'" :chart-data="pageDef.result.chartData" :options="{width: 200, height: 150}" style="height:150px;width:200px;" />
              <horizontal-bar-chart v-if="currentPath == '/imagenet'" :chart-data="pageDef.result.chartData" :options="{width: 200, height: 150}" style="height:150px;width:200px;" />
            </div>
            <div>
              <h4><a href="#explain-grad-cam">grad-CAM</a></h4>
              <div style="border:1px solid rgba(0, 0, 0, 1)">
                <canvas ref="grad-cam-canvas" width=150 height=150 style="width:150px;height:150px" />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="training-data">
      <h1>{{ pageDef.trainingData.name }}<i>&nbsp;- training data</i></h1>
      <p v-html="pageDef.trainingData.html">
      </p>
    </div>
    <div v-if="pageDef.training != undefined" class="training">
      <h1>{{ pageDef.training.name }}<i>&nbsp;- tuning & learning</i></h1>
      <p v-html="pageDef.training.html">
      </p>
    </div>
    <div class="archetecture">
      <h1>{{ pageDef.archetecture.name }}<i>&nbsp; - network archetecture</i></h1>
      <table>
        <thead>
          <tr>
          <th v-for="(value, index) in pageDef.archetecture.data.table.head" :key="`arch-table-head-${index}`">
            {{ value }}
          </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(row, index) in pageDef.archetecture.data.table.body" :key="`arch-table-body-tr-${index}`" :class="{'odd': index % 2 == 1}">
            <td v-for="(value, index) in row" :key="`arch-table-body-td-${index}`">
              {{ value }}
            </td>
          </tr>
        </tbody>
      </table>
      <h4 v-for="(value, key, index) in pageDef.archetecture.data.comment" :key="`arch-comment-${index}`">
        {{`${key}: ${value}`}}
      </h4>
    </div>
    <div class="footnote">
      <h1>Footnote</h1>
      <h4 id="explain-grad-cam">Grad-CAM</h4>
      <p>
        Gradient-weighted Class Activation Mapping
        <br />
        &nbsp;&nbsp;ML models can be used as black boxes, but detailed tuning requires understanding.
        In particular, for the classification problem, it is necessary to identify what the model sees and determines such a decision.
        Methods for procuring these "visual plans" include occlusion map, Guided-Backpropagation, CAM, Grid-CAM etc. and in the case of the Grad-CAM, no structural changes and re-learning are required and the areas referred to are expressed to make a judgment. 
      </p>
    </div>
  </div>
</div>
</template>

<script>
/* eslint-disable no-console */
import TitleBar from '@/components/TitleBar'
import BarChart from '@/components/d3/BarChart'
import HorizontalBarChart from '@/components/d3/HorizontalBarChart'
import Canvas from '@/components/Canvas'
import UploadCanvas from '@/components/UploadCanvas'

import elementResizeEvent from 'element-resize-event'
import { AlexNet } from '@/js/3rdparty/NN-SVG/AlexNet.js'
import MISC from '@/js/miscellaneous.js'
import { gradClassActivationMap } from '@/js/3rdparty/tfjs-examples/gradClassActivationMap.js'
import path from 'path'

export default {
  components: {
    'title-bar': TitleBar,
    'bar-chart': BarChart,
    'horizontal-bar-chart': HorizontalBarChart,
    'vue-canvas': Canvas,
    'vue-upload-canvas': UploadCanvas
  },
  data: function () {
    return {
      currentPath: `/${path.basename(this.$route.path)}`,
      def: {
        '/mnist': {
          inference: {
            modelDefinition: {
              architecture_: [
                {height: 28, width: 28, depth: 1, filterHeight: 3, filterWidth: 3, rel_x: this.randConvPos(), rel_y: this.randConvPos()},
                {height: 28, width: 28, depth: 16, filterHeight: 3, filterWidth: 3, rel_x: this.randConvPos(), rel_y: this.randConvPos()},
                {height: 14, width: 14, depth: 32, filterHeight: 3, filterWidth: 3, rel_x: this.randConvPos(), rel_y: this.randConvPos()},
                {height: 7, width: 7, depth: 32, filterHeight: 1, filterWidth: 1, rel_x: this.randConvPos(), rel_y: this.randConvPos()}
              ],
              architecture2_: [40, 10]
            },
            model: {path: 'custom_cnn/model.json'}
          },
          trainingData: {
            name: 'MNIST',
            html: `&nbsp;&nbsp;MNIST database<i>(Modified National Institute of Standards and Technology database)</i>is the base of the numeric cursive image data.
                  <br />
                  &nbsp;&nbsp;The image is 28x28 size of gray scale consisting of 60000 learning data and 10000 test data. There are 10 classess from 0 to 9.
                  <br />
                  &nbsp;&nbsp;It is easy to classify, and the capacity of the required models are small. And there are big-scale benchmarks, which make it a good dataset for first-time machine-learning users.

                  <br />
                  &nbsp;&nbsp;Deep network architecture + augmentation +use ensembles ,you can get more than 99.79% accuracy. <i>(<a href="https://rodrigob.github.io/are_we_there_yet/build/classification_datasets_results.html#4d4e495354">MNIST - who is the best in MNIST</a>)</i>
                  `
          },
          training: {
            name: 'Training',
            html: `&nbsp;&nbsp;keras&tensorflow model is <a href="https://github.com/whwnsdlr1/tensorflow.js-classification-example/train/custom_cnn/model.py">https://github.com/whwnsdlr1/tensorflow.js-classification-example/train/custom_cnn/model.py</a> 
                 file learning code can be find in <a href="https://github.com/whwnsdlr1/tensorflow.js-classification-example/train/custom_cnn/train.py">https://github.com/whwnsdlr1/tensorflow.js-classification-example/train/custom_cnn/train.py</a>
                  <br /><br />
                  &nbsp;&nbsp;It has divided again learning data into 50000 chapters and 10000 pages of learning and verification data.
                  &nbsp;&nbsp;We learned from the hyperparameters below, for verification data was saved with the following hyperparameters.
                  <br />
                  &nbsp;&nbsp;&nbsp;&nbsp;optimizer: adam
                  <br />
                  &nbsp;&nbsp;&nbsp;&nbsp;loss: cross-entropy
                  <br />
                  &nbsp;&nbsp;&nbsp;&nbsp;learning-rate: 0.001
                  <br />
                  &nbsp;&nbsp;&nbsp;&nbsp;batch-size: 32
                  <br />
                  &nbsp;&nbsp;&nbsp;&nbsp;epochs: 100 // but with early stoppping, learning process stopped at epoch-17
                  <br />
                  &nbsp;&nbsp;i7-8700 CPU / tensorflow 2.0 were used to learning and took no more than three minutes.
                  &nbsp;&nbsp;The accuracy for the learning data of the final model was 0.9979, the verification data was 0.9886 and the test data was 0.9907.
                  `
          },
          archetecture: {
            name: 'Custom-CNN',
            data: require('@/assets/custom_cnn_archetecture.json')
          },
          result: {      
            chartData: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9].map(v => {return {name: v + '', value: 0}}),
            classNames: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
          }
        },
        '/imagenet': {
          inference: {
            modelDefinition: {
              architecture_: [
                {height: 224, width: 224, depth: 3, filterHeight: 3, filterWidth: 3, rel_x: this.randConvPos(), rel_y: this.randConvPos()},
                {height: 224, width: 224, depth: 16, filterHeight: 3, filterWidth: 3, rel_x: this.randConvPos(), rel_y: this.randConvPos()},
                {height: 112, width: 112, depth: 32, filterHeight: 1, filterWidth: 1, rel_x: this.randConvPos(), rel_y: this.randConvPos()},
                {height: 56, width: 56, depth: 16, filterHeight: 3, filterWidth: 3, rel_x: this.randConvPos(), rel_y: this.randConvPos()},
                {height: 56, width: 56, depth: 128, filterHeight: 1, filterWidth: 1, rel_x: this.randConvPos(), rel_y: this.randConvPos()},
                {height: 56, width: 56, depth: 16, filterHeight: 3, filterWidth: 3, rel_x: this.randConvPos(), rel_y: this.randConvPos()},
                {height: 56, width: 56, depth: 128, filterHeight: 1, filterWidth: 1, rel_x: this.randConvPos(), rel_y: this.randConvPos()},
                {height: 28, width: 28, depth: 32, filterHeight: 3, filterWidth: 3, rel_x: this.randConvPos(), rel_y: this.randConvPos()},
                {height: 28, width: 28, depth: 256, filterHeight: 1, filterWidth: 1, rel_x: this.randConvPos(), rel_y: this.randConvPos()},
                {height: 28, width: 28, depth: 32, filterHeight: 3, filterWidth: 3, rel_x: this.randConvPos(), rel_y: this.randConvPos()},
                {height: 28, width: 28, depth: 256, filterHeight: 1, filterWidth: 1, rel_x: this.randConvPos(), rel_y: this.randConvPos()},
                {height: 14, width: 14, depth: 64, filterHeight: 3, filterWidth: 3, rel_x: this.randConvPos(), rel_y: this.randConvPos()},
                {height: 14, width: 14, depth: 512, filterHeight: 1, filterWidth: 1, rel_x: this.randConvPos(), rel_y: this.randConvPos()},
                {height: 14, width: 14, depth: 64, filterHeight: 3, filterWidth: 3, rel_x: this.randConvPos(), rel_y: this.randConvPos()},
                {height: 14, width: 14, depth: 512, filterHeight: 3, filterWidth: 3, rel_x: this.randConvPos(), rel_y: this.randConvPos()},
                {height: 14, width: 14, depth: 128, filterHeight: 1, filterWidth: 1, rel_x: this.randConvPos(), rel_y: this.randConvPos()},
                {height: 14, width: 14, depth: 1000, filterHeight: 14, filterWidth: 14, rel_x: this.randConvPos(), rel_y: this.randConvPos()}
              ],
              architecture2_: [1000]
            },
            model: {path: 'darknet_tiny/model.json'}
          },
          trainingData: {
            name: 'Imagenet',
            html: `&nbsp;&nbsp;ImageNet consists of a total of 14M, class 21841, data set that is composed of various images from the Internet.
                 In machine learning, the term imagenet usually refers to the sub-data set corrected in ILSVRC2012<i>(Large Scale Visual Recognition Challenge 2012)</i> rather than the entire dataset.
                  For the IRSLV2012 data, there are 1000 classes, and the learning images are 1.2M images taken from the image net, and the verification and test data are collected from the Internet without overlap with the existing image net.
                  <br />
                  &nbsp;&nbsp;This dataset consists of a large amount of data for various classes, so it is often used for transfer learning to solve data-poor learning problems.
                 Transfer learning is a method to reduce generalization by learning first with image net and fine-tuning with the data in question, assuming that the method of expressing and extracting the characteristics of natal scene( picture, medical...)</i> if modality is similar.
                  `
          },
          training: {
            name: 'Training',
            html: `
                  &nbsp;&nbsp;Learning was not done directly and both the model structure and weight used Tiny Darknet. For more information, see a href="https://pjreddie.com/darknet/tiny-darknet/">https://pjreddie.com/darknet/tiny-darknet/</a>.

                  <br />
                  &nbsp;&nbsp;you can confirm darknet (only classify model) to keras model conversion code in<a href="https://github.com/whwnsdlr1/tensorflow.js-classification-example/train/darknet_tiny/convert.py">convert.py</a>
                  `
          },
          archetecture: {
            name: 'Tiny Darknet',
            data: require('@/assets/darknet_tiny_archetecture.json')
          },
          result: {      
            chartData: [0, 1, 2, 3, 4].map((v) => {return {name: v, value: 0}}),
            classNames: require('@/assets/darknet_imagenet_classname.json')
          }
        }
      },
      alexnet: undefined,
      model: undefined,
      isRunning: false,
      colors: ['#E6194B', '#F58231', '#FFE119', '#BFEF45', '#3CB44B', '#42D4F4', '#4363D8', '#911EB4', '#F032E6', '#A9A9A9']
    }
  },
  methods: {
    listen__x__onmove: function (path) {
      this.$router.push(`/tensorflow.js-classification-example${path}`)
      this.currentPath = path
    },
    listen__view_model__onresize: function () {
      if (this.alexnet != undefined) {
        const style = getComputedStyle(this.$refs['view-model'])
        this.alexnet.rendererResize(parseInt(style.width), parseInt(style.height))
      }
    },
    listen__view_model_refresh__onclick: function () {
      if (this.alexnet != undefined) {
        this.alexnet.refresh()
      }
    },
    listen__view_model_help__onclick: function () {
      let dom = MISC.createElement('DIV', {}, {})
      MISC.createElement('H3', {fontSize: '20px', marginBottom: '0px'}, {parent: dom, text: 'control'})
      MISC.createElement('HR', {}, {parent: dom})
      const styleSpan = {fontSize: '16px', lineHeight: 1.5}
      const data = {
        Orbit: 'left mouse / touch: one-finger move' ,
        Zoom: 'middle mouse, or mousewheel / touch: two-finger spread or squish',
        Pan: 'right mouse, or arrow keys / touch: two-finger move'
      }
      for (let key in data) {
        let div = MISC.createElement('DIV', {}, {parent: dom})
        MISC.createElement('SPAN', {...styleSpan, fontWeight: 'bold', paddingRight: '10px'}, {parent: div, text: `${key}:`})
        MISC.createElement('SPAN', styleSpan, {parent: div, text: data[key]})
      }
      MISC.createElement('H3', {fontSize: '20px', marginTop: '30px', marginBottom: '0px'}, {parent: dom, text: 'powered by NN SVG'})
      MISC.createElement('HR', {}, {parent: dom})
      for (let el of [{head: 'github', type: 'a', text:'https://github.com/alexlenail/NN-SVG'}]) {
        let div = MISC.createElement('DIV', {}, {parent: dom})
        MISC.createElement('SPAN', {...styleSpan, fontWeight: 'bold', paddingRight: '10px'}, {parent: div, text: `${el.head}:`})
        if (el.type == 'span')
          MISC.createElement('SPAN', styleSpan, {parent: div, text: el.text})
        else if (el.type == 'a')
          MISC.createElement('A', styleSpan, {parent: div, text: el.text, attrs: {href: el.text}})
        else if (el.type == 'mail')
          MISC.createElement('A', styleSpan, {parent: div, text: el.text, attrs: {href: `mailto:${el.text}`}})
      }
      this.$mModal.show('dialog', {
        dom: dom,
        buttons: [
          {
            title: 'confirm',
            class: ['green'],
            onclick: () => {
            }
          }
        ]
      })
    },
    listen__inference__onclick: function () {
      const Vue = this
      Vue.$refs['btn-inference-run'].disabled = true
      Vue.isRunning = true
      
      const tf = window.tf
      Vue.doubleRaf(async () => {
        try {
          tf.setBackend('cpu')
          if (Vue.model == undefined || Vue.model.name != Vue.currentPath) {
            if (Vue.pageDef.inference.model == undefined) throw new Error('no model file to load. upload model file first.')
            const btime = new Date()
            Vue.model = {name: Vue.currentPath, net: await tf.loadLayersModel(Vue.pageDef.inference.model.path)}
            Vue.$toasted.show(`elapsed time - load ${Vue.currentPath} model: ${new Date() - btime} ms`, {type: 'error', duration: 2000, position: 'bottom-center'})
          }
          if (Vue.model == undefined) throw new Error(`can't load model.`)
          
          if (Vue.currentPath == '/mnist') {
            const data = Vue.$refs['vue-canvas'].getData()
            const pixelArray0 = MISC.resizeImg(data.data, data.width, data.height, 28, 28)
            
            const pixelArray = new Float32Array(28 * 28)
            for (let i = 0; i < pixelArray.length; i++) {
              const k = i * 4
              pixelArray[i] = (pixelArray0[k] + pixelArray0[k + 1] + pixelArray0[k + 2]) / 765
            }
            let inputTensor = tf.tensor(pixelArray, [1, 28, 28, 1], 'float32')

            let btime = new Date()
            const resTensor = Vue.model.net.predict(inputTensor)
            Vue.$toasted.show(`elapsed time - predict: ${new Date() - btime} ms`, {type: 'error', duration: 2000, position: 'bottom-center'})
            const res = resTensor.dataSync()

            const sortedRes = [].slice.call(res).map((v, i) => [v, i]).sort((v1, v2) => v2[0] - v1[0])

            btime = new Date()
            const gradCamPixelData0 = gradClassActivationMap(Vue.model.net, sortedRes[0][1], inputTensor).dataSync()
            Vue.$toasted.show(`elapsed time - cal gradCAM: ${new Date() - btime} ms`, {type: 'error', duration: 2000, position: 'bottom-center'})
            let gradCamPixelData = new Array(28 * 28 * 4)
            for (let i = 0; i < 28 * 28; i++) {
              const k1 = i * 3
              const k2 = i * 4
              gradCamPixelData[k2] = gradCamPixelData0[k1]
              gradCamPixelData[k2 + 1] = gradCamPixelData0[k1 + 1]
              gradCamPixelData[k2 + 2] = gradCamPixelData0[k1 + 2]
              gradCamPixelData[k2 + 3] = 255
            }
            Vue.setGradCamCanvas(MISC.resizeImg(gradCamPixelData, 28, 28, 150, 150))

            const sortedColors = sortedRes.map((v, i) => [v[1], i]).sort((v1, v2) => v1[0] - v2[0]).map(v => Vue.colors[v[1]])
            Vue.pageDef.result.chartData = Array.prototype.slice.call(res).map((v, i) => {return {name: Vue.pageDef.result.classNames[i] + '', value: v, color: sortedColors[i]}})
          } else if (Vue.currentPath == '/imagenet') {
            const data = Vue.$refs['vue-upload-canvas'].getData()
            const pixelArray0 = MISC.resizeImg(data.data, data.width, data.height, 224, 224)
            
            const pixelArray = new Float32Array(224 * 224 * 3)
            for (let i = 0; i < pixelArray.length; i += 3) {
              const k = i  / 3 * 4
              pixelArray[i] = pixelArray0[k] / 255
              pixelArray[i + 1] = pixelArray0[k + 1] / 255
              pixelArray[i + 2] = pixelArray0[k + 2] / 255
            }
            let inputTensor = tf.tensor(pixelArray, [1, 224, 224, 3], 'float32')

            let btime = new Date()
            const resTensor = Vue.model.net.predict(inputTensor)
            Vue.$toasted.show(`elapsed time - predict: ${new Date() - btime} ms`, {type: 'error', duration: 2000, position: 'bottom-center'})
            const res = resTensor.dataSync()

            const sortedRes = [].slice.call(res).map((v, i) => [v, i]).sort((v1, v2) => v2[0] - v1[0])

            btime = new Date()
            const gradCamPixelData0 = gradClassActivationMap(Vue.model.net, sortedRes[0][1], inputTensor).dataSync()
            Vue.$toasted.show(`elapsed time - cal gradCAM: ${new Date() - btime} ms`, {type: 'error', duration: 2000, position: 'bottom-center'})
            let gradCamPixelData = new Array(224 * 224 * 4)
            for (let i = 0; i < 224 * 224; i++) {
              const k1 = i * 3
              const k2 = i * 4
              gradCamPixelData[k2] = gradCamPixelData0[k1]
              gradCamPixelData[k2 + 1] = gradCamPixelData0[k1 + 1]
              gradCamPixelData[k2 + 2] = gradCamPixelData0[k1 + 2]
              gradCamPixelData[k2 + 3] = 255
            }
            Vue.setGradCamCanvas(MISC.resizeImg(gradCamPixelData, 224, 224, 150, 150))

            Vue.pageDef.result.chartData = sortedRes.slice(0, 5).map((v, i) => {return {name: Vue.pageDef.result.classNames[v[1]] + '', value: v[0], color: Vue.colors[i]}})
          }
          else throw new Error('wrong page.')
        } catch (err) {
          console.log(err)
          Vue.$toasted.show(err, {type: 'error', duration: 2000, position: 'bottom-center'})
        } finally {
          Vue.$refs['btn-inference-run'].disabled = false
          Vue.isRunning = false
        }
      }, 100)
    },
    randConvPos: function () {
      return Math.random() * 0.8 - 0.4
    },
    argMax: function (array) {
      return [].map.call(array, (x, i) => [x, i]).reduce((r, a) => (a[0] > r[0] ? a : r))[1];
    },
    setGradCamCanvas: function (data) {
      const canvas = this.$refs['grad-cam-canvas']
      let context = canvas.getContext('2d', {alpha: false})
      context.clearRect(0, 0, context.canvas.width, context.canvas.height)
      if (data != undefined) {
        let imageData = context.createImageData(canvas.width, canvas.height)
        const lc = canvas.width * canvas.height * 4
        for (let i = 0; i < lc; i++) imageData.data[i] = data[i]
        context.putImageData(imageData, 0, 0)
      }
    },
    doubleRaf: function (callback) {
      requestAnimationFrame(() => {
        requestAnimationFrame(callback)
      })
    }
  },
  watch: {
    currentPath: function (currentPath) {
      if (this.alexnet != undefined) {
        if (currentPath == '/mnist' || currentPath == '/imagenet') this.alexnet.redraw(this.def[currentPath].inference.modelDefinition)
      }
      this.isRunning = false
      this.def[currentPath].result.chartData = []
      this.setGradCamCanvas()
    }
  },
  computed: {
    pageDef: function () {
      return this.def[this.currentPath]
    }
  },
  mounted () {
    this.setGradCamCanvas()
    const Vue = this
    let idInterval = setInterval(() => {
      if (window.THREE != undefined) {
        require('@/js/3rdparty/NN-SVG/OrbitControls.js')
        Vue.alexnet = AlexNet(window.THREE, Vue.$refs['view-model'])
        Vue.alexnet.redraw(this.def[this.currentPath].inference.modelDefinition)
        elementResizeEvent(Vue.$refs['view-model'], Vue._.debounce(Vue.listen__view_model__onresize, 10))
        clearInterval(idInterval)
      }
    }, 500)
    Vue.$refs['btn-inference-run'].onclick = Vue._.debounce(Vue.listen__inference__onclick, 100)
  },
  beforeDestory () {
    elementResizeEvent.unbind(this.$refs['view-model'])
  }
}
</script>

<style>
.main > .content p {
  font-size: 16px;
}
.main > .content p > i {
  font-size: 12px;
}
</style>
<style scoped>
h1 {
  font-size: 30px;
  margin-bottom: 0px;
}
h1 > i {
  font-size: 20px;
  color: rgb(110, 110, 110);
}

div.main {
  display: flex;
  flex-direction: column;
  height: 100%;
  width: 100%;
}
div.main > div.content {
  flex: 1 0 0;
  overflow-y: auto;
  background: rgb(230, 230, 230);
}
div.main > div.content > div {
   padding: 0px 30px;
}
div.main > div.content > div:not(:first-child) {
   margin-top: 40px;
}

.inference .block {
   display:flex;
   flex-direction:row;
   height:400px;
   justify-content: space-evenly;
}

.inference .block .vb {
  display: flex;
  flex: 0 0 40px;
  min-width: 0px;
  align-items: center;
  justify-content: center;
}
.inference .block .vb img {

  width: 100%;
}

.inference .block .run {
  display: flex;
  flex-direction: column;
}

.inference .block .run .title {
  display: flex;
  font-size: 20px;
  height: 40px;
  align-items: center;
  justify-content: center;
}

.inference .block .run .content {
  display: flex;
  flex-direction: column;
  font-size: 20px;
  flex: 1 0 0;
  min-height: 0px;
  overflow: hidden;
  align-items: center;
}

.inference .block .run.input {
  flex: 0 0 260px;
  min-width: 0px;
}
.inference .block .run.model {
  flex: 1 0 0;
  min-width: 0px;
}
.inference .block .run.result {
  flex: 0 0 260px;
}

.inference .block .run.input button {
  height: 30px;
  width: 224px;
  margin-top: 5px;
  display: inline-block;
  zoom: 1;
  *display: inline;
  vertical-align: baseline;
  outline: none;
  cursor: pointer;
  text-align: center;
  text-decoration: none;
  font: 14px/100% Arial, Helvetica, sans-serif;
  padding: 0;
  text-shadow: 0 1px 1px rgba(0,0,0,.3);
  border-radius: .5em;
  box-shadow: 0 1px 2px rgba(0,0,0,.2);
  border: solid 1px #b7b7b7;
  background: #fff;
  background: -webkit-gradient(linear, left top, left bottom, from(#fff), to(#ededed));
  background: -moz-linear-gradient(top,  #fff,  #ededed);
}
.inference .block .run.input button:hover {
    text-decoration: none;
    background: #ededed;
    background: -webkit-gradient(linear, left top, left bottom, from(#fff), to(#dcdcdc));
    background: -moz-linear-gradient(top,  #fff,  #dcdcdc);
}
.inference .block .run.input button:active {
    position: relative;
    top: 1px;
    color: #999;
    background: -webkit-gradient(linear, left top, left bottom, from(#ededed), to(#fff));
    background: -moz-linear-gradient(top,  #ededed,  #fff);
}
.inference .block .run.input button:disabled {
  border-color: rgb(120, 120, 120);
  color: rgb(210, 210, 210);
  background: #e0e0e0;
  cursor: default;
}

.inference .block .run.model .content .w-view-model {
  display: block;
  height: 250px;
  width: 100%;
  height: 250px;
  border: 1px solid black;
}

.inference .block .run.model .content .view-model {
  display: block;
  width: 100%;
  height: 100%;
}

.inference .block .run.model .content .w-view-model .buttons {
  position: absolute;
  display: flex;
  flex-direction: row;
  top: 5px;
  right: 15px;
}

.inference .block .run.model .content .w-view-model .buttons > .btn {
  display: flex;
  background: rgba(190, 190, 190, 0.2);
  border: 1px solid rgba(120, 120, 120, 0.5);
  width: 25px;
  height: 25px;
  border-radius: 12px;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  -webkit-user-select: none; /* Safari */
  -khtml-user-select: none; /* Konqueror HTML */
    -moz-user-select: none; /* Firefox */
    -ms-user-select: none; /* Internet Explorer/Edge */
        user-select: none; /* Non-prefixed version, currently
                              supported by Chrome and Opera */
}

.inference .block .run.model .content .w-view-model .buttons > .btn:hover {
  background: rgba(190, 190, 190, 0.8);
}

.inference .block .run.model .content .w-view-model .buttons > .btn.refresh {
  font-size: 18px;
  margin-right: 8px;
}
.inference .block .run.model .content .w-view-model .buttons > .btn.help {
  font-size: 15px;
}

.inference .block .run.result .content h4 {
  font-size: 14px;
  margin: 0px;
}
.inference .block .run.result .content > div {
  display: flex;
  flex-direction: column;
  align-items: center;
}
.inference .block .run.result .content > div:nth-child(2) {
  margin-top: 20px;
}
.archetecture h4 {
  font-size: 16px;
  margin: 2px;
}
.archetecture table {
  margin-top: 10px;
  margin-bottom: 10px;
}
.archetecture table td {
  padding: 5px 15px;
  font-size: 12px;
}
.archetecture table thead th {
  background: #8888AA;
  color: white;
  padding: 5px 15px;
  font-size: 14px;
  font-weight: normal;
}
.archetecture table tr.odd {
  background: #F0F0FF;
}
.footnote h4 {
  margin: 10px 0px 0px 0px;
}
.footnote p {
  margin: 5px 0px 0px 15px;
}

.w-spinner {
  top: 0px;
  margin: 0px;
  padding: 0px;
}
</style>
