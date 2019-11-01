<template>
<div class="body" :style="{width: `${width}px`}" @mouseenter="() => {mouseEntered = true;}">
  <div class="tool" :style="{flex: `0 0 ${toolHeight}px`}">
    <div class="buttons">
      <button ref="btn-upload" class="btn upload" title="upload" @click="uploadCanvas" >&#x2191;</button>
    </div>
    <input ref="input-upload" type="file" accept=".png,.jpg,.bmp" @change="listen__file__onchange" />
  </div>
  <canvas ref="canvas"
    :style="{flex: `0 0 ${canvasHeight}px`}" >
  </canvas>
  <div v-show="mouseEntered == false" class="layer">
    <span>{{ layerMsg }}</span>
  </div>
</div>
</template>

<script>
/* eslint-disable no-console */

export default {
  props: ['align-method', 'width', 'tool-height', 'canvas-height', 'layer-msg'],
  data: function () {
    return {
      mouseEntered: false
    }
  },
  methods: {
    listen__file__onchange: async function (e) {
      const Vue = this
      Vue.$refs['btn-upload'].disabled = true

      try {
        if (e.target.files.length == 1) {
          const file = e.target.files[0]
          if(file.type.match('image.*')) {
            const dataUrl = await Vue.readFile(file)
            
            let canvas = Vue.$refs['canvas']
            let context = canvas.getContext('2d', {alpha: false})
            let img = new Image()
            img.onload = () => {
              let tempCanvas = document.createElement('canvas')
              tempCanvas.width = img.naturalWidth
              tempCanvas.height = img.naturalHeight
              let tempContext = tempCanvas.getContext('2d')
              tempContext.drawImage(img, 0, 0, img.naturalWidth, img.naturalHeight)
              const imageData = tempContext.getImageData(0, 0, img.naturalWidth, img.naturalHeight)
              context.putImageData(Vue.alignImage(imageData, Vue.width, Vue.canvasHeight), 0, 0)
            }
            img.src = dataUrl
          }
        }
      } finally {
        Vue.$refs['btn-upload'].disabled = false
      }
    },
    readFile: function (file) {
      return new Promise((resolve) => {
        let reader = new FileReader()
        reader.onload = async function (e) {
          resolve(e.target.result)
        }
        reader.readAsDataURL(file)
      })
    },
    resizeImg: function (pixelData, width, height, dstWidth, dstHeight) {
      var canvasCopy = document.createElement('canvas')
      var copyContext = canvasCopy.getContext('2d')
      var canvasCopy2 = document.createElement('canvas')
      var copyContext2 = canvasCopy2.getContext('2d')
      canvasCopy.width = width;
      canvasCopy.height = height;
      copyContext.putImageData(new ImageData(new Uint8ClampedArray(pixelData), width, height), 0, 0)

      // init
      canvasCopy2.width = dstWidth
      canvasCopy2.height = dstHeight
      copyContext2.drawImage(canvasCopy, 0, 0, canvasCopy.width, canvasCopy.height, 0, 0, canvasCopy2.width, canvasCopy2.height)
      return copyContext2.getImageData(0, 0, dstWidth, dstHeight).data
    },
    alignLetterboxImage: function (im, w, h) {
      let newW, newH
      if (w / im.width < h / im.height) {
        newW = w
        newH = parseInt(im.height * w / im.width)
      } else {
        newH = h
        newW = parseInt(im.width * h / im.height)
      }
      let resized = this.resizeImg(im.data, im.width, im.height, newW, newH)
      let boxed = new Uint8ClampedArray(w * h * 4)
      for (let row = 0; row < h; row++) {
        const rowp = row * w * 4
        for (let col = 0; col < w; col++) {
          const colp = rowp + col * 4
          boxed[colp] = 127
          boxed[colp + 1] = 127
          boxed[colp + 2] = 127
          boxed[colp + 3] = 255
        }
      }
      
      const t = parseInt((h - newH) / 2)
      const l = parseInt((w - newW) / 2)
      const erow = t + newH
      const ecol = l + newW
      for (let row = t; row < erow; row++) {
        const rowp1 = row * w * 4
        const rowp2 = (row - t) * newW * 4
        for (let col = l; col < ecol; col++) {
          let colp1 = rowp1 + col * 4
          let colp2 = rowp2 + (col - l) * 4
          boxed[colp1] = resized[colp2]
          boxed[colp1 + 1] = resized[colp2 + 1]
          boxed[colp1 + 2] = resized[colp2 + 2]
          boxed[colp1 + 3] = resized[colp2 + 3]
        }
      }
      return new ImageData(boxed, w, h)
    },
    alignDefaultImage: function (im, w, h) {
      let resized = this.resizeImg(im.data, im.width, im.height, w, h)
      return new ImageData(resized, w, h)
    },
    uploadCanvas: function () {
      let canvas = this.$refs['canvas']
      let context = canvas.getContext('2d', {alpha: false})
      context.clearRect(0, 0, context.canvas.width, context.canvas.height)
      this.$refs['input-upload'].click()
    },
    getData: function () {
      let canvas = this.$refs['canvas']
      let context = canvas.getContext('2d', {alpha: false})
      return context.getImageData(0, 0, context.canvas.width, context.canvas.height)
    }
  },
  computed: {
    alignImage: function () {
      if (this.alignMethod == 'letterbox')
        return this.alignLetterboxImage
      else
        return this.alignDefaultImage
    }
  },
  mounted () {
    const canvas = this.$refs['canvas']
    canvas.getContext('2d', {alpha: false})
    const styleCanvas = getComputedStyle(canvas)
    const widthCanvas = styleCanvas.width
    const heightCanvas = styleCanvas.height
    
    canvas.width = parseInt(widthCanvas)
    canvas.height = parseInt(heightCanvas)
  }
}
</script>

<style scoped>
div.body {
  display: flex;
  flex-direction: column;
  box-shadow: 3px 3px 9px rgba(20, 20, 20, 0.5);
}
canvas {
  width: 100%;
}
div.tool {
  display: flex;
  flex-direction: row;
  min-height: 0;
  border: 1px solid rgb(80, 80, 80);
  padding: 0px 5px;
  justify-content: center;
  overflow: hidden;
}
.buttons {
  display: flex;
  flex-direction: row;
  padding: 3px 0px 3px 0px;
  overflow: hidden;
}
.btn.upload {
  font-size: 10px;
  color: rgb(0, 0, 0);
  cursor: pointer;
  padding: 0px 30px;
}
.btn[disabled] {
  color: rgb(80, 80, 80);
  background: rgb(160, 160, 160);
}

input[type='file'] {
  position: absolute;
  visibility: hidden;
}
div.layer {
  display: flex;
  left: 0px;
  top: 0px;
  width: 100%;
  height: 100%;
  justify-content: center;
  align-items: center;
  font-size: 20px;
  background: rgba(255, 255, 255, 0.8);
}
</style>
