import Vue from 'vue'
import store from '@/store'
// import { isString, isArray } from '@/utils/validate'
// import settings from '@/settings'

// you can set in settings.js
// errorLog:'production' | ['production', 'development']
// const { errorLog: needErrorLog } = settings

function isRelease() {
  if (typeof (process.env.VUE_APP_API) !== 'undefined' && process.env.VUE_APP_API === 'production') {
    return true
  }
  if (typeof (process.env.NODE_ENV) !== 'undefined' && process.env.NODE_ENV === 'production') {
    return true
  }
  return false
}

if (isRelease()) {
  Vue.config.errorHandler = function(err, vm, info, a) {
    // Don't ask me why I use Vue.nextTick, it just a hack.
    // detail see https://forum.vuejs.org/t/dispatch-in-vue-config-errorhandler-has-some-problem/23500
    Vue.nextTick(() => {
      store.dispatch('errorLog/addErrorLog', {
        err,
        vm,
        info,
        url: window.location.href
      })
    })
  }
}
