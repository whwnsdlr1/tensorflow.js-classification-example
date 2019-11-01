<template>
<div class="body">
  <div class="dataset">
    <div :class="{active: page == '/mnist'}" @click="() => {this.$emit('vue-move', '/mnist')}">
      <div class="wcheck">
        <img v-show="page == '/mnist'" class="check" src="@/assets/icons/outline_done_white_24dp.png" />
      </div>
      <span>MNIST</span>
    </div>
    <div :class="{active: page == '/cifar'}" @click="() => {this.$emit('vue-move', '/cifar')}">
      <div class="wcheck">
        <img v-show="page == '/cifar'" class="check" src="@/assets/icons/outline_done_white_24dp.png" />
      </div>
      <span>CIFAR</span>
    </div>
    <div :class="{active: page == '/imagenet'}" @click="() => {this.$emit('vue-move', '/imagenet')}">
      <div class="wcheck">
        <img v-show="page == '/imagenet'" class="check" src="@/assets/icons/outline_done_white_24dp.png" />
      </div>
      <span>ImageNet</span>
    </div>
  </div>
  <div class="buttons">
    <div class="btn" title="change language" @click="listen__lang__onclick"><span>{{ lang == 'EN' ? 'KO' : 'EN' }}</span></div>
    <a href="https://github.com/whwnsdlr1/tensorflow.js-classification-example" style="line-height:0"><img class="btn github" src="@/assets/icons/GitHub-Mark-Light-32px.png" title="github"/></a>
    <img v-show="fullscreen == false" class="btn" src="@/assets/icons/outline_fullscreen_white_24dp.png" title="maxmize" @click="listen__fullscreen__onclick" />
    <img v-show="fullscreen == true" class="btn" src="@/assets/icons/outline_fullscreen_exit_white_24dp.png" title="minimize" @click="listen__fullscreen__onclick" />
    <img class="btn" src="@/assets/icons/outline_help_outline_white_24dp.png" title="help" @click="listen__help__onclick" />
  </div>
</div>
</template>

<script>
/* eslint-disable no-console */
import MISC from '@/js/miscellaneous.js'
export default {
  props: ['page', 'lang'],
  data: function () {
    return {
      fullscreen: false
    }
  },
  methods: {
    listen__help__onclick: function () {
      let dom = MISC.createElement('DIV', {}, {})
      MISC.createElement('H3', {fontSize: '20px', marginBottom: '0px'}, {parent: dom, text: 'tensorflow.js'})
      MISC.createElement('HR', {}, {parent: dom})
      const tf = window.tf
      const styleSpan = {fontSize: '16px', lineHeight: 1.5}
      for (let key in tf.version) {
        let div = MISC.createElement('DIV', {}, {parent: dom})
        MISC.createElement('SPAN', {...styleSpan, fontWeight: 'bold', paddingRight: '10px'}, {parent: div, text: `${key}:`})
        MISC.createElement('SPAN', styleSpan, {parent: div, text: tf.version[key]})
      }
      MISC.createElement('H3', {fontSize: '20px', marginTop: '30px', marginBottom: '0px'}, {parent: dom, text: 'used library'})
      MISC.createElement('HR', {}, {parent: dom})
      let div = MISC.createElement('DIV', {}, {parent: dom})
      MISC.createElement('SPAN', styleSpan, {parent: div, text: 'please see the readme file on github.'})
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
    listen__fullscreen__onclick: function () {
      if (this.fullscreen == true) {
        if (document.mozCancelFullScreen) {
          document.mozCancelFullScreen()
        } else if (document.webkitExitFullscreen) {
          document.webkitExitFullscreen()
        }
        this.fullscreen = false
      }
      else {
        if (document.body.mozRequestFullScreen) {
          document.body.mozRequestFullScreen()
        } else if (document.body.webkitRequestFullscreen) {
          document.body.webkitRequestFullScreen()
        }
        this.fullscreen = true
      }
    },
    listen__lang__onclick: function () {
      this.$emit('vue-lang-tochange', {})
    }
  },
  mounted () {
  }
}
</script>

<style scoped>
div.body {
  display: flex;
  flex-direction: row;
  flex: 0 0 35px;
  background: rgb(36, 41, 46);
  align-items: center;
  justify-content: space-between;
  padding: 0px 20px;
  border-bottom: 1px solid rgb(80, 80, 80);
}
div.body * {
  -webkit-user-select: none; /* Safari */
    -khtml-user-select: none; /* Konqueror HTML */
      -moz-user-select: none; /* Firefox */
      -ms-user-select: none; /* Internet Explorer/Edge */
          user-select: none; /* Non-prefixed version, currently
                                supported by Chrome and Opera */
}
.dataset {
  display: flex;
  flex-direction: row;
  align-items: center;
}
.dataset > div {
  display: flex;
  flex-direction: row;
  height: 100%;
  align-items: center;
  padding: 3px 5px;
  margin: 0px;
}
.dataset > div.active {
  pointer-events: none;
  color: rgb(30, 30, 30);
  background: rgb(190, 190, 190);
  box-shadow: 1px 1px 1px rgba(255, 255, 255, 0.5) inset;
}
.dataset > div:not(.active) {
  cursor: pointer;
  color: rgb(230, 230, 230);
  background: rgb(120, 120, 120);
  box-shadow: 1px 1px 1px rgba(255, 255, 255, 0.5);
}
.dataset > div:not(.active):hover {
  color: rgb(30, 30, 30);
  background: rgb(190, 190, 190);
  box-shadow: 1px 1px 1px rgba(255, 255, 255, 0.5) inset;
}
.dataset > div:first-child {
  padding-left: 10px;
  padding-right: 5px;
  border-top-left-radius: 9px;
  border-bottom-left-radius: 9px;
}
.dataset > div:not(:first-child) {
  border-left: 1px solid rgb(0, 0, 0);
}
.dataset > div:last-child {
  padding-left: 5px;
  padding-right: 10px;
  border-top-right-radius: 9px;
  border-bottom-right-radius: 9px;
}
.dataset .wcheck {
  margin-right: 5px;
  width: 16px;
  height: 16px;
}
.dataset > div.active .wcheck {
  background: rgba(50, 50, 100, 0.65);
  box-shadow: 1px 1px 1px rgb(0, 0,  0) inset;
}
.dataset > div:not(.active) .wcheck {
  background: rgba(50, 50, 100, 0.45);
  box-shadow: 1px 1px 1px rgb(0, 0,  0);
}
.dataset .check {
  width: 16px;
  height: 16px;
  padding: 0;
  margin: 0;
}
.dataset span {
   position:relative;
   display:inline-block;
   top:2px;
}
.buttons {
  display: flex;
  flex-direction: row;
  height: 100%;
  align-items: center;
}
.buttons .btn {
  width: 24px;
  height: 24px;
  cursor: pointer;
  border-radius: 3px;
  border: 1px solid rgb(36, 41, 46);
  margin-right: 5px;
  color: white;
}
.buttons div.btn {
  display: flex;
  flex-direction: row;
  font-size: 12px;
  align-items: center;
  justify-content: center;
}
.buttons .btn.github {
  width: 20px;
  height: 20px;
  padding: 3px;
}
.buttons .btn:hover {
  background: rgb(80, 80, 80);
  border: 1px solid rgb(150, 150, 150);
}
@media only screen and (max-width: 650px) {
.body > a,
.body > img {
  display: none;
}
}
</style>
