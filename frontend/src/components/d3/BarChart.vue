<template>
<div style="position:relative;display:block;">
</div>
</template>
<script>
import * as d3 from 'd3'
import d3Tip from 'd3-tip'
export default {
  props: ['chartData', 'options'],
  data: function () {
    const margin = {top: 5, right: 5, bottom: 20, left: 25}
    const width = this.options.width - margin.left - margin.right
    const height = this.options.height - margin.top - margin.bottom;
    return {
      margin,
      width,
      height,
      svg: undefined,
      tip: undefined,
      x: undefined,
      axisX: undefined,
      y: undefined,
      axisY: undefined
    }
  },
  methods: {
    update: function (data) {
      const Vue = this

      // X axis
      Vue.x.domain(data.map(function(d) { return d.name }))
      Vue.axisX.call(d3.axisBottom(Vue.x))

      // Add Y axis
      Vue.y.domain([0, 1])
      Vue.axisY.call(d3.axisLeft(Vue.y).ticks(2))  

      let u = Vue.svg.selectAll('rect')
        .data(data)

      u.enter()
        .append('rect')
        .on('mouseover', Vue.tip.show)
        .on('mouseout', Vue.tip.hide)
        .merge(u)
        .transition().duration(300)
          .attr('class', 'bar')
          .attr('x', function (d) { return Vue.x(d.name) })
          .attr('y', function (d) { return Vue.y(d.value) })
          .attr('width', Vue.x.bandwidth())
          .attr('height', function (d) { return Vue.height - Vue.y(d.value) })
          .attr('fill', function (d) { return d.color != undefined ? d.color : '#69b3a2' })
    }
  },
  watch: {
    chartData: function (chartData) {
      this.update(chartData)
    }
  },
  mounted () {
    this.svg = d3.select(this.$el)
      .append('svg')
        .attr('width', this.width + this.margin.left + this.margin.right)
        .attr('height', this.height + this.margin.top + this.margin.bottom)
      .append('g')
        .attr('transform',
              `translate(${this.margin.left},${this.margin.top})`)

    this.tip = d3Tip()
      .attr('class', 'd3-tip')
      .offset([-10, 0])
      .html(function(d, a) {
        return `<strong>${a}</strong>: <span style='color:red'>${d.value.toFixed(3)}</span>`
      })
    this.svg.call(this.tip)

    // X axis
    this.x = d3.scaleBand()
      .range([0, this.width])
      .padding(0.2)
    this.axisX = this.svg.append('g')
      .attr('transform', `translate(0,${this.height})`)

    // Add Y axis
    this.y = d3.scaleLinear()
      .range([this.height, 0])
    this.axisY = this.svg.append('g')

    const data = this.chartData
    this.update(data)
  }
}
</script>

<style>
.bar:hover {
  fill: red;
}
.d3-tip {
  line-height: 1;
  font-weight: bold;
  padding: 12px;
  background: rgba(0, 0, 0, 0.8);
  color: #fff;
  border-radius: 2px;
}

.d3-tip:after {
  box-sizing: border-box;
  display: inline;
  font-size: 10px;
  width: 100%;
  line-height: 1;
  color: rgba(0, 0, 0, 0.8);
  content: "\25BC";
  position: absolute;
  text-align: center;
}

.d3-tip.n:after {
  margin: -1px 0 0 0;
  top: 100%;
  left: 0;
}
</style>