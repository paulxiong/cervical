export function tooltipContent(options) {
  return `<a title=${options.label} style='display:inline-block;width:100%;height:100%;background-color:${options.typecolor};color:white;font-size: 15px;'>${options.shortname}</a>`
}
