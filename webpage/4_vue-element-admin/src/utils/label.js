import { cellsOptionsAll } from '@/const/const'

// newlabelid 生成标注的ID
export function newlabelid(pid, did) {
  var labelid = '' + (new Date().getTime())
  labelid = labelid + ('' + parseInt((1 + Math.random()) * 65536)).padStart(6, '0')
  return labelid
}

// cellInFullPosation 使用predict的信息计算出当前细胞在全图的位置, 输入参数cell是从服务器获得的一个predict
export function cellInFullPosation(cell, realimgheight, realimgwidth, imgext) {
  let arr = cell.cellpath.split('IMG')
  arr = arr[1].split(imgext)
  arr = arr[0].split('x')
  const x = parseInt(arr[1])
  const y = parseInt(arr[0])
  var y1 = parseInt((y - 1) * realimgheight + cell.y1)
  var x1 = parseInt((x - 1) * realimgwidth + cell.x1)
  var y2 = parseInt((y - 1) * realimgheight + cell.y2)
  var x2 = parseInt((x - 1) * realimgwidth + cell.x2)

  y1 = -y1 // 在第四像限，所以y是负数
  y2 = -y2 // 在第四像限，所以y是负数

  var points = []
  points.push([y1, x1])
  points.push([y2, x2])
  var _cell = Object.assign({}, cell)
  _cell.points = points
  return _cell
}

// fullPosation2Fov 使用当前细胞在全图的位置计算出一条类似predict的信息, 输入lanbelinfo的x1,y1,x2,y2是在全图上的坐标
export function fullPosation2Fov(labelinfo, realimgheight, realimgwidth, imgext) {
  var x = parseInt((labelinfo.x1 + labelinfo.x2) / 2)
  var y = parseInt((labelinfo.y1 + labelinfo.y2) / 2)
  x = parseInt(x / realimgwidth)
  y = parseInt(y / realimgheight)
  console.log(x, y)
}

export function celltypekeys() { // 细胞类型字典
  var celltypes = []
  celltypes = celltypes.concat(cellsOptionsAll)
  celltypes = celltypes.sort(function(a, b) {
    return (a.order - b.order)
  })

  // 细胞类型字典, 导入系统预测时候使用
  var _celltypekeys = {}
  celltypes.map(v => {
    _celltypekeys[v.id] = v
  })
  return Object.assign({}, _celltypekeys)
}
