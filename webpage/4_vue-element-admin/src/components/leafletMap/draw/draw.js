import L from 'leaflet'
import 'leaflet-draw'

function _tooltip_init(_this) { // 初始化地图上默认的一些提示信息
  L.drawLocal.draw.handlers.rectangle.tooltip.start = '单击并拖动鼠标来绘制矩形'
  L.drawLocal.draw.handlers.simpleshape.tooltip.end = '单击完成绘制'
  L.drawLocal.edit.handlers.remove.tooltip.text = '单击标注来删除'

  // 下面这个是自定义方法，目的是缩放的时候动态更新tooltip位置, 是画完框之后，上面的设置是画框的时候的提示
  L.Tooltip.prototype._updatePosition = function() {
    // this是指tooltip
    var pos = this._map.latLngToLayerPoint(this._latlng)
    if (this._source && this._source._bounds) {
      const x1y1 = this._source._bounds._northEast // 右上
      pos = this._map.latLngToLayerPoint(x1y1)
    }
    this._setPosition(pos)
  }
}

function _drawEvent(_map) {
  _map.on(L.Draw.Event.CREATED, function() { console.log('CREATED       ') })
  _map.on(L.Draw.Event.EDITED, function() { console.log('EDITED        ') })
  _map.on(L.Draw.Event.DELETED, function() { console.log('DELETED       ') })
  _map.on(L.Draw.Event.DRAWSTART, function() { console.log('DRAWSTART     ') })
  _map.on(L.Draw.Event.DRAWSTOP, function() { console.log('DRAWSTOP      ') })
  _map.on(L.Draw.Event.DRAWVERTEX, function() { console.log('DRAWVERTEX    ') })
  _map.on(L.Draw.Event.EDITSTART, function() { console.log('EDITSTART     ') })
  _map.on(L.Draw.Event.EDITMOVE, function() { console.log('EDITMOVE      ') })
  _map.on(L.Draw.Event.EDITSTOP, function() { console.log('EDITSTOP      ') })
  _map.on(L.Draw.Event.DELETESTART, function() { console.log('DELETESTART   ') })
  _map.on(L.Draw.Event.DELETESTOP, function() { console.log('DELETESTOP    ') })
  _map.on(L.Draw.Event.TOOLBAROPENED, function() { console.log('TOOLBAROPENED') })
  _map.on(L.Draw.Event.TOOLBARCLOSED, function() { console.log('TOOLBARCLOSED') })
  _map.on(L.Draw.Event.MARKERCONTEXT, function() { console.log('MARKERCONTEXT') })
  _map.on(L.Draw.Event.EDITRESIZE, function(e) { console.log('EDITRESIZE    ') })
  _map.on(L.Draw.Event.EDITVERTEX, function(e) { console.log('EDITVERTEX    ') })
}

function _MapDrawCreate(_this, mapInstance) { // 创建画图实例，参数mapInstance是已经初始化的Map实例, _this是vue的实例
  const that = _this
  that.drawnItems = new L.FeatureGroup()
  mapInstance.addLayer(that.drawnItems)
  that.drawControl = new L.Control.Draw({
    position: 'topright',
    draw: {
      polyline: false, // 不准画线
      polygon: false, // 不准画多边形
      circle: false, // 不准画圆
      marker: false, // 不准画标记
      circlemark: false,
      rectangle: {
        shapeOptions: {
          clickable: true,
          fillOpacity: 0, // 填充完全透明
          weight: that.weight
        }
      }
    },
    edit: {
      featureGroup: that.drawnItems,
      poly: {
        allowIntersection: false
      },
      remove: true
    }
  })
  if (mapInstance.addControl(that.drawControl)) {
    console.log('addControl')
  }

  mapInstance.on(L.Draw.Event.CREATED, function(e) {
    var type = e.layerType
    if (type !== 'rectangle') { // 目前只支持画矩形
      return
    }
    var layer = e.layer
    // 参考 https://github.com/Leaflet/Leaflet/blob/master/src/layer/Tooltip.js
    layer.bindTooltip('HPV', {
      permanent: true,
      direction: 'right',
      sticky: true,
      interactive: 'true',
      offset: [0, 0] // 这个必须是0,0, 上面修改了_updatePosition，缩放的时候才计算偏移
    }).addTo(that.drawnItems)
  })

  mapInstance.on(L.Draw.Event.EDITED, function(e) {
    var layers = e.layers
    var countOfEditedLayers = 0
    layers.eachLayer(function(layer) {
      countOfEditedLayers++

      // 更新tooltip的位置
      if (layer.getTooltip) {
        var toolTip = layer.getTooltip()
        if (toolTip) {
          toolTip._updatePosition()
        }
      }
    })
    console.log('修改了 ' + countOfEditedLayers + ' 个图层')
  })
}

// initDrawrecDrawControl() {
//   this.drawRectangle = new L.Draw.Rectangle(this.mapInstance, this.drawControl.options.rectangle).disable()
//   this.drawRectangle.disable()
//   this.mapInstance.on('draw:editstart', function(e) {
//     console.log(e)
//   })
// }
// drawrec(e) {
//   new L.Draw.Rectangle(this.mapInstance, this.drawControl.options.rectangle).enable()
// },
// drawedit(e) {
//   new L.Draw.Rectangle(this.mapInstance, this.drawControl.options.rectangle).disable()
//   this.mapDrawEdit = new L.EditToolbar.Edit(this.mapInstance, {
//     featureGroup: this.drawnItems,
//     selectedPathOptions: this.drawControl.options.edit.selectedPathOptions
//   }).enable()
//   console.log(this.mapDrawEdit)
//   this.mapInstance.on('MSPointerMove', function(e) { // 拖动视野图结束移动就会触发
//     console.log('MSPointerMove')
//   })
// },
// draweditdone(e) {
//   this.mapDrawEdit = new L.EditToolbar.Edit(this.mapInstance, {
//     featureGroup: this.drawnItems,
//     selectedPathOptions: this.drawControl.options.edit.selectedPathOptions
//   }).disable()
// },
// drawdelete() {
//   new L.Draw.Rectangle(this.mapInstance, this.drawControl.options.rectangle).disable()
//   this.mapDrawDelete = new L.EditToolbar.Delete(this.mapInstance, {
//     featureGroup: this.drawnItems
//   }).enable()
// }

export function MapDrawCreate(_this, _map) {
  _tooltip_init(_this)
  _drawEvent(_map)
  _MapDrawCreate(_this, _map)
}
