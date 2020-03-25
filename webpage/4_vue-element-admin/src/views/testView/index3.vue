<template>
  <div>
    <diruploader />
    <lmap style="width: 50%" />
  </div>
</template>

<script>
import diruploader from './components/diruploader'
import lmap from '@/components/leafletMap/leafletMap'
import { Icon } from 'leaflet'
import 'leaflet/dist/leaflet.css'

// Resolve an issue where the markers would not appear
delete Icon.Default.prototype._getIconUrl
Icon.Default.mergeOptions({
  iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
  iconUrl: require('leaflet/dist/images/marker-icon.png'),
  shadowUrl: require('leaflet/dist/images/marker-shadow.png')
})

export default {
  components: { lmap, diruploader },
  data() {
    return {
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
