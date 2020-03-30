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
      mapInstance: null,
      minZoom: -2,
      maxZoom: 0.4, // >0表示放大，但是放大不能超过0.5不然自动加载下个z-level切片
      maxNativeZoom: 0.1,
      minNativeZoom: 0,
      zoom: 0
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
    console.log(this.args)
    var that = this // 保留vue的this, 方便后面使用

    this.mapInstance = this.Map_create()

    var tiles = new L.GridLayer({ 'tileSize': L.point(this.args.realimgwidth, this.args.realimgheight) })
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
      k._removeAllTiles = function() {
        for (var key in this._tiles) {
          var zoomlevel = that.mapInstance.getZoom()
          if (zoomlevel !== 0.00) { // 0缩放级别是原图，大于小于这个都不要删除图层,因为我们只有1层图层，放大缩小都是这层, 删掉就看不到了
            continue
          }
          // that.latLngToCoords(that.mapInstance.getCenter()) // 这个取到的是跳转之前的
          this._removeTile(key)
        }
      } // 禁止移除图层，因为我们只有一个z-level，不准切换z-level
      return k
    }
    L.tileLayer.kitten({
      'tileSize': L.point(this.args.realimgwidth, this.args.realimgheight),
      'continuousWorld': true,
      'maxNativeZoom': this.maxNativeZoom,
      'minNativeZoom': this.minNativeZoom }).addTo(this.mapInstance)
  },
  beforeDestroy() {
  },
  methods: {
    Map_create() {
      return L.map('map', {
        crs: L.CRS.Simple,
        center: new L.LatLng(0, 0), // 左上角(y, x)
        maxBounds: this.makebounds(this.args.scenewidth, this.args.sceneheight),
        minZoom: this.minZoom,
        maxZoom: this.maxZoom, // >0表示放大，但是放大不能超过0.5不然自动加载下个z-level切片
        maxNativeZoom: this.maxNativeZoom,
        minNativeZoom: this.minNativeZoom,
        zoom: this.zoom,
        zoomDelta: 0.1, // 变焦增量+-滚轮一下缩放多少,
        zoomSnap: 0.1,
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
      if (coords.x >= this.args.scenewidth / this.args.realimgwidth) {
        return ''
      }
      if (coords.y >= this.args.sceneheight / this.args.realimgheight) {
        return ''
      }
      var img = this.IMGURL + '/scratch/img/' + this.args.batchid + '/' + this.args.medicalid + '/Images'
      img = img + '/IMG' + ('' + (coords.y + 1)).padStart(3, '0') + 'x' + ('' + (coords.x + 1)).padStart(3, '0')
      img = img + this.args.imgext + '?crop=0,0|' + this.args.realimgwidth + ',' + this.args.realimgheight + '&quality=80'
      return img
    },
    TileLayer_getAttribution() {
      return "<a href='https://placekitten.com/attribution.html'>提示</a>"
    },
    makebounds(scenewidth, sceneheight) {
      // 要把坐标移动到第四象限，这样保证左上角X,y都是0,从左往右X递增，从上到下Y递减
      // L.CRS.Simple，的latLng的单位是像素点
      var southWest = [-sceneheight, 0] // 地图西南点坐标， 左下(y1, x1)
      var northEast = [0, scenewidth] // 地图东北点坐标，右上(y2, x2)
      var bounds = L.latLngBounds(southWest, northEast) // 地图边界
      return bounds
    },
    gotolatLng(x, y) {
      y = -y // y轴是负数
      // console.log(this.mapInstance.getCenter())
      this.mapInstance.setView([y, x], this.zoom)
      var bounds = [[y, x], [y - 100, x + 100]]
      L.rectangle(bounds, { color: '#ff7800', weight: 2, fillOpacity: 0 }).addTo(this.mapInstance)
    },
    latLngToCoords(latLng) {
      var y = parseInt(latLng.lat / this.args.realimgheight)
      y = -y
      var x = parseInt(latLng.lng / this.args.realimgwidth)
      console.log(x, y)
    }
  }
}
</script>

<style scoped>
</style>
