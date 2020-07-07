import L from 'leaflet'
import { tooltipContent } from './element.js'

L.CellTypePicker = L.Toolbar2.Action.extend({
  options: {
    toolbarIcon: { className: 'leaflet-color-swatch' }
  },
  initialize: function(map, shape, options) {
    this._map = map
    this._shape = shape
    L.setOptions(this, options)
    L.Toolbar2.Action.prototype.initialize.call(this, map, options)
  },
  addHooks: function() {
    this._shape.setStyle({ color: this.options.celltype.typecolor })
    this.disable()
    const toolTip = this._shape.getTooltip()
    if (toolTip) {
      if (toolTip._source.celltype !== this.options.celltype) {
        toolTip._source.setTooltipContent(tooltipContent(this.options.celltype))
        toolTip._source.celltype = this.options.celltype
        this._map.fire('draw:updatelabel', { layers: L.layerGroup([this._shape]) })
      }
    }
  },
  _createIcon: function(toolbar, container, args) {
    var colorSwatch = L.DomUtil.create('div')

    L.Toolbar2.Action.prototype._createIcon.call(this, toolbar, container, args)

    L.extend(colorSwatch.style, {
      display: 'flex',
      backgroundColor: '#efefef',
      width: '400px',
      height: L.DomUtil.getStyle(this._link, 'height'),
      border: '3px solid ' + L.DomUtil.getStyle(this._link, 'backgroundColor')
    })

    // 显示细胞类型
    this.cellTypeText = L.DomUtil.create('a', 'cell-option-text')
    this.cellTypeText.innerHTML = `${this.options.celltype.shortname}`
    this.cellTypeText.style.width = '20%'
    this.cellTypeText.style.height = '100%'
    this.cellTypeText.style.backgroundColor = this.options.celltype.choicscolor
    this.cellTypeText.style.display = 'inline-block'
    this.cellTypeText.style.lineHeight = L.DomUtil.getStyle(this._link, 'height')
    this.cellTypeText.style.textAlign = 'left'
    this.cellTypeText.style.fontSize = '15px'
    this.cellTypeText.style.textIndent = '5%'
    this.cellTypeText.style.color = 'black'
    colorSwatch.appendChild(this.cellTypeText)

    this.cellTypeText2 = L.DomUtil.create('a', 'cell-option-text')
    this.cellTypeText2.innerHTML = `${this.options.celltype.label}`
    this.cellTypeText2.style.width = '80%'
    this.cellTypeText2.style.height = '100%'
    this.cellTypeText2.style.backgroundColor = this.options.celltype.choicscolor
    this.cellTypeText2.style.display = 'inline-block'
    this.cellTypeText2.style.lineHeight = L.DomUtil.getStyle(this._link, 'height')
    this.cellTypeText2.style.textAlign = 'left'
    this.cellTypeText2.style.fontSize = '13px'
    this.cellTypeText2.style.color = 'black'
    colorSwatch.appendChild(this.cellTypeText2)

    this._link.appendChild(colorSwatch)

    L.DomEvent.on(this._link, 'mouseover', function() {
      this.cellTypeText.style.backgroundColor = '#3399FF'
      this.cellTypeText2.style.backgroundColor = '#3399FF'
    }, this)
    L.DomEvent.on(this._link, 'mouseout', function() {
      this.cellTypeText.style.backgroundColor = this.options.celltype.choicscolor
      this.cellTypeText2.style.backgroundColor = this.options.celltype.choicscolor
    }, this)

    L.DomEvent.on(this._link, 'click', function() {
      this._map.removeLayer(this.toolbar.parentToolbar)
    }, this)
  }
})
