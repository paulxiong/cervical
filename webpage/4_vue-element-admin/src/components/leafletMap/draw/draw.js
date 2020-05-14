import L from 'leaflet'
import 'leaflet-draw'

function _tooltip_init(_this) { // 初始化地图上默认的一些提示信息
  L.drawLocal.draw.toolbar.buttons.rectangle = '绘制矩形标注'
  L.drawLocal.draw.toolbar.actions.title = '取消绘制矩形标注'
  L.drawLocal.draw.toolbar.actions.text = '取消'
  L.drawLocal.draw.handlers.rectangle.tooltip.start = '左键按下不放，拖动鼠标来绘制矩形标注'
  L.drawLocal.draw.handlers.simpleshape.tooltip.end = '松开左键完成绘制'
  L.drawLocal.edit.toolbar.buttons.edit = '修改标注'
  L.drawLocal.edit.toolbar.buttons.editDisabled = '没有可以修改的标注'
  L.drawLocal.edit.toolbar.buttons.remove = '删除标注'
  L.drawLocal.edit.toolbar.actions.save.title = '保存修改'
  L.drawLocal.edit.toolbar.actions.save.text = '保存'
  L.drawLocal.edit.toolbar.actions.cancel.title = '取消当前的标注修改'
  L.drawLocal.edit.toolbar.actions.cancel.text = '取消'
  L.drawLocal.edit.toolbar.actions.clearAll.title = '删除所有的标注, 慎用！'
  L.drawLocal.edit.toolbar.actions.clearAll.text = '删除所有'
  L.drawLocal.edit.toolbar.buttons.removeDisabled = '没有可以删除的标注'
  L.drawLocal.edit.handlers.remove.tooltip.text = '单击标注来删除'
  L.drawLocal.edit.handlers.edit.tooltip.text = '拖拽标注中心点可平移标注，拖拽四角可改变标注形状'
  L.drawLocal.edit.handlers.edit.tooltip.subtext = '右上角“取消/保存”可以放弃/保存修改'

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

// 单击一个正方形触发
function _clickRectangleHandler(e, _this) {
  var layer = e.sourceTarget // 这里获得矩形
  console.log(layer.getTooltip())

//   layer.editing.enable() // 使能修改当前矩形
//   handler: new L.EditToolbar.Edit(map, {
//     featureGroup: featureGroup,
//     selectedPathOptions: this.options.edit.selectedPathOptions,
//     poly: this.options.poly
// }),
}

// 画完一个正方形触发
function _createRectangleHandler(e, _this) {
  var type = e.layerType
  if (type !== 'rectangle') { // 目前只支持画矩形
    return
  }
  var layer = e.layer
  // 参考 https://github.com/Leaflet/Leaflet/blob/master/src/layer/Tooltip.js
  layer.bindTooltip(`<a title="123" style='width:100%;height:100%;background-color: red;color: white;'>HPV1</a>`, {
    permanent: true, // 始终显示
    direction: 'right',
    sticky: true,
    interactive: false, // 可交互的，就是能被点击到
    offset: [0, 0] // 这个必须是0,0, 上面修改了_updatePosition，缩放的时候才计算偏移
  }).addTo(_this.drawnItems)

  // 单击矩形触发
  layer.on('click', function(event) {
    _clickRectangleHandler(event, _this, layer)
  })
}

// 修改中触发
function _editingRectangleHandler(e, _this) {
  const layer = e.layer
  if (!layer.getTooltip) {
    return
  }
  const toolTip = layer.getTooltip()
  if (!toolTip) {
    return
  }
  toolTip._updatePosition()
}

// 修改结束之后触发
function _editRectangleHandler(e, _this) {
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
}

function _drawEvent(_this, _map) {
  _map.on(L.Draw.Event.DELETED, function() { console.log('DELETED') })
  _map.on(L.Draw.Event.DRAWSTOP, function() { console.log('DRAWSTOP') })
  _map.on(L.Draw.Event.DRAWVERTEX, function() { console.log('DRAWVERTEX') })
  _map.on(L.Draw.Event.EDITSTART, function() { console.log('EDITSTART') })
  _map.on(L.Draw.Event.EDITSTOP, function() { console.log('EDITSTOP') })
  _map.on(L.Draw.Event.DELETESTART, function() { console.log('DELETESTART') })
  _map.on(L.Draw.Event.DELETESTOP, function() { console.log('DELETESTOP') })
  _map.on(L.Draw.Event.TOOLBAROPENED, function() { console.log('TOOLBAROPENED') })
  _map.on(L.Draw.Event.TOOLBARCLOSED, function() { console.log('TOOLBARCLOSED') })
  _map.on(L.Draw.Event.MARKERCONTEXT, function() { console.log('MARKERCONTEXT') })
  _map.on(L.Draw.Event.EDITVERTEX, function(e) { console.log('EDITVERTEX') })
  _map.on(L.Draw.Event.DRAWSTART, function() {
    console.log('DRAWSTART')
  })
  _map.on(L.Draw.Event.CREATED, function(e) {
    console.log('CREATED') // 画框
    _createRectangleHandler(e, _this)
  })
  _map.on(L.Draw.Event.EDITED, function(e) { // 修改结束
    console.log('EDITED')
    _editRectangleHandler(e, _this)
  })
  _map.on(L.Draw.Event.EDITMOVE, function(e) { // 修改，平移矩形
    _editingRectangleHandler(e, _this)
  })
  _map.on(L.Draw.Event.EDITRESIZE, function(e) { // 修改，矩形改变大小
    _editingRectangleHandler(e, _this)
  })
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
      circlemarker: false,
      rectangle: {
        shapeOptions: {
          clickable: true,
          fillOpacity: 0, // 填充完全透明
          color: 'red', // 边框颜色
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
}

export function MapDrawCreate(_this, _map) {
  _tooltip_init(_this)
  _drawEvent(_this, _map)
  _MapDrawCreate(_this, _map)
}

// 查找工具栏按钮,并单击
function _clickToolBar(classname, title) {
  var element = document.getElementsByClassName(classname)
  if (element.length < 1) {
    return
  }
  for (var i = 0; i < element.length; i++) {
    var item = element[i]
    if (item.title !== title) {
      continue
    }
    item.click()
  }
  return
}
// 查找工具栏按钮,并单击
function _clickAction(classname, title, text) {
  var element = document.getElementsByClassName(classname)
  if (element.length < 1) {
    return
  }
  for (var i = 0; i < element.length; i++) {
    var item = element[i].getElementsByTagName('a')
    if (item.length < 1) {
      continue
    }
    for (var j = 0; j < item.length; j++) {
      if (!item[j] || item[j].title !== title || item[j].text !== text) {
        continue
      }
      item[j].click()
    }
  }
}

// 通过页面元素操作来控制工具栏
export function clickDrawRec() { // 开始绘制矩形
  return _clickToolBar('leaflet-draw-draw-rectangle', '绘制矩形标注')
}
export function clickEditRec() { // 开始修改
  return _clickToolBar('leaflet-draw-edit-edit', '修改标注')
}
export function clickRemoveRec() { // 开始删除
  return _clickToolBar('leaflet-draw-edit-remove', '删除标注')
}
export function clickDrawCancel() { // 取消绘制矩形
  return _clickAction('leaflet-draw-actions', '取消绘制矩形标注', '取消')
}
export function clickEditCancel() { // 取消修改
  return _clickAction('leaflet-draw-actions', '取消当前的标注修改', '取消')
}
export function clickEditSave() { // 保存修改
  return _clickAction('leaflet-draw-actions', '保存修改', '保存')
}
export function clickRemoveCancel() { // 取消删除
  return _clickAction('leaflet-draw-actions', '取消当前的标注修改', '取消')
}
export function clickRemoveSave() { // 保存删除
  return _clickAction('leaflet-draw-actions', '保存修改', '保存')
}
export function clickRemoveAll() { // 删除所有
  return _clickAction('leaflet-draw-actions', '删除所有的标注, 慎用！', '删除所有')
}
