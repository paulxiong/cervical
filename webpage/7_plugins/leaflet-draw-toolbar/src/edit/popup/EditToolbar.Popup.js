L.Toolbar2.EditToolbar.Popup = L.Toolbar2.Popup.extend({
	options: {
		actions: [
			L.Toolbar2.EditAction.Popup.Edit,
			L.Toolbar2.EditAction.Popup.Delete
		],
        className: 'leaflet-draw-toolbar'
	},

	onAdd: function (map) {
		var shape = this._arguments[1];

		if (shape instanceof L.Marker) {
			/* Adjust the toolbar position so that it doesn't cover the marker. */
			this.options.anchor = L.point(shape.options.icon.options.popupAnchor);
		}

		L.Toolbar2.Popup.prototype.onAdd.call(this, map);

		// 最笨的办法检测鼠标点在标注外面,如果点在外面就把popup关闭
		var thisPopup = this
		function hidepopup(e) {
			if(!e.latlng || !thisPopup || !thisPopup._map) {
				return
			}
			if(!shape.getBounds().contains(e.latlng)) {
				thisPopup._map.removeLayer(thisPopup)
			}
		}
		setTimeout(function() {
			thisPopup._map.once('click', hidepopup, {capture: false, once: true});
		}, 20);
	}
});
