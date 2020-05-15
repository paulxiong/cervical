import L from 'leaflet'
import 'leaflet-draw'
import 'leaflet-toolbar'
import 'leaflet-draw-toolbar/dist/leaflet.draw-toolbar.js'
import './ColorPicker.js'

function _tooltip_init() { // 初始化地图上默认的一些提示信息
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
function _clickRectangleHandler(e, drawInstance, _map) {
  var layer = e.sourceTarget // 这里获得矩形
  console.log(layer.getTooltip())

  // layer.editing.enable() // 使能修改当前矩形
  // layer.setTooltipContent('修改')

//   handler: new L.EditToolbar.Edit(map, {
//     featureGroup: featureGroup,
//     selectedPathOptions: this.options.edit.selectedPathOptions,
//     poly: this.options.poly
// }),
}

// 画完一个正方形触发
function _createRectangleHandler(e, drawInstance, _map) {
  var type = e.layerType
  if (type !== 'rectangle') { // 目前只支持画矩形
    return
  }
  var layer = e.layer
  // 参考 https://github.com/Leaflet/Leaflet/blob/master/src/layer/Tooltip.js
  const ts = '' + new Date().getTime()
  layer.bindTooltip(`<a title="123" style='width:100%;height:100%;background-color: red;color: white;'>${ts}</a>`, {
    permanent: true, // 始终显示
    direction: 'right',
    sticky: true,
    interactive: true, // 可交互的，就是能被点击到
    offset: [0, 0] // 这个必须是0,0, 上面修改了_updatePosition，缩放的时候才计算偏移
  }).addTo(drawInstance.drawnItems)

  layer.cellid = ts
  // 单击矩形触发
  layer.on('click', function(event) {
    _clickRectangleHandler(event, drawInstance, layer, _map)
  })

  layer.on('dblclick', function(event) {
    console.log('dblclick')
  })
}

// 修改中触发
function _editingRectangleHandler(e, drawInstance) {
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
function _editRectangleHandler(e, drawInstance) {
  var layers = e.layers
  var countOfEditedLayers = 0
  layers.eachLayer(function(layer) {
    countOfEditedLayers++
    console.log(layer.cellid)
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

// 删除结束之后触发
function _removeRectangleHandler(e, drawInstance) {
  var layers = e.layers
  var countOfEditedLayers = 0
  layers.eachLayer(function(layer) {
    countOfEditedLayers++
    // 更新tooltip的位置
    if (layer.getTooltip) {
      var toolTip = layer.getTooltip()
      console.log(toolTip)
      console.log(layer.cellid)
      // if (toolTip) {
      //   toolTip._updatePosition()
      // }
    }
  })
  console.log('删除了 ' + countOfEditedLayers + ' 个图层')
}

function _drawEvent(_map, drawInstance) {
  _map.on(L.Draw.Event.DRAWVERTEX, function() { console.log('DRAWVERTEX') })
  _map.on(L.Draw.Event.TOOLBAROPENED, function() { console.log('TOOLBAROPENED') })
  _map.on(L.Draw.Event.TOOLBARCLOSED, function() { console.log('TOOLBARCLOSED') })
  _map.on(L.Draw.Event.MARKERCONTEXT, function() { console.log('MARKERCONTEXT') })
  _map.on(L.Draw.Event.EDITVERTEX, function(e) { console.log('EDITVERTEX') })
  _map.on(L.Draw.Event.DRAWSTART, function() {
    console.log('DRAWSTART')
    drawInstance.startdraw = true
  })
  _map.on(L.Draw.Event.DRAWSTOP, function() {
    console.log('DRAWSTOP')
    drawInstance.startdraw = false
  })
  _map.on(L.Draw.Event.EDITSTART, function() {
    console.log('EDITSTART')
    drawInstance.startedit = true
  })
  _map.on(L.Draw.Event.EDITSTOP, function() {
    console.log('EDITSTOP')
    drawInstance.startedit = false
  })
  _map.on(L.Draw.Event.DELETESTART, function() {
    console.log('DELETESTART')
    drawInstance.startremove = true
  })
  _map.on(L.Draw.Event.DELETESTOP, function() {
    console.log('DELETESTOP')
    drawInstance.startremove = false
  })
  _map.on(L.Draw.Event.CREATED, function(e,) { // 新画了框
    console.log('CREATED')
    _createRectangleHandler(e, drawInstance, _map)
  })
  _map.on(L.Draw.Event.EDITED, function(e) { // 修改结束
    console.log('EDITED')
    _editRectangleHandler(e, drawInstance)
  })
  _map.on(L.Draw.Event.DELETED, function(e) { // 删除结束
    console.log('DELETED')
    _removeRectangleHandler(e, drawInstance)
  })
  _map.on(L.Draw.Event.EDITMOVE, function(e) { // 修改，平移矩形
    _editingRectangleHandler(e, drawInstance)
  })
  _map.on(L.Draw.Event.EDITRESIZE, function(e) { // 修改，矩形改变大小
    _editingRectangleHandler(e, drawInstance)
  })
}

function _MapDrawCreate(mapInstance, drawInstance) { // 创建画图实例，参数mapInstance是已经初始化的Map实例
  drawInstance.drawnItems = new L.FeatureGroup()
  mapInstance.addLayer(drawInstance.drawnItems)

  var editActions = [
    L.Toolbar2.EditAction.Popup.Edit,
    L.Toolbar2.EditAction.Popup.Delete,
    L.Toolbar2.Action.extendOptions({
      toolbarIcon: {
        className: 'leaflet-draw-draw-marker',
        html: '<span class="fa fa-eyedropper"></span>'
      },
      subToolbar: new L.Toolbar2({ actions: [
        L.ColorPicker.extendOptions({ color: '#db1d0f' }),
        L.ColorPicker.extendOptions({ color: '#025100' }),
        L.ColorPicker.extendOptions({ color: '#ffff00' }),
        L.ColorPicker.extendOptions({ color: '#0000ff' })
      ] })
    })
  ]
  new L.Toolbar2.DrawToolbar({
    position: 'topleft'
  }).addTo(mapInstance)

  mapInstance.on('draw:created', function(evt) {
    var	type = evt.layerType
    var layer = evt.layer

    drawInstance.drawnItems.addLayer(layer)

    layer.on('click', function(event) {
      new L.Toolbar2.EditToolbar.Popup(event.latlng, {
        actions: editActions
      }).addTo(mapInstance, layer)
    })
  })
}

export default class LeafletDrawRectangle {
  constructor(vueInstance, mapInstance) {
    // 下面是全局量
    this.mapInstance = mapInstance
    this.vueInstance = vueInstance
    this.drawnItems = null
    this.drawControl = null
    // 下面是参数
    this.weight = 2
    this.startdraw = false // 画框状态
    this.startedit = false // 修改状态
    this.startremove = false // 删除状态

    _tooltip_init()
    _MapDrawCreate(this.mapInstance, this)
    _drawEvent(this.mapInstance, this)
  }

  clickDrawRec() { // 开始绘制矩形
    this.drawControl._toolbars.draw._modes.rectangle.handler.enable()
  }
  clickEditRec() { // 开始修改
    this.drawControl._toolbars.edit._modes.edit.handler.enable() // 修改所有
  }
  clickRemoveRec() { // 开始删除
    this.drawControl._toolbars.edit._modes.remove.handler.enable() // 开始删除
  }
  clickDrawCancel() { // 取消绘制矩形
    if (!this.startdraw) return
    this.drawControl._toolbars.draw._modes.rectangle.handler.disable() // 取消绘制矩形
  }
  clickCancel() { // 取消修改/删除
    if (!this.startedit && !this.startremove) return
    this.drawControl._toolbars.edit.disable() // 取消修改
  }
  clickSave() { // 保存修改/删除
    if (!this.startedit && !this.startremove) return
    this.drawControl._toolbars.edit._save()
    this.drawControl._toolbars.edit.disable() // 取消修改
  }
  clickRemoveAll() { // 删除所有
    if (!this.startremove) return
    this.drawControl._toolbars.edit._modes.remove.handler.removeAllLayers() // 取消修改
  }
}
