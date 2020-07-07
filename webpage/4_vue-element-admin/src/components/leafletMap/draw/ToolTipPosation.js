import L from 'leaflet'

L.ToolTipPosation = L.Toolbar2.Action.extend({
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
    this.disable()
    const toolTip = this._shape.getTooltip()
    if (toolTip) {
      toolTip.options.direction2 = this.options.direction2
      if (this.options.direction === 'right') {
        toolTip.options.direction = 'right'
      } else if (this.options.direction === 'left') {
        toolTip.options.direction = 'left'
      } else {
        toolTip.options.direction = 'right'
      }
      toolTip._updatePosition()
    }
  },
  _createIcon: function(toolbar, container, args) {
    var colorSwatch = L.DomUtil.create('div')

    L.Toolbar2.Action.prototype._createIcon.call(this, toolbar, container, args)

    L.extend(colorSwatch.style, {
      display: 'flex',
      backgroundColor: '#efefef',
      width: '95px',
      height: L.DomUtil.getStyle(this._link, 'height'),
      border: '3px solid ' + L.DomUtil.getStyle(this._link, 'backgroundColor')
    })

    // 显示细胞类型
    this.cellTypeText = L.DomUtil.create('a', 'cell-option-text')
    this.cellTypeText.innerHTML = `${this.options.label}`
    this.cellTypeText.style.width = '100%'
    this.cellTypeText.style.height = '100%'
    this.cellTypeText.style.backgroundColor = this.options.color
    this.cellTypeText.style.display = 'inline-block'
    this.cellTypeText.style.lineHeight = L.DomUtil.getStyle(this._link, 'height')
    this.cellTypeText.style.textAlign = 'left'
    this.cellTypeText.style.fontSize = '15px'
    this.cellTypeText.style.textIndent = '5%'
    this.cellTypeText.style.color = 'black'
    colorSwatch.appendChild(this.cellTypeText)

    this._link.appendChild(colorSwatch)

    L.DomEvent.on(this._link, 'mouseover', function() {
      this.cellTypeText.style.backgroundColor = '#3399FF'
    }, this)
    L.DomEvent.on(this._link, 'mouseout', function() {
      this.cellTypeText.style.backgroundColor = this.options.color
    }, this)

    L.DomEvent.on(this._link, 'click', function() {
      this._map.removeLayer(this.toolbar.parentToolbar)
    }, this)
  }
})
