import L from 'leaflet'

L.ColorPicker = L.Toolbar2.Action.extend({
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
      toolTip._source.setTooltipContent(`<a title="123" style='width:100%;height:100%;background-color: ${this.options.celltype.typecolor};color: white; display: inline-block;font-size: 15px;'>${this.options.celltype.label}</a>`)
      toolTip._source.celltypeid = this.options.celltype.id
    }
  },
  _createIcon: function(toolbar, container, args) {
    var colorSwatch = L.DomUtil.create('div')

    L.Toolbar2.Action.prototype._createIcon.call(this, toolbar, container, args)

    L.extend(colorSwatch.style, {
      backgroundColor: '#efefef',
      // width: L.DomUtil.getStyle(this._link, 'width'),
      width: '210px',
      height: L.DomUtil.getStyle(this._link, 'height'),
      border: '3px solid ' + L.DomUtil.getStyle(this._link, 'backgroundColor')
    })

    // 显示细胞类型
    this.cellTypeText = L.DomUtil.create('a', 'cell-option-text')
    this.cellTypeText.innerHTML = `${this.options.celltype.label}`
    this.cellTypeText.style.width = '100%'
    this.cellTypeText.style.height = '100%'
    this.cellTypeText.style.backgroundColor = this.options.celltype.choicscolor
    this.cellTypeText.style.display = 'block'
    this.cellTypeText.style.lineHeight = L.DomUtil.getStyle(this._link, 'height')
    this.cellTypeText.style.textAlign = 'left'
    this.cellTypeText.style.border = '1px solid #ccc'
    this.cellTypeText.style.fontSize = '15px'
    this.cellTypeText.style.fontWeight = 'bold'
    this.cellTypeText.style.textIndent = '5%'
    this.cellTypeText.style.color = 'black'
    colorSwatch.appendChild(this.cellTypeText)

    this._link.appendChild(colorSwatch)

    L.DomEvent.on(this._link, 'mouseover', function() {
      this.cellTypeText.style.backgroundColor = '#D8D8D8'
    }, this)
    L.DomEvent.on(this._link, 'mouseout', function() {
      this.cellTypeText.style.backgroundColor = this.options.celltype.choicscolor
    }, this)

    L.DomEvent.on(this._link, 'click', function() {
      this._map.removeLayer(this.toolbar.parentToolbar)
    }, this)
  }
})
