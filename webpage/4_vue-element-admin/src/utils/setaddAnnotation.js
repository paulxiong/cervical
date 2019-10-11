export function setaddAnnotation(id, url, item, divide) {
  window.AnalyserNode.setProperties({
    outline: item.color,
    outline_width: 3,
    stroke: 'yellow'
  })
  window.anno.makeAnnotatable(document.getElementById(id))
  for (let i = 0; i < item.length; i++) {
    var annotation = {
      src: url,
      text: '' + item[i].typeout,
      units: 'pixel',
      editable: true,
      shapes: [
        {
          type: 'rect',
          units: 'pixel',
          geometry: {
            x: parseInt(item[i].x / divide),
            y: parseInt(item[i].y / divide),
            width:
              item[i].w <= divide ? 1 : parseInt(item[i].w / divide),
            height:
              item[i].h <= divide ? 1 : parseInt(item[i].h / divide)
          }
        }
      ]
    }
    // 添加头像框到画布里
    window.anno.addAnnotation(annotation)
    // window.anno.highlightAnnotation(annotation)
  }
}
