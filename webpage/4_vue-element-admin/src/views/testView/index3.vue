<template>
  <div>
    <diruploader />
    <lmap
      :args="mapargs"
      style="width: 50%"
    />
  </div>
</template>

<script>
import diruploader from './components/diruploader'
import lmap from '@/components/leafletMap/leafletMap'

export default {
  components: { lmap, diruploader },
  data() {
    return {
      mapargs: {
        bid: 'b20200327',
        mid: 'b20200327095341',
        ext: '.jpg',
        ImageWidth: 2448,
        ImageHeight: 2048,
        sceneWidth: 72348,
        sceneHeight: 72104
      },
      options: {
        // https://github.com/simple-uploader/Uploader/tree/develop/samples/Node.js
        target: '//localhost:3000/upload',
        testChunks: false
      },
      attrs: {
        accept: 'image/*'
      }
    }
  }
}
</script>

<style>
  .uploader-example {
    width: 880px;
    padding: 15px;
    margin: 40px auto 0;
    font-size: 12px;
    box-shadow: 0 0 10px rgba(0, 0, 0, .4);
  }
  .uploader-example .uploader-btn {
    margin-right: 4px;
  }
  .uploader-example .uploader-list {
    max-height: 440px;
    overflow: auto;
    overflow-x: hidden;
    overflow-y: auto;
  }
</style>
