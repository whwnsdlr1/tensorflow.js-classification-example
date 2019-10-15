<template>
<div class="body" :style="{width: `${width}px`}" @mouseenter="() => {mouseEntered = true;}">
  <div class="tool" :style="{flex: `0 0 ${toolHeight}px`}">
    <div class="wrap-stroke-width">
      <span>stroke width:&nbsp;&nbsp;</span>
      <input type="range" min="1" max="15" v-model="lineWidth" @change="listen__stroke_width__onchange" />
    </div>
    <div class="buttons">
      <button class="btn clear" title="clear" @click="clearCanvasRect" :disabled="points.length == 0" >X</button>
    </div>
  </div>
  <canvas ref="canvas"
    :style="{flex: `0 0 ${canvasHeight}px`}"
    @mousedown="listen__canvas__onmousedown"
    @mousemove="listen__canvas__onmousemove"
    @mouseup="listen__canvas__onmouseup"
    @mouseleave="listen__canvas__onmouseleave">
  </canvas>
  <div v-show="mouseEntered == false" class="layer">
    <span>{{ layerMsg }}</span>
  </div>
</div>
</template>

<script>
/* eslint-disable no-console */

export default {
  props: ['width', 'tool-height', 'canvas-height', 'layer-msg'],
  data: function () {
    return {
      paint: false,
      points: [],
      lineWidth: 9,
      mouseEntered: false
    }
  },
  methods: {
    listen__canvas__onmousedown: function (e) {
      const canvas = this.$refs['canvas']
      const boundingClientRect = canvas.getBoundingClientRect()
      this.paint = true
      this.points.push([e.pageX - boundingClientRect.x, e.pageY - boundingClientRect.y, true])
      this.redraw()
    },
    listen__canvas__onmousemove: function (e) {
      if (this.paint) {
        const canvas = this.$refs['canvas']
        const boundingClientRect = canvas.getBoundingClientRect()
        this.points.push([e.pageX - boundingClientRect.x, e.pageY - boundingClientRect.y, false, this.lineWidth])
        this.redraw()
      }
    },
    listen__canvas__onmouseup: function () {
      this.paint = false
    },
    listen__canvas__onmouseleave: function () {
      this.paint = false
    },
    listen__stroke_width__onchange: function () {
    },
    redraw: function () {
      const points = this.points
      if (points.length > 0) {
        let canvas = this.$refs['canvas']
        let context = canvas.getContext('2d', {alpha: false})
        context.clearRect(0, 0, context.canvas.width, context.canvas.height)

        context.strokeStyle = '#FFFFFF'
        context.lineJoin = 'round'

        for (let i = 1; i < points.length; i++) {
          const point = points[i]
          if (point[2] == true) continue
          
          context.lineWidth = point[3]
          const prePoint = points[i - 1]
          context.beginPath()
          context.moveTo(prePoint[0], prePoint[1])
          context.lineTo(point[0], point[1])
          context.closePath()
          context.stroke()
        }
      }
    },
    clearCanvasRect: function () {
      let canvas = this.$refs['canvas']
      let context = canvas.getContext('2d', {alpha: false})
      context.clearRect(0, 0, context.canvas.width, context.canvas.height)
      this.points = []
    },
    getData: function () {
      let canvas = this.$refs['canvas']
      let context = canvas.getContext('2d', {alpha: false})
      return context.getImageData(0, 0, context.canvas.width, context.canvas.height)
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
    this.points = []
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
}
div.wrap-stroke-width {
  display: flex;
  flex-direction: row;
  flex: 1 0 0;
  align-items: center;
}
div.wrap-stroke-width span {
  font-size: 12px;
}
div.wrap-stroke-width input[type=range] {
  position: relative;
  bottom: 1px;
  width: 80px;
  height: 6px;
  padding: 0px 0px 0px 0px;
  margin: 0px 0px 0px 0px;
  -webkit-appearance: none;
  border-radius: 3px;
  border: 1px solid rgb(180, 180, 180);
  background: #d3d3d3;
  outline: none;
  opacity: 0.7;
  -webkit-transition: .2s;
  transition: opacity .2s;
  box-sizing: border-box;
}
div.wrap-stroke-width input[type=range]::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 8px;
  height: 15px;
  background: rgb(0, 123, 255);
  border: 1px solid rgb(255, 255, 255);
  cursor: pointer;
}
div.wrap-stroke-width input[type=range]::-moz-range-thumb {
  width: 8px;
  height: 15px;
  background: rgb(0, 123, 255);
  border: 1px solid rgb(255, 255, 255);
  cursor: pointer;
}
.buttons {
  display: flex;
  flex-direction: row;
  padding: 3px 0px 3px 0px;
  overflow: hidden;
}
.btn.clear {
  font-size: 10px;
  color: rgb(0, 0, 0);
  cursor: pointer;
}
.btn[disabled] {
  color: rgb(80, 80, 80);
  background: rgb(160, 160, 160);
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
