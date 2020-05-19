import { cellsOptionsAll } from '@/const/const'

// newlabelid 生成标注的ID
export function newlabelid(pid, did) {
  var labelid = ('' + pid).padStart(8, '0')
  labelid = labelid + ('' + did).padStart(8, '0')
  labelid = labelid + ('' + (new Date().getTime())).padStart(13, '0')
  labelid = labelid + ('' + parseInt((1 + Math.random()) * 65536)).padStart(5, '0')
  return labelid
}

// cellInFovPosation 使用predict的信息计算出当前细胞在全图的位置, 输入参数cell是从服务器获得的一个predict
export function cellInFovPosation(cell, realimgheight, realimgwidth, imgext) {
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

export function celltypekeys() { // 细胞类型字典
  var celltypes = []
  celltypes = celltypes.concat(cellsOptionsAll)
  celltypes = celltypes.sort(function(a, b) {
    return a.order > b.order
  })

  // 细胞类型字典, 导入系统预测时候使用
  var _celltypekeys = {}
  celltypes.map(v => {
    _celltypekeys[v.id] = v
  })
  return Object.assign({}, _celltypekeys)
}
