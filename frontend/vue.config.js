module.exports = {
  publicPath: process.env.NODE_ENV === 'production'
  ? '/tensorflow.js-classification-example'
  : '/tensorflow.js-classification-example',
  outputDir: '../docs',
  devServer: {
    host: '0.0.0.0'
  },
  productionSourceMap: false
}