<template>
  <div class="vue-leaflet">
    <div id="map" :style="{width: curWidth, height: curHeight}" />
  </div>
</template>

<script>
import 'leaflet/dist/leaflet.css'
import 'leaflet-draw/dist/leaflet.draw.css'
import 'leaflet-toolbar/dist/leaflet.toolbar.css'
import 'leaflet-draw-toolbar/dist/leaflet.draw-toolbar.css'
import { APIUrl } from '@/const/config'
import L from 'leaflet'
import 'leaflet-draw'
import LeafletDrawRectangle from './draw/draw.js'

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
      curWidth: (window.innerWidth - 435) + 'px',
      curHeight: window.innerHeight + 'px',
      debug: false,
      IMGURL: APIUrl + '/imgs',
      mapInstance: null,
      minZoom: -2,
      maxZoom: 0.4, // >0表示放大，但是放大不能超过0.5不然自动加载下个z-level切片
      maxNativeZoom: 0.1,
      minNativeZoom: -0,
      zoom: 0,
      drawInstance: null
    }
  },
  created() {
  },
  mounted() {
    const that = this // 保留vue的this, 方便后面使用
    this.mapInstance = this.Map_create()

    const tiles = new L.GridLayer({ 'tileSize': L.point(this.args.realimgwidth, this.args.realimgheight) })
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
      const k = new L.TileLayer.Kitten(options)
      k._removeAllTiles = function() {
        for (const key in this._tiles) {
          const zoomlevel = that.mapInstance.getZoom()
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

    // 下面是标注相关的
    if (this.args.labletool) {
      this.drawInstance = new LeafletDrawRectangle(this, this.mapInstance)
    }
  },
  beforeDestroy() {
  },
  methods: {
    Map_create() {
      const _map = L.map('map', {
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
        detectRetina: false,
        attributionControl: false // 不要显示leaflet的链接
      })
      const that = this
      _map.on('dragend', function(e) { // 拖动视野图结束移动就会触发
        const xy = that.latLngToCoords(that.mapInstance.getCenter())
        that.$emit('dragend', xy)
      })
      return _map
    },
    GridLayer_createTile(coords, _this) {
      const tile = L.DomUtil.create('canvas', 'leaflet-tile')
      const ctx = tile.getContext('2d')
      const size = _this.getTileSize() // 这个this不是vue的this
      tile.width = size.x
      tile.height = size.y
      if (this.debug === true) {
        const nwPoint = coords.scaleBy(size)// 将切片号乘以切片分辨率，得到切片左上角的绝对像素坐标
        const nw = this.mapInstance.unproject(nwPoint, coords.z)// 根据绝对像素坐标，以及缩放层级，反投影得到其经纬度
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
      if (coords.x < 0 || coords.y < 0) {
        return ''
      }
      if (coords.x >= this.args.scenewidth / this.args.realimgwidth) {
        return ''
      }
      if (coords.y >= this.args.sceneheight / this.args.realimgheight) {
        return ''
      }
      let img = this.IMGURL + '/scratch/img/' + this.args.batchid + '/' + this.args.medicalid + '/Images'
      img = img + '/IMG' + ('' + (coords.y + 1)).padStart(3, '0') + 'x' + ('' + (coords.x + 1)).padStart(3, '0')
      img = img + this.args.imgext + '?crop=0,0|' + this.args.realimgwidth + ',' + this.args.realimgheight + '&quality=80'
      return img
    },
    TileLayer_getAttribution() {
      return ''
    },
    makebounds(scenewidth, sceneheight) {
      // 要把坐标移动到第四象限，这样保证左上角X,y都是0,从左往右X递增，从上到下Y递减
      // L.CRS.Simple，的latLng的单位是像素点
      const southWest = [-sceneheight, 0] // 地图西南点坐标， 左下(y1, x1)
      const northEast = [0, scenewidth] // 地图东北点坐标，右上(y2, x2)
      const bounds = L.latLngBounds(southWest, northEast) // 地图边界
      return bounds
    },
    gotolatLng(x, y, drawrectangle) {
      y = -y // y轴是负数
      // console.log(this.mapInstance.getCenter())
      this.mapInstance.setView([y, x], this.zoom, { animate: true, duration: 0.1 }) // 通过移动动画强制刷新画面
      // if (!drawrectangle) {
      //   return
      // }
      // // const bounds = [[y, x], [y - 100, x + 100]]
      // L.rectangle(bounds, { color: '#ff7800', weight: 2, fillOpacity: 0 }).addTo(this.mapInstance)
    },
    latLngToCoords(latLng) {
      let y = parseInt(latLng.lat / this.args.realimgheight)
      y = -y
      const x = parseInt(latLng.lng / this.args.realimgwidth)
      return { 'x': x, 'y': y }
    },
    clickDrawRec() {
      this.drawInstance.clickDrawRec()
    },
    clickDrawCancel() {
      this.drawInstance.clickDrawCancel()
    },
    drawrectangle(cell) { // 这个是自动导入使用
      this.drawInstance.drawrectangle(cell)
    }
  }
}
</script>

<style>
.leaflet-right {
  /* 把toolbar放在右上角，然后使用display隐藏 */
  display: none;
}
</style>
