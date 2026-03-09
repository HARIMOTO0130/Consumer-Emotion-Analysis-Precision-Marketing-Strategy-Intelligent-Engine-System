import axios from 'axios'

// Odoo 19系统连接配置
const ODOO_CONFIG = {
  baseUrl: 'http://localhost:8069',
  database: 'xiangcai_restaurant_db',
  username: 'admin',
  password: 'admin123',
  apiKey: 'xiangcai_analytics_key_2024'
}

// Odoo API端点
const ODOO_ENDPOINTS = {
  sales: '/api/v1/sales/transactions',
  products: '/api/v1/products/menu_items',
  customers: '/api/v1/customers/dining_history',
  inventory: '/api/v1/inventory/stock',
  reports: '/api/v1/reports/sales_summary'
}

/**
 * POS数据服务 - 支持Odoo 19系统对接和CSV数据导入
 * 统一数据框架，支持多种数据源
 */
class POSDataService {
  constructor() {
    this.data = null
    this.loading = false
    this.error = null
    this.fieldMapping = null // CSV字段映射配置
  }

  /**
   * 从Odoo 19系统获取POS数据
   * @param {Object} config - Odoo连接配置
   * @param {Object} options - 查询选项
   * @returns {Promise<Object>} POS数据
   */
  async fetchFromOdoo(config, options = {}) {
    this.loading = true
    this.error = null
    
    try {
      const { host, database, username, password, model = 'pos.order' } = config
      
      // 构建Odoo RPC请求
      const rpcData = {
        jsonrpc: '2.0',
        method: 'call',
        params: {
          service: 'object',
          method: 'execute_kw',
          args: [
            database,
            1, // 用户ID，通常为1
            password,
            model,
            'search_read',
            [
              options.domain || [], // 过滤条件
              options.fields || ['id', 'date_order', 'amount_total', 'lines', 'partner_id', 'session_id']
            ],
            {
              limit: options.limit || 1000,
              offset: options.offset || 0,
              order: options.order || 'date_order desc'
            }
          ]
        }
      }

      const response = await axios.post(`${host}/jsonrpc`, rpcData, {
        headers: {
          'Content-Type': 'application/json'
        }
      })

      if (response.data.error) {
        throw new Error(`Odoo API错误: ${response.data.error.message}`)
      }

      // 转换Odoo数据格式为统一格式
      const convertedData = this.convertOdooData(response.data.result)
      
      this.data = convertedData
      this.loading = false
      
      return convertedData
      
    } catch (error) {
      this.error = error.message
      this.loading = false
      throw error
    }
  }

  /**
   * 转换Odoo数据格式为统一格式
   * @param {Array} odooData - Odoo返回的原始数据
   * @returns {Object} 统一格式的数据
   */
  convertOdooData(odooData) {
    const rows = odooData.map(order => {
      // 计算订单总销售额和总数量
      let totalSales = order.amount_total || 0
      let totalQuantity = 0
      
      // 如果有订单行数据，计算详细信息
      if (order.lines && Array.isArray(order.lines)) {
        order.lines.forEach(line => {
          totalQuantity += line.qty || 0
        })
      }

      return {
        date: order.date_order ? new Date(order.date_order).toISOString().split('T')[0] : null,
        product: order.lines && order.lines[0] ? order.lines[0].product_id[1] : 'Unknown',
        category: order.lines && order.lines[0] ? order.lines[0].product_id[1] : 'General',
        sales: totalSales,
        quantity: totalQuantity,
        customer_type: order.partner_id ? 'Registered' : 'Guest',
        order_id: order.id,
        customer_name: order.partner_id ? order.partner_id[1] : 'Guest',
        session_id: order.session_id ? order.session_id[1] : null
      }
    })

    return {
      source: 'odoo',
      rows,
      metadata: {
        totalRecords: rows.length,
        dateRange: this.getDateRange(rows),
        categories: this.getUniqueValues(rows, 'category'),
        products: this.getUniqueValues(rows, 'product'),
        customerTypes: this.getUniqueValues(rows, 'customer_type'),
        sourceSystem: 'Odoo 19 POS'
      }
    }
  }

  /**
   * 从CSV文件导入数据
   * @param {File} file - CSV文件
   * @param {Object} mapping - 字段映射配置
   * @returns {Promise<Object>} 解析后的数据
   */
  async importCSV(file, mapping) {
    this.loading = true
    this.error = null
    this.fieldMapping = mapping
    
    try {
      // 读取文件内容
      const text = await this.readFileAsText(file)
      
      // 解析CSV数据
      const parsedData = this.parseCSV(text, mapping)
      
      // 验证数据格式
      this.validateData(parsedData)
      
      this.data = parsedData
      this.loading = false
      
      return parsedData
    } catch (error) {
      this.error = error.message
      this.loading = false
      throw error
    }
  }

  /**
   * 读取文件为文本
   * @param {File} file - 文件对象
   * @returns {Promise<string>} 文件内容
   */
  readFileAsText(file) {
    return new Promise((resolve, reject) => {
      const reader = new FileReader()
      reader.onload = (e) => resolve(e.target.result)
      reader.onerror = () => reject(new Error('文件读取失败'))
      reader.readAsText(file)
    })
  }

  /**
   * 解析CSV数据
   * @param {string} csvText - CSV文本内容
   * @param {Object} mapping - 字段映射配置
   * @returns {Object} 解析后的数据对象
   */
  parseCSV(csvText, mapping) {
    const lines = csvText.split('\n').filter(line => line.trim())
    if (lines.length < 2) {
      throw new Error('CSV文件内容为空或格式不正确')
    }

    // 解析表头
    const headers = lines[0].split(',').map(h => h.trim())
    
    // 验证映射配置
    const requiredFields = ['date', 'product', 'sales', 'quantity']
    const missingMappings = requiredFields.filter(field => !mapping[field])
    if (missingMappings.length > 0) {
      throw new Error(`字段映射配置缺少必需字段: ${missingMappings.join(', ')}`)
    }

    // 验证CSV表头是否包含所有必需字段
    const missingHeaders = requiredFields.filter(field => {
      const csvField = mapping[field]
      return !headers.includes(csvField)
    })
    
    if (missingHeaders.length > 0) {
      throw new Error(`CSV文件缺少必需字段: ${missingHeaders.join(', ')}`)
    }

    // 解析数据行
    const data = []
    const errors = []
    
    for (let i = 1; i < lines.length; i++) {
      try {
        const values = lines[i].split(',').map(v => v.trim())
        const row = this.mapCSVRow(headers, values, mapping, i + 1)
        data.push(row)
      } catch (error) {
        errors.push(`第${i + 1}行: ${error.message}`)
      }
    }

    // 如果有解析错误，抛出异常而不是返回部分数据
    if (errors.length > 0) {
      throw new Error(`CSV解析错误:\n${errors.join('\n')}`)
    }

    return {
      source: 'csv',
      headers,
      rows: data,
      metadata: {
        totalRecords: data.length,
        dateRange: this.getDateRange(data),
        categories: this.getUniqueValues(data, 'category'),
        products: this.getUniqueValues(data, 'product'),
        customerTypes: this.getUniqueValues(data, 'customer_type'),
        sourceSystem: 'CSV文件导入',
        fieldMapping: mapping
      }
    }
  }

  /**
   * 映射CSV行到统一格式
   * @param {Array} headers - CSV表头
   * @param {Array} values - CSV行值
   * @param {Object} mapping - 字段映射配置
   * @param {number} rowIndex - 行号（用于错误报告）
   * @returns {Object} 映射后的行数据
   */
  mapCSVRow(headers, values, mapping, rowIndex) {
    const row = {}
    
    // 映射必需字段
    row.date = this.parseDate(values[headers.indexOf(mapping.date)], rowIndex)
    row.product = values[headers.indexOf(mapping.product)] || 'Unknown'
    row.sales = this.parseNumber(values[headers.indexOf(mapping.sales)], 'sales', rowIndex)
    row.quantity = this.parseInteger(values[headers.indexOf(mapping.quantity)], 'quantity', rowIndex)
    
    // 映射可选字段
    row.category = values[headers.indexOf(mapping.category)] || 'General'
    row.customer_type = values[headers.indexOf(mapping.customer_type)] || 'Guest'
    row.customer_name = values[headers.indexOf(mapping.customer_name)] || null
    row.order_id = values[headers.indexOf(mapping.order_id)] || null

    return row
  }

  /**
   * 解析日期字段
   * @param {string} value - 日期字符串
   * @param {number} rowIndex - 行号
   * @returns {string} 格式化的日期字符串
   */
  parseDate(value, rowIndex) {
    if (!value) {
      throw new Error(`日期字段不能为空`)
    }
    
    const date = new Date(value)
    if (isNaN(date)) {
      throw new Error(`日期格式无效: ${value}`)
    }
    
    return date.toISOString().split('T')[0]
  }

  /**
   * 解析数值字段
   * @param {string} value - 数值字符串
   * @param {string} fieldName - 字段名
   * @param {number} rowIndex - 行号
   * @returns {number} 解析后的数值
   */
  parseNumber(value, fieldName, rowIndex) {
    if (!value) {
      throw new Error(`${fieldName}字段不能为空`)
    }
    
    const num = parseFloat(value.replace(/,/g, ''))
    if (isNaN(num) || num < 0) {
      throw new Error(`${fieldName}字段必须为非负数值: ${value}`)
    }
    
    return num
  }

  /**
   * 解析整数字段
   * @param {string} value - 整数字符串
   * @param {string} fieldName - 字段名
   * @param {number} rowIndex - 行号
   * @returns {number} 解析后的整数
   */
  parseInteger(value, fieldName, rowIndex) {
    if (!value) {
      throw new Error(`${fieldName}字段不能为空`)
    }
    
    const num = parseInt(value.replace(/,/g, ''))
    if (isNaN(num) || num < 0) {
      throw new Error(`${fieldName}字段必须为非负整数: ${value}`)
    }
    
    return num
  }

  /**
   * 验证数据格式
   * @param {Object} data - 解析后的数据
   */
  validateData(data) {
    if (!data || !data.rows || data.rows.length === 0) {
      throw new Error('CSV文件中没有有效数据')
    }

    // 验证每行数据的完整性
    data.rows.forEach((row, index) => {
      if (!row.date || !row.product || row.sales == null || row.quantity == null) {
        throw new Error(`第${index + 1}行数据不完整`)
      }
    })
  }

  /**
   * 获取日期范围
   * @param {Array} rows - 数据行
   * @returns {Object} 日期范围对象
   */
  getDateRange(rows) {
    const dates = rows.map(row => new Date(row.date)).filter(date => !isNaN(date))
    if (dates.length === 0) {
      return { start: null, end: null }
    }
    
    const start = new Date(Math.min(...dates))
    const end = new Date(Math.max(...dates))
    
    return {
      start: start.toISOString().split('T')[0],
      end: end.toISOString().split('T')[0]
    }
  }

  /**
   * 获取唯一值列表
   * @param {Array} rows - 数据行
   * @param {string} field - 字段名
   * @returns {Array} 唯一值数组
   */
  getUniqueValues(rows, field) {
    const values = rows.map(row => row[field]).filter(v => v)
    return [...new Set(values)]
  }

  /**
   * 获取销售数据聚合
   * @param {Object} data - POS数据
   * @returns {Object} 聚合数据
   */
  getSalesAggregation(data) {
    const aggregation = {
      totalSales: 0,
      totalQuantity: 0,
      dailySales: {},
      categorySales: {},
      productSales: {},
      customerTypeSales: {}
    }

    data.rows.forEach(row => {
      const sales = parseFloat(row.sales)
      const quantity = parseInt(row.quantity)
      const date = row.date
      const category = row.category
      const product = row.product
      const customerType = row.customer_type

      // 总计
      aggregation.totalSales += sales
      aggregation.totalQuantity += quantity

      // 按日期聚合
      if (!aggregation.dailySales[date]) {
        aggregation.dailySales[date] = { sales: 0, quantity: 0 }
      }
      aggregation.dailySales[date].sales += sales
      aggregation.dailySales[date].quantity += quantity

      // 按类别聚合
      if (!aggregation.categorySales[category]) {
        aggregation.categorySales[category] = { sales: 0, quantity: 0 }
      }
      aggregation.categorySales[category].sales += sales
      aggregation.categorySales[category].quantity += quantity

      // 按产品聚合
      if (!aggregation.productSales[product]) {
        aggregation.productSales[product] = { sales: 0, quantity: 0 }
      }
      aggregation.productSales[product].sales += sales
      aggregation.productSales[product].quantity += quantity

      // 按客户类型聚合
      if (!aggregation.customerTypeSales[customerType]) {
        aggregation.customerTypeSales[customerType] = { sales: 0, quantity: 0 }
      }
      aggregation.customerTypeSales[customerType].sales += sales
      aggregation.customerTypeSales[customerType].quantity += quantity
    })

    return aggregation
  }

  /**
   * 获取时间序列数据用于图表
   * @param {Object} data - POS数据
   * @param {string} timeRange - 时间范围 ('daily', 'weekly', 'monthly')
   * @returns {Object} 时间序列数据
   */
  getTimeSeriesData(data, timeRange = 'daily') {
    const aggregation = this.getSalesAggregation(data)
    const timeSeries = {
      dates: [],
      sales: [],
      quantity: []
    }

    // 获取日期范围
    const startDate = new Date(data.metadata.dateRange.start)
    const endDate = new Date(data.metadata.dateRange.end)

    // 根据时间范围生成日期序列
    const currentDate = new Date(startDate)
    while (currentDate <= endDate) {
      const dateStr = currentDate.toISOString().split('T')[0]
      
      if (timeRange === 'daily') {
        timeSeries.dates.push(dateStr)
        timeSeries.sales.push(aggregation.dailySales[dateStr]?.sales || 0)
        timeSeries.quantity.push(aggregation.dailySales[dateStr]?.quantity || 0)
        currentDate.setDate(currentDate.getDate() + 1)
      } else if (timeRange === 'weekly') {
        // 简化周聚合逻辑
        const weekStart = new Date(currentDate)
        weekStart.setDate(currentDate.getDate() - currentDate.getDay())
        const weekEnd = new Date(weekStart)
        weekEnd.setDate(weekStart.getDate() + 6)
        
        let weekSales = 0
        let weekQuantity = 0
        
        for (let d = new Date(weekStart); d <= weekEnd; d.setDate(d.getDate() + 1)) {
          const dStr = d.toISOString().split('T')[0]
          weekSales += aggregation.dailySales[dStr]?.sales || 0
          weekQuantity += aggregation.dailySales[dStr]?.quantity || 0
        }
        
        timeSeries.dates.push(`${weekStart.toISOString().split('T')[0]} - ${weekEnd.toISOString().split('T')[0]}`)
        timeSeries.sales.push(weekSales)
        timeSeries.quantity.push(weekQuantity)
        
        currentDate.setDate(currentDate.getDate() + 7)
      }
    }

    return timeSeries
  }

  /**
   * 获取饼图数据
   * @param {Object} data - POS数据
   * @param {string} type - 数据类型 ('category', 'product', 'customer_type')
   * @returns {Array} 饼图数据数组
   */
  getPieChartData(data, type) {
    const aggregation = this.getSalesAggregation(data)
    let sourceData = null

    switch (type) {
      case 'category':
        sourceData = aggregation.categorySales
        break
      case 'product':
        sourceData = aggregation.productSales
        break
      case 'customer_type':
        sourceData = aggregation.customerTypeSales
        break
      default:
        throw new Error('不支持的数据类型')
    }

    return Object.entries(sourceData).map(([name, values]) => ({
      name,
      value: values.sales,
      quantity: values.quantity
    }))
  }

  /**
   * 获取柱状图数据
   * @param {Object} data - POS数据
   * @param {string} type - 数据类型 ('category', 'product', 'customer_type')
   * @returns {Object} 柱状图数据
   */
  getBarChartData(data, type) {
    const pieData = this.getPieChartData(data, type)
    
    return {
      categories: pieData.map(item => item.name),
      sales: pieData.map(item => item.value),
      quantity: pieData.map(item => item.quantity)
    }
  }

  /**
   * 获取当前数据状态
   * @returns {Object} 数据状态
   */
  getStatus() {
    return {
      hasData: !!this.data,
      loading: this.loading,
      error: this.error,
      metadata: this.data?.metadata || null,
      fieldMapping: this.fieldMapping
    }
  }

  /**
   * 清除当前数据
   */
  clearData() {
    this.data = null
    this.loading = false
    this.error = null
    this.fieldMapping = null
  }

  /**
   * 获取默认字段映射配置
   * @returns {Object} 默认映射配置
   */
  getDefaultMapping() {
    return {
      date: 'date',
      product: 'product',
      category: 'category',
      sales: 'sales',
      quantity: 'quantity',
      customer_type: 'customer_type',
      customer_name: 'customer_name',
      order_id: 'order_id'
    }
  }

  /**
   * 验证字段映射配置
   * @param {Object} mapping - 字段映射配置
   * @param {Array} csvHeaders - CSV表头
   * @returns {Object} 验证结果
   */
  validateMapping(mapping, csvHeaders) {
    const result = {
      valid: true,
      errors: [],
      warnings: []
    }

    const requiredFields = ['date', 'product', 'sales', 'quantity']
    
    // 检查必需字段
    requiredFields.forEach(field => {
      if (!mapping[field]) {
        result.valid = false
        result.errors.push(`缺少必需字段映射: ${field}`)
      } else if (!csvHeaders.includes(mapping[field])) {
        result.valid = false
        result.errors.push(`CSV文件中不存在字段: ${mapping[field]}`)
      }
    })

    // 检查字段重复
    const mappedFields = Object.values(mapping).filter(v => v)
    const duplicates = mappedFields.filter((item, index) => mappedFields.indexOf(item) !== index)
    if (duplicates.length > 0) {
      result.valid = false
      result.errors.push(`字段映射重复: ${[...new Set(duplicates)].join(', ')}`)
    }

    return result
  }
}

// 创建单例实例
const posDataService = new POSDataService()

export default posDataService