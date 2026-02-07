import * as echarts from 'echarts/core'
import { LineChart, BarChart, PieChart } from 'echarts/charts'
import {
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent,
  DataZoomComponent
} from 'echarts/components'
import { CanvasRenderer, SVGRenderer } from 'echarts/renderers'

// 注册模块
echarts.use([
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent,
  DataZoomComponent,
  LineChart,
  BarChart,
  PieChart,
  CanvasRenderer
])

export function initTrendChart() {
  const getChartDom = () => {
    const chartDom = document.getElementById('trend-chart')
    if (!chartDom) {
      console.warn('未找到图表容器：trend-chart')
      return null
    }
    const rect = chartDom.getBoundingClientRect()
    if (rect.width === 0 || rect.height === 0) {
      console.warn('图表容器宽高为0，尝试强制设置默认尺寸')
      chartDom.style.width = '100%'
      chartDom.style.height = '200px'
    }
    return chartDom
  }

    const chartDom = getChartDom()
    if (!chartDom) return

    const myChart = echarts.init(chartDom)
    
    const option = {
      tooltip: {
        trigger: 'axis'
      },
      legend: {
        data: ['点击量', '转化量'], 
        bottom: 0
      },
      grid: {
        left: '4%',
        right: '4%',
        bottom: '10%',
        top: '15%',
        outerBounds: {
          left: 10,
          right: 10,
          top: 10,
          bottom: 10
        }
      },
      xAxis: {
        type: 'category',
        boundaryGap: true,
        data: ['1月', '2月', '3月', '4月', '5月', '6月','7月', '8月', '9月', '10月', '11月', '12月',]
      },
      yAxis: {
        type: 'value',
        name: '数量'
      },
      series: [
        {
          name: '点击量',
          type: 'line',
          smooth: true,
          data: [1200, 1900, 1500, 1132, 876, 1223,1233,789,1245,545,896,1456]
        },
        {
          name: '转化量',
          type: 'bar',
          data: [34, 23, 32, 12, 8, 24,123,231,167,87,45,56]
        }
      ]
    }

    // 渲染图表
    myChart.setOption(option)

    // 自适应窗口大小
    window.addEventListener('resize', () => {
      myChart.resize()
    })

    return myChart
}