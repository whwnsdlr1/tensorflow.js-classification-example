const SitemapPlugin = require('sitemap-webpack-plugin').default

module.exports = {
  publicPath: process.env.NODE_ENV === 'production'
  ? '/tensorflow.js-classification-example'
  : '/tensorflow.js-classification-example',
  outputDir: '../docs',
  devServer: {
    host: '0.0.0.0'
  },
  configureWebpack: {
    plugins: [
      new SitemapPlugin('https://whwnsdlr1.github.io/tensorflow.js-classification-example/', ['/'], {
        fileName: 'sitemap.xml',
        lastMod: true,
        changeFreq: 'monthly'
      })
    ]
  },
  productionSourceMap: false
}