var ini = require('ini')

function _filelist(cfg) {
  cfg.filelist = {} // 文件名做key，值默认是false
  for (var i = 1; i <= parseInt(cfg.RowCount); i++) {
    for (var j = 1; j <= parseInt(cfg.ColumnCount); j++) {
      var imgfile = cfg.ImageFileName
      imgfile = imgfile.replace('\%1', ('' + i).padStart(3, '0'))
      imgfile = imgfile.replace('\%2', ('' + j).padStart(3, '0'))
      cfg.filelist[imgfile] = false
    }
  }
  cfg.filelist[cfg.Preview] = false
  cfg.filelist[cfg.Result] = false
}

export function scanTxtParse(text) {
  var config = {}
  text = text.replace(new RegExp('#', 'g'), '\\#') // 特殊字符处理
  try {
    var cfg = ini.parse(text)
    if (!cfg || !cfg.General || !cfg.General.ImagesPath) {
      return config
    }
    config.ImageFileName = cfg.General.ImageFileName
    config.ColumnCount = cfg.General.ColumnCount
    config.RowCount = cfg.General.RowCount
    config.Preview = cfg.General.Preview
    config.Result = cfg.General.Result

    _filelist(config)
  } catch (err) {
    config = {}
  }
  return config
}

// fileListObj 是从scan.txt里面解析出需要的文件的列表， filelist是插件从本地扫描出来的文件数组
export function checkFileList(fileListObj, filelist) {
  var lostfiles = []
  var _fileListObj = Object.assign({}, fileListObj)
  for (var i = 0; i < filelist.length; i++) {
    if (_fileListObj.hasOwnProperty(filelist[i].name)) {
      _fileListObj[filelist[i].name] = true
    }
  }

  for (var key in _fileListObj) {
    if (!_fileListObj[key]) {
      lostfiles.push(key)
    }
  }
  return lostfiles
}

