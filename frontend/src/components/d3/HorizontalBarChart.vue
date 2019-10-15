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
    const margin = {top: 5, right: 10, bottom: 20, left: 50}
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
      Vue.x.domain([0, 1])
      Vue.axisX.call(d3.axisBottom(Vue.x).ticks(2))

      // Add Y axis
      Vue.y.domain(data.map(function(d) { return d.name }))
      Vue.axisY.call(d3.axisLeft(Vue.y).tickFormat(function (str) { return str.length > 6? str.slice(0, 5) + '...' : str }))
      /*
        .selectAll('text')
          .attr("transform", "translate(-5,-5)rotate(-30)")
          .style("text-anchor", "end");
      */
      let u = Vue.svg.selectAll('rect')
        .data(data)

      u.enter()
        .append('rect')
        .on('mouseover', Vue.tip.show)
        .on('mouseout', Vue.tip.hide)
        .merge(u)
        .transition().duration(300)
          .attr('class', 'bar')
          .attr('x', Vue.x(0.01))
          .attr('y', function (d) { return Vue.y(d.name) })
          .attr('height', Vue.y.bandwidth())
          .attr('width', function (d) { return Vue.x(d.value) })
          .attr('fill', function (d) { return d.color })
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
      .html(function(d) {
        return `<strong>${d.name}</strong>: <span style='color:red'>${d.value.toFixed(3)}</span>`
      })
    this.svg.call(this.tip)

    this.x = d3.scaleLinear()
      .range([0, this.width])
    this.axisX = this.svg.append('g')
      .attr('transform', `translate(0,${this.height})`)

    this.y = d3.scaleBand()
      .range([0, this.height])
      .padding(0.5)
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