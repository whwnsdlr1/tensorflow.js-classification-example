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
        &nbsp;&nbsp;ML model은 블랙박스로 사용할 수 있지만 세밀한 튜닝을 위해서는 이해가 필요하다.
        특히 classification 문제의 경우 모델이 도대체 무엇을 보고 그런 결정을 판단하는지 확인 할 필요가 있다.
        이런 "visual explanations"을 producing하는 방법은 occlusion map, Guided-Backpropagation, CAM, Grad-CAM등이 있고 Grad-CAM의 경우 구조변경과 재학습이 필요 없으며 판단을 내리기 위해 참고한 영역을 표현 할 수 있다.  
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
            html: `&nbsp;&nbsp;MNIST database<i>(Modified National Institute of Standards and Technology database)</i>는 숫자 필기체 이미지 데이터베이스 이다.
                  <br />
                  &nbsp;&nbsp;이미지는 28 x 28 사이즈의 gray scale이며 학습 데이터 60000장, 테스트 데이터 10000장으로 구성 되어있다. 클래스는 0 부터 9까지 총 10개 이다.
                  <br />
                  &nbsp;&nbsp;분류 난이도가 쉬운 편이고 필요한 모델의 용량도 작은 편이며 오랫동안 축척된 벤치마크가 있어서 처음 머신러닝을 접하는 사람들이 이용하기 좋은 데이터셋이다.
                  <br />
                  &nbsp;&nbsp;깊은 네트워크 구조 + augmentation + 앙상블들을 이용하면 99.79% 이상의 정확도 까지 얻을 수 있다.<i>(<a href="https://rodrigob.github.io/are_we_there_yet/build/classification_datasets_results.html#4d4e495354">MNIST - who is the best in MNIST</a>)</i>
                  `
          },
          training: {
            name: 'Training',
            html: `&nbsp;&nbsp;keras&tensorflow를 이용한 모델 정의는 <a href="https://github.com/whwnsdlr1/tensorflow.js-classification-example/train/custom_cnn/model.py">https://github.com/whwnsdlr1/tensorflow.js-classification-example/train/custom_cnn/model.py</a> 파일에
                  학습 코드는 <a href="https://github.com/whwnsdlr1/tensorflow.js-classification-example/train/custom_cnn/train.py">https://github.com/whwnsdlr1/tensorflow.js-classification-example/train/custom_cnn/train.py</a>에서 찾을 수 있다.
                  <br /><br />
                  &nbsp;&nbsp;60000장의 학습 데이터를 다시 50000장과 10000장의 학습, 검증 데이터로 나눴다.
                  &nbsp;&nbsp;아래의 하이퍼파리미터로 학습 하였고 검증 데이터에 대해서 가장 낮은 loss를 가지는 epoch 모델을 저장하였다.
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
                  &nbsp;&nbsp;학습에는 i7-8700 CPU / tensorflow 2.0이 사용되었고 3분에 채 안걸렸다.
                  &nbsp;&nbsp;최종 모델의 학습 데이터에 대한 accuracy는 0.9979, 검증 데이터는 0.9886, 테스트 데이터는 0.9907였다.
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
            html: `&nbsp;&nbsp;이미지넷은 인터넷에 있는 다양한 이미지들을 모아서 만든 데이터 셋으로 총 이미지 14M, 클래스 21841로 구성 되어있다.
                  통상 머신러닝에서 이미지넷이라고 하면 전체 데이터셋가 아닌 ILSVRC2012<i>(Large Scale Visual Recognition Challenge 2012)</i>에서 정제한 하위 데이터셋을 의미한다.
                  IRSLV2012 데이터의 경우 클래스는 1000개 이며 학습 이미지는 이미지넷에서 가져온 이미지 1.2M개, 검증 및 테스트 데이터는 기존 이미지넷과 겹치지 않는 이미지들을 인터넷에서 수집하였다.
                  <br />
                  &nbsp;&nbsp;이 데이터셋은 다양한 클래스에 대해서 많은 양의 데이터로 구성 되어 있으므로 데이터가 부족한 학습 문제 해결을 위한 transfer learning에 많이 이용되는 데이터셋이다.
                  transper learning은 모달리티가 유사하다면<i>(natural scene, picture, medical...)</i> 특징을 표현, 추출하는 방법이 비슷할 것이라고 가정하여 이미지넷으로 먼저 학습하고 문제의 데이터로 파인튜닝하여 일반화에러를 줄이는 방법이다.
                  `
          },
          training: {
            name: 'Training',
            html: `
                  &nbsp;&nbsp;학습은 직접하지 않았고 모델 구조 및 weight 모두 Tiny Darknet을 사용하였다. 자세한 내용은 <a href="https://pjreddie.com/darknet/tiny-darknet/">https://pjreddie.com/darknet/tiny-darknet/</a>에서 볼 수 있다.
                  <br />
                  &nbsp;&nbsp;darknet (only classify model) to keras model 변환 코드는 <a href="https://github.com/whwnsdlr1/tensorflow.js-classification-example/train/darknet_tiny/convert.py">convert.py</a>에서 확인 할 수 있다.
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
