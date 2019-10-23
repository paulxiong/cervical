<template>
  <div class="vmr-ai-panel" :loading="loading" :class="rootClass">
    <div class="vmr-g-image" style="position: relative; overflow: hidden;">
      <img class="vmr-ai-raw-image" :src="currentBaseImage" style="display: block; position: absolute; user-select: none;" @load="onImageLoad">
      <div class="annotate vmr-ai-raw-image-mask" style="user-select: none; position: absolute; cursor: crosshair; left: 0px; top: 0;">
        <div class="draft" style="position: absolute;user-select: none;display: none;background-color: rgba(1,0,0,0.5);" />
      </div>
    </div>
  </div>
</template>
<script>
import PictureMarker from './marker.js'
import './bdmarker.scss'
const empImg = `data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAwAAAAMCAIAAADZF8uwAAAAGUlEQVQYV2M4gwH+YwCGIasIUwhT25BVBADtzYNYrHvv4gAAAABJRU5ErkJggg==`
export default {
  name: 'VueMarker',
  props: {
    readOnly: {
      type: Boolean,
      default: false
    },
    img: {
      type: String,
      default: ''
    },
    uniqueKey: {
      type: [String, Number],
      default: ''
    },
    width: {
      type: [String, Number],
      default: ''
    },
    ratio: {
      type: Number,
      default: 16
    }
  },
  data() {
    return {
      emptyImg: empImg,
      options: void 0,
      currentBaseImage: void 0,
      rootClass: '',
      key: '',
      wratioh: 16 / 9,
      loading: true
    }
  },
  watch: {
    img: function(n, o) {
      this.currentBaseImage = n
    },
    width: function(n, o) {
      this.__updateFrame()
    },
    readOnly: function(n, o) {
      this.options.options = {
        ...this.options.options,
        editable: !n
      }
      if (this.marker) {
        this.marker.updateConfig(this.options)
      }
    },
    ratio: function(n, o) {
      if (n) {
        this.wratioh = n
        this.__updateFrame()
      }
    }
  },
  beforeMount() {
    this.key = this.uniqueKey
    this.rootClass = this.uniqueKey ? `pannel-${this.uniqueKey}` : void 0
  },
  mounted() {
    this.__updateFrame()
  },
  created() {
    const self = this
    this.options = {
      options: {
        blurOtherDots: true,
        blurOtherDotsShowTags: true,
        editable: this.readOnly ? 'false' : 'true',
        trashPositionStart: 1
      },
      onDataRendered: self.onDataRendered,
      onUpdated: self.onUpdated,
      onDrawOne: self.onDrawOne,
      onSelect: self.onSelect
    }
    if (/^.+$/.test(this.img)) {
      this.currentBaseImage = this.img
    } else {
      this.currentBaseImage = this.emptyImg
    }
    this.$nextTick(function() {
      self.__initMarker()
      self.$emit('vmarker:onReady', self.key)
    })
  },
  activated() {
    this.rootClass = `pannel-${this.key}`
    this.$emit('vmarker:onReady', this.key)
  },
  methods: {
    getMarker() {
      return this.marker
    },
    __updateFrame() {
      const root = this.$el
      if (!root) {
        return
      }

      let width = this.width
      if (!this.width) {
        width = '100%'
      }
      root.style.width = width.endsWith('%') ? width : parseInt(width) + 'px'
      root.style.height = root.clientWidth / this.wratioh + 'px'
      root
        .querySelectorAll(
          '.vmr-g-image,.vmr-ai-raw-image,.vmr-ai-raw-image-mask'
        )
        .forEach(element => {
          element.style.width = root.style.width
          element.style.height =
            parseInt(root.clientWidth) / this.wratioh + 'px'
        })
    },
    __initMarker() {
      const self = this
      const root = this.$el
      if (!root) {
        return
      }
      self.marker = new PictureMarker(
        root.querySelector(`.annotate`),
        root.querySelector(`.draft `),
        self.options
      )
    },
    onImageLoad(e) {
      const rawData = {
        rawW: e.target.naturalWidth,
        rawH: e.target.naturalHeight,
        currentW: e.target.offsetWidth,
        currentH: e.target.offsetHeight
      }
      if (!this.currentBaseImage.startsWith('data')) {
        this.$emit('vmarker:onImageLoad', rawData, this.key)
      }
      this.loading = false
    },
    onDataRendered() {
      this.$emit('vmarker:onDataRendered', this.key)
    },
    onUpdated(data) {
      this.$emit('vmarker:onUpdated', data, this.key)
    },
    onDrawOne(data, currentMovement) {
      this.$emit('vmarker:onDrawOne', data, this.key)
    },
    onSelect(data) {
      this.$emit('vmarker:onSelect', data, this.key)
    },
    dispatchEvent(event, data) {
      if (this.marker) {
        return this.marker[event](data)
      }
    },
    renderData(data, wh) {
      if (this.marker) {
        this.marker.renderData(data, wh)
      }
    },
    clearData() {
      if (this.marker) {
        this.marker.clearData()
      }
    },
    setTag(tag) {
      if (this.marker) {
        this.marker.setTag(tag)
      }
    },
    renderer(imageUrl) {
      this.currentBaseImage = this.img = imageUrl
    }
  }
}
</script>
<style lang="scss" scoped>
$opImageWidth: 600px;
$gulp: 10px;
.vmr-ai-panel {
  background: #3e3e3e;
  width: 100%;
  display: flex;
  flex-direction: row;
  align-items: center;
  height: auto; // $gulp * 2;
  .vmr-g-image,
  .vmr-ai-raw-image,
  .vmr-ai-raw-image-mask {
    // width: $opImageWidth;
    // height: round($opImageWidth * 9 / 16);
    width: 100%;
    height: 100%;
  }
}
</style>
