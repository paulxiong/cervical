<template>
  <div class="main">
    <div id="pieCharts" style="width: 800px;height: 650px;" />
  </div>
</template>

<script>
import echarts from 'echarts'
export default {
  name: 'Index',
  data() {
    return {}
  },
  mounted: function() {
    this.$nextTick(function() {
      this.getPie()
    })
  },
  methods: {
    getPie() {
      // 绘制图表
      var myChart = echarts.init(document.getElementById('pieCharts'))
      // 指定图表的配置项和数据
      var option = {
        title: {
          text: '细胞分布情况', // 主标题文本
          subtext: '虚构数据', // 副标题文本
          left: 'center'// 左对齐
        },
        tooltip: {
          trigger: 'item',
          formatter: '{a} <br/>{b} : {c} ({d}%)'
        },
        legend: {// 图例组件，图例组件展现了不同系列的标记(symbol)，颜色和名字。可以通过点击图例控制哪些系列不显示
          // orient: 'vertical',
          // top: 'middle',
          bottom: 0,
          left: 50,
          textStyle: {// 图例中文字的样式
            color: '#000',
            fontSize: 12
          },
          data: [
            'Norm正常细胞',
            'LSIL鳞状上皮细胞低度病变',
            'HSIL鳞状上皮细胞高度病变',
            'HPV感染',
            'SCC鳞状上皮细胞癌',
            'ASCUS不典型鳞状细胞低',
            'ASCH不典型鳞状细胞高',
            'AGC不典型腺细胞',
            'AIS颈管原位腺癌',
            'ADC腺癌',
            'T滴虫',
            'M霉菌',
            'HSV疱疹',
            'X1线索细胞',
            '阴性细胞',
            '阳性细胞',
            '未知类型',
            '不是细胞'
          ] // 图例上显示的饼图各模块上的名字
        },
        // 饼图中各模块的颜色
        color: [
          '#008B00',
          '#7CFC00',
          '#C0FF3E',
          '#9370DB',
          '#00FF7F',
          '#40E0D0',
          '#00BFFF',
          '#DAA520',
          '#BDB76B',
          '#BCEE68',
          '#BCD2EE',
          '#BC8F8F',
          '#121212',
          '#D8BFD8',
          '#BA55D3',
          '#EEC900',
          '#EE3B3B',
          '#B8860B'
        ],
        series: [
          {
            name: '细胞占比',
            type: 'pie',
            radius: '70%',
            border: 100,
            right: 100,
            textStyle: {
              fontSize: 14
            },
            data: [
              { name: 'Norm正常细胞', value: 10 },
              { name: 'LSIL鳞状上皮细胞低度病变', value: 5 },
              { name: 'HSIL鳞状上皮细胞高度病变', value: 5 },
              { name: 'HPV感染', value: 5 },
              { name: 'SCC鳞状上皮细胞癌', value: 5 },
              { name: 'ASCUS不典型鳞状细胞低', value: 5 },
              { name: 'ASCH不典型鳞状细胞高', value: 10 },
              { name: 'AGC不典型腺细胞', value: 5 },
              { name: 'AIS颈管原位腺癌', value: 5 },
              { name: 'ADC腺癌', value: 10 },
              { name: 'T滴虫', value: 5 },
              { name: 'M霉菌', value: 5 },
              { name: 'HSV疱疹', value: 10 },
              { name: 'X1线索细胞', value: 5 },
              { name: '阴性细胞', value: 5 },
              { name: '阳性细胞', value: 5 },
              { name: '未知类型', value: 10 },
              { name: '不是细胞', value: 5 }
            ],
            itemStyle: {// 用于设置样式
              emphasis: {// 饼状图高亮时的背景样式
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: 'rgba(0, 0, 0, 0.8)'
              }
            }
          }
        ]
      }
      // 使用刚指定的配置项和数据显示图表
      myChart.setOption(option)
    }
  }
}
</script>

<style lang="scss" scoped>
.main {
  background: #fff;
  padding: 10px 0;
}
</style>
