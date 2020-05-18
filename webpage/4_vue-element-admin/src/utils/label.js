// newlabelid 生成标注的ID
export function newlabelid(pid, did) {
  var labelid = ('' + pid).padStart(8, '0')
  labelid = labelid + ('' + did).padStart(8, '0')
  labelid = labelid + ('' + (new Date().getTime())).padStart(13, '0')
  labelid = labelid + ('' + parseInt((1 + Math.random()) * 65536)).padStart(5, '0')
  return labelid
}
