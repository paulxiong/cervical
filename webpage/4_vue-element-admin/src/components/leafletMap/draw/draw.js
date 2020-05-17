import L from 'leaflet'
import 'leaflet-draw'
import 'leaflet-toolbar'
import 'leaflet-draw-toolbar/dist/leaflet.draw-toolbar.js'
import './CellTypePicker.js'
import './ToolTipPosation.js'
import { cellsOptionsAll } from '@/const/const'
import { tooltipContent } from './element.js'

function _celltype_init() {
  var celltypes = []
  celltypes = celltypes.concat(cellsOptionsAll)
  celltypes = celltypes.sort(function(a, b) {
    return a.order > b.order
  })

  // 细胞类型字典, 导入系统预测时候使用
  var celltypekeys = {}
  celltypes.map(v => {
    celltypekeys[v.id] = v
  })

  // 创建菜单列表
  const menuitems = []
  var unkownCell = null
  for (var i = 0; i < celltypes.length; i++) {
    if (celltypes[i].id === 100) {
      unkownCell = Object.assign({}, celltypes[i])
    }
    if (celltypes[i].notcelltype) {
      continue
    }
    menuitems.push(L.CellTypePicker.extendOptions({ 'color': celltypes[i].choicscolor, 'celltype': celltypes[i] }))
  }

  // tooltip的位置列表
  var toolTipPosation = []
  toolTipPosation.push(L.ToolTipPosation.extendOptions({ 'label': '右上', 'color': '#ffdca8', 'direction': 'right', 'direction2': 'top' }))
  toolTipPosation.push(L.ToolTipPosation.extendOptions({ 'label': '右下', 'color': '#ffdca8', 'direction': 'right', 'direction2': 'bottom' }))
  toolTipPosation.push(L.ToolTipPosation.extendOptions({ 'label': '左下', 'color': '#ffdca8', 'direction': 'left', 'direction2': 'bottom' }))
  toolTipPosation.push(L.ToolTipPosation.extendOptions({ 'label': '左上', 'color': '#ffdca8', 'direction': 'left', 'direction2': 'top' }))

  return { 'menuitems': menuitems, 'unkownCell': unkownCell, 'toolTipPosation': toolTipPosation, 'celltypekeys': celltypekeys }
}

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
      var x1y1 = this._source._bounds._northEast
      if (this.options.direction === 'left') {
        if (this.options.direction2 === 'top') {
          x1y1 = this._source.getBounds().getNorthWest() // 左上
        } else if (this.options.direction2 === 'bottom') {
          x1y1 = this._source.getBounds().getSouthWest() // 左下
        }
      } else if (this.options.direction === 'right') {
        if (this.options.direction2 === 'top') {
          x1y1 = this._source.getBounds().getNorthEast() // 右上
        } else if (this.options.direction2 === 'bottom') {
          x1y1 = this._source.getBounds().getSouthEast() // 右下
        }
      }
      pos = this._map.latLngToLayerPoint(x1y1)
    }
    this._setPosition(pos)
  }
}

// 画完一个正方形触发, 设置菜单和事件, celltypeinfo只在导入系统预测时候才有，手动画的时候没有, 是const.js里面定义的其中一种细胞类型
function _createRectangleHandler(e, drawInstance, _map, celltypeinfo) {
  var type = e.layerType
  if (type !== 'rectangle') { // 目前只支持画矩形
    return
  }
  const _celltypeinfo = celltypeinfo || drawInstance.unkownCell
  var layer = e.layer
  // 参考 https://github.com/Leaflet/Leaflet/blob/master/src/layer/Tooltip.js
  layer.bindTooltip(tooltipContent(_celltypeinfo), {
    permanent: true, // 始终显示
    direction: 'right',
    direction2: 'top', // 这个是我们自己加的
    sticky: true,
    interactive: false, // 可交互的，就是能被点击到, 调试样式要改成true
    offset: [0, 0] // 这个必须是0,0, 上面修改了_updatePosition，缩放的时候才计算偏移
  }).addTo(drawInstance.drawnItems)
  layer.celltypeid = _celltypeinfo.id // 默认是200--未知类型

  // 创建菜单
  drawInstance.drawnItems.addLayer(layer)
  var editActions = [
    L.Toolbar2.EditAction.Popup.Edit,
    L.Toolbar2.EditAction.Popup.Delete,
    L.Toolbar2.Action.extendOptions({
      toolbarIcon: {
        className: 'leaflet-draw-draw-marker',
        html: '<span class="fa fa-eyedropper"></span>'
      },
      subToolbar: new L.Toolbar2({ actions: drawInstance.menuitems })
    }),
    L.Toolbar2.Action.extendOptions({
      toolbarIcon: {
        className: 'leaflet-draw-draw-rectangle',
        html: '<span class="fa fa-rectangle"></span>'
      },
      subToolbar: new L.Toolbar2({ actions: drawInstance.toolTipPosation })
    })
  ]
  // 单击矩形触发菜单
  layer.on('click', function(event) {
    if (!event || !event.sourceTarget || !event.latlng) {
      return
    }

    // 点在矩形上才弹出，tooltip上不要弹出菜单
    if (event.sourceTarget.getBounds().contains(event.latlng)) {
      new L.Toolbar2.EditToolbar.Popup(event.latlng, {
        actions: editActions
      }).addTo(_map, layer)
    }
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
    _createRectangleHandler(e, drawInstance, _map, null)
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

  drawInstance.drawControl = new L.Control.Draw({ // 这个是leaflet.draw提供，编辑和删除是全局控制
    position: 'topright',
    draw: {
      polyline: false, // 不准画线
      polygon: false, // 不准画多边形
      circle: false, // 不准画圆
      marker: false, // 不准画标记
      circlemarker: false,
      rectangle: { shapeOptions: drawInstance.rectangleOptions }
    },
    edit: {
      featureGroup: drawInstance.drawnItems,
      poly: {
        allowIntersection: false
      },
      remove: true
    }
  })
  if (mapInstance.addControl(drawInstance.drawControl)) {
    console.log('addControl')
  }

  new L.Toolbar2.DrawToolbar({ // 这个是leaflet-draw-toolbar提供，编辑和删除是单个控制
    position: 'topright',
    actions: [L.Toolbar2.DrawAction.Rectangle]
  }).addTo(mapInstance)
}

function _cellPosation(cell, vueInstance) { // 使用predict的信息计算出当前细胞在全图的位置, 输入参数cell是从服务器获得的一个predict
  let arr = cell.cellpath.split('IMG')
  arr = arr[1].split(vueInstance.args.imgext)
  arr = arr[0].split('x')
  let x = parseInt(arr[1])
  let y = parseInt(arr[0])
  y = (y - 1) * vueInstance.args.realimgheight + cell.y1
  x = (x - 1) * vueInstance.args.realimgwidth + cell.x1

  y = -y // 在第四像限，所以y是负数
  var points = []
  points.push([y, x])
  points.push([y, x + 100])
  points.push([y - 100, x + 100])
  points.push([y - 100, x])
  cell.points = points
}

function _drawrectangle(drawInstance, mapInstance, cellinfo) {
  _cellPosation(cellinfo, drawInstance.vueInstance)

  var rectangle = new L.Rectangle(cellinfo.points, drawInstance.rectangleOptions)
  rectangle.addTo(drawInstance.drawnItems)

  const e = {
    layerType: 'rectangle',
    layer: rectangle
  }

  const _celltype = drawInstance.celltypekeys[cellinfo.predict_type] || drawInstance.unkownCell

  // 创建菜单，设置事件
  _createRectangleHandler(e, drawInstance, mapInstance, _celltype)
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

    const ret = _celltype_init() // 所有细胞类型
    this.menuitems = ret.menuitems // 所有细胞类型
    this.unkownCell = ret.unkownCell // 未知类型，标注初始化时候使用
    this.toolTipPosation = ret.toolTipPosation // toolTip的位置列表
    this.celltypekeys = ret.celltypekeys // 细胞类型字典, 导入系统预测时候使用

    // 矩形框参数
    this.rectangleOptions = {
      opacity: 1,
      clickable: true,
      fillOpacity: 0, // 填充完全透明
      color: this.unkownCell.typecolor, // 边框颜色
      weight: this.weight
    }

    _tooltip_init()
    _MapDrawCreate(this.mapInstance, this)
    _drawEvent(this.mapInstance, this)
  }
  drawrectangle(cellinfo) {
    _drawrectangle(this, this.mapInstance, cellinfo)
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
