# tensorflow.js-classification-example

This is a client web application to demonstrate a simple deployment of a classification network using tensorflow.js
<br />
currently test available on model trained by MNIST, CIFAR-100 and ImageNet.
<br />
<br />
always welcome to issue & PR to fix the awkward and wrong parts of the text and complement for the lack of content.
<br />
edit the value of the html-key in /frontend/src/assets/strings/*.json.
<br />
String elements in the array are combined with line breaks and can contain html tags within the string.
<br />
<br />
본문 중 어색한 부분, 잘못된 부분에 대한 내용 수정과 부족한 내용 보충을 위한 issue & PR은 언제나 환영입니다.
<br />
/frontend/src/assets/strings/*.json의 html-key의 value를 편집하면 됩니다.
<br />
배열의 문자열 엘리먼트들은 줄바꿈으로 결합되며 문자열안에 html 태그를 포함 할 수 있습니다.


## Demo
you can online demo in [https://whwnsdlr1.github.io/tensorflow.js-classification-example](https://whwnsdlr1.github.io/tensorflow.js-classification-example).
<br />
or
<br />
install project as below
```
git clone https://github.com/whwnsdlr1/tensorflow.js-classification-example
cd tensorflow.js-classification-example/frontend
yarn install
yarn run serve
```
and access to http://localhost:port/tensorflow.js-classification-example

## Usage
1. draw or upload image.
2. run !

## Browser support - (tested)
- Google Chrome 77+
- Mozilla FireFox 68+

## Project setup
### Customize configuration
See [Configuration Reference](https://cli.vuejs.org/config/).

## Third-party libraries
### Dependencies
- vue: [https://github.com/vuejs/vue](https://github.com/vuejs/vue)
- tfjs-examples: [https://github.com/tensorflow/tfjs-examples](https://github.com/tensorflow/tfjs-examples)
- darknet: [https://pjreddie.com/darknet/](https://pjreddie.com/darknet/)
- d3: [https://github.com/d3/d3](https://github.com/d3/d3)
- d3-tip: [https://github.com/caged/d3-tip](https://github.com/arian/pngjs)
- element-resize-event: [https://github.com/KyleAMathews/element-resize-event](https://github.com/KyleAMathews/element-resize-event)
- vue-lodash: [https://github.com/Ewocker/vue-lodash](https://github.com/Ewocker/vue-lodash)
- vue-toasted: [https://github.com/shakee93/vue-toasted](https://github.com/shakee93/vue-toasted)

### Dev-Dependencies
- @vue/cli-plugin-babel
- @vue/cli-plugin-eslint
- @vue/cli-service
- babel-eslint
- eslint
- eslint-plugin-vue
- vue-template-compiler

## used sources
### dataset
- [MNIST](http://yann.lecun.com/exdb/mnist/)
- [CIFAR](https://www.cs.toronto.edu/~kriz/cifar.html)
- [ImageNet](http://www.image-net.org/)
### images
- [https://wikimedia.org/api/rest_v1/media/math/render/svg/bdc1f8eaa8064d15893f1ba6426f20ff8e7149c5](https://wikimedia.org/api/rest_v1/media/math/render/svg/bdc1f8eaa8064d15893f1ba6426f20ff8e7149c5)