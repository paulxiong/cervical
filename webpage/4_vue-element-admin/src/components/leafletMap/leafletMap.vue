<template>
  <div class="vue-leaflet">
    <div id="map" style="width:1000px; height:800px;" />
  </div>
</template>

<script>
import { APIUrl } from '@/const/config'
import L from 'leaflet'
import { Icon } from 'leaflet'
import 'leaflet/dist/leaflet.css'

export default {
  name: 'LeafletVue',
  components: { },
  props: {
    args: {
      type: Object,
      default: () => {
        return { }
      }
    }
  },
  data() {
    return {
      debug: false,
      IMGURL: APIUrl + '/imgs',
      mapInstance: null
    }
  },
  created() {
    // Resolve an issue where the markers would not appear
    delete Icon.Default.prototype._getIconUrl
    Icon.Default.mergeOptions({
      iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
      iconUrl: require('leaflet/dist/images/marker-icon.png'),
      shadowUrl: require('leaflet/dist/images/marker-shadow.png')
    })
  },
  mounted() {
    var that = this // 保留vue的this, 方便后面使用

    this.mapInstance = this.Map_create()

    var tiles = new L.GridLayer({ 'tileSize': L.point(this.args.ImageWidth, this.args.ImageHeight) })
    tiles.createTile = function(coords) {
      return that.GridLayer_createTile(coords, this)
    }
    tiles.addTo(this.mapInstance)

    L.TileLayer.Kitten = L.TileLayer.extend({
      initialize: function(options) {
        that.TileLayer_initialize(options, this)
      },
      getTileUrl: that.TileLayer_getTileUrl,
      getAttribution: that.TileLayer_getAttribution
    })
    L.tileLayer.kitten = function(options) {
      var k = new L.TileLayer.Kitten(options)
      k._removeAllTiles = function() {} // 禁止移除图层，因为我们只有一个z-level，不准切换z-level
      return k
    }
    L.tileLayer.kitten({ 'tileSize': L.point(this.args.ImageWidth, this.args.ImageHeight), 'continuousWorld': true }).addTo(this.mapInstance)
  },
  beforeDestroy() {
  },
  methods: {
    Map_create() {
      return L.map('map', {
        crs: L.CRS.Simple,
        center: new L.LatLng(0, 0), // 左上角(y, x)
        maxBounds: this.makebounds(this.args.sceneWidth, this.args.sceneHeight),
        minZoom: -0.49,
        maxZoom: 0.49, // >0表示放大，但是放大不能超过0.5不然自动加载下个z-level切片
        maxNativeZoom: 0,
        zoom: -0.49,
        zoomDelta: 0.05, // 变焦增量+-滚轮一下缩放多少,
        zoomSnap: 0.05,
        noWrap: true,
        detectRetina: false
      })
    },
    GridLayer_createTile(coords, _this) {
      var tile = L.DomUtil.create('canvas', 'leaflet-tile')
      var ctx = tile.getContext('2d')
      var size = _this.getTileSize() // 这个this不是vue的this
      tile.width = size.x
      tile.height = size.y
      if (this.debug === true) {
        var nwPoint = coords.scaleBy(size)// 将切片号乘以切片分辨率，得到切片左上角的绝对像素坐标
        var nw = this.mapInstance.unproject(nwPoint, coords.z)// 根据绝对像素坐标，以及缩放层级，反投影得到其经纬度
        ctx.fillStyle = 'white'
        ctx.fillRect(0, 0, size.x, 50)
        ctx.fillStyle = 'black'
        ctx.fillText('x: ' + coords.x + ', y: ' + coords.y + ', zoom: ' + coords.z, 20, 20)
        ctx.fillText('lat: ' + nw.lat + ', lon: ' + nw.lng, 20, 40)
        ctx.strokeStyle = 'red'
        ctx.beginPath()
        ctx.moveTo(0, 0)
        ctx.lineTo(size.x - 1, 0)
        ctx.lineTo(size.x - 1, size.y - 1)
        ctx.lineTo(0, size.y - 1)
        ctx.closePath()
        ctx.stroke()
      }
      return tile
    },
    TileLayer_initialize(options, _this) {
      L.TileLayer.prototype.initialize.call(_this, '', options) // url=''
    },
    TileLayer_getTileUrl(coords) {
      // 这里的X,y表示第几个瓦片坐标，不是像素坐标, 左上角是原点（初始化map有关），从左往右X递增，从上到下Y递增
      console.log('z=%d \t x=%d \t y=%d', coords.z, coords.x, coords.y)
      if (coords.x < 0 || coords.y < 0) {
        return ''
      }
      if (coords.x >= this.args.sceneWidth / this.args.ImageWidth) {
        return ''
      }
      if (coords.y >= this.args.sceneHeight / this.args.ImageHeight) {
        return ''
      }
      var img = this.IMGURL + '/scratch/img/' + this.args.bid + '/' + this.args.mid + '/Images'
      img = img + '/IMG' + ('' + (coords.y + 1)).padStart(3, '0') + 'x' + ('' + (coords.x + 1)).padStart(3, '0')
      img = img + this.args.ext
      return img
    },
    TileLayer_getAttribution() {
      return "<a href='https://placekitten.com/attribution.html'>提示</a>"
    },
    makebounds(sceneWidth, sceneHeight) {
      // 要把坐标移动到第四象限，这样保证左上角X,y都是0,从左往右X递增，从上到下Y递减
      // L.CRS.Simple，的latLng的单位是像素点
      var southWest = [-sceneHeight, 0] // 地图西南点坐标， 左下(y1, x1)
      var northEast = [0, sceneWidth] // 地图东北点坐标，右上(y2, x2)
      var bounds = L.latLngBounds(southWest, northEast) // 地图边界
      return bounds
    },
    gotolatLng(val) {
      if (val === 1) {
        this.mapInstance.setView([-13604, 15502], -0.49)
      } else {
        this.mapInstance.setView([-33282.53466523906, 42536.421951476725], -0.49)
      }
      console.log(this.mapInstance.getCenter())
    }
  }
}
</script>

<style scoped>
</style>
