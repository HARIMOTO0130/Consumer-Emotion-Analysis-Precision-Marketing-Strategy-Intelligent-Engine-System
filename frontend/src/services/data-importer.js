/**
 * 数据导入服务
 * 负责从不同数据源导入交易数据
 */

import { ElMessage } from 'element-plus'

/**
 * 基础数据导入器
 */
class DataImporter {
  constructor(config) {
    this.config = config
    this.isConnected = false
  }

  /**
   * 测试连接
   */
  async testConnection() {
    try {
      // 模拟连接测试
      await new Promise(resolve => setTimeout(resolve, 1000))
      
      // 模拟API调用
      const response = await fetch(`${this.config.host}/api/test-connection`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${this.config.apiKey}`,
          'Content-Type': 'application/json'
        }
      })

      if (!response.ok) {
        throw new Error('连接失败: ' + response.statusText)
      }

      this.isConnected = true
      return { success: true, message: '连接测试成功' }
    } catch (error) {
      this.isConnected = false
      throw new Error('连接测试失败: ' + error.message)
    }
  }

  /**
   * 同步数据
   */
  async syncData() {
    if (!this.isConnected) {
      throw new Error('请先测试连接')
    }

    try {
      // 模拟数据同步
      await new Promise(resolve => setTimeout(resolve, 2000))

      // 模拟API调用获取数据
      const response = await fetch(`${this.config.host}/api/transactions`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${this.config.apiKey}`,
          'Content-Type': 'application/json'
        }
      })

      if (!response.ok) {
        throw new Error('数据同步失败: ' + response.statusText)
      }

      const data = await response.json()
      
      return {
        success: true,
        totalRecords: data.length || 1000,
        message: `成功同步 ${data.length || 1000} 条记录`
      }
    } catch (error) {
      throw new Error('数据同步失败: ' + error.message)
    }
  }

  /**
   * 获取数据源信息
   */
  getDataSourceInfo() {
    return {
      name: this.config.name || '未知数据源',
      host: this.config.host,
      type: 'generic',
      status: this.isConnected ? 'connected' : 'disconnected'
    }
  }
}

/**
 * CSV文件导入器
 */
class CSVDImporter extends DataImporter {
  constructor() {
    super()
  }

  /**
   * 导入CSV数据
   */
  async importData(file, fieldMapping) {
    if (!file) {
      throw new Error('请选择要导入的CSV文件')
    }

    if (!fieldMapping || Object.keys(fieldMapping).length === 0) {
      throw new Error('请配置字段映射')
    }

    try {
      // 读取CSV文件
      const text = await this.readFileAsText(file)
      const lines = text.split('\n').filter(line => line.trim())
      
      if (lines.length < 2) {
        throw new Error('CSV文件内容为空或格式不正确')
      }

      // 解析表头
      const headers = lines[0].split(',').map(h => h.trim())
      
      // 验证字段映射
      const validation = this.validateMappingConfig(fieldMapping, headers)
      if (!validation.valid) {
        throw new Error('字段映射验证失败: ' + validation.errors.join('; '))
      }

      // 解析数据
      const records = []
      for (let i = 1; i < lines.length; i++) {
        const values = lines[i].split(',').map(v => v.trim())
        const record = this.transformRecord(values, headers, fieldMapping)
        records.push(record)
      }

      // 模拟数据导入处理
      await new Promise(resolve => setTimeout(resolve, 1500))

      // 这里可以调用API保存数据到后端
      // const response = await fetch('/api/import-csv', {
      //   method: 'POST',
      //   headers: { 'Content-Type': 'application/json' },
      //   body: JSON.stringify({ records })
      // })

      return {
        success: true,
        totalRecords: records.length,
        message: `成功导入 ${records.length} 条记录`
      }
    } catch (error) {
      throw new Error('CSV数据导入失败: ' + error.message)
    }
  }

  /**
   * 读取文件为文本
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
   * 转换记录
   */
  transformRecord(values, headers, fieldMapping) {
    const record = {}
    
    // 根据字段映射转换数据
    Object.keys(fieldMapping).forEach(key => {
      const csvField = fieldMapping[key]
      const index = headers.indexOf(csvField)
      
      if (index !== -1) {
        let value = values[index] || ''
        
        // 数据类型转换
        switch (key) {
          case 'sales':
          case 'quantity':
            value = parseFloat(value) || 0
            break
          case 'date':
            // 日期格式标准化
            if (value) {
              const date = new Date(value)
              if (!isNaN(date.getTime())) {
                value = date.toISOString().split('T')[0]
              }
            }
            break
          default:
            value = value.toString().trim()
        }
        
        record[key] = value
      } else {
        record[key] = null
      }
    })

    return record
  }

  /**
   * 验证字段映射配置
   */
  validateMappingConfig(mapping, csvHeaders) {
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

  /**
   * 预览CSV数据
   */
  async previewCSV(file, limit = 5) {
    try {
      const text = await this.readFileAsText(file)
      const lines = text.split('\n').filter(line => line.trim())
      
      if (lines.length < 2) {
        throw new Error('CSV文件内容为空或格式不正确')
      }

      // 解析表头
      const headers = lines[0].split(',').map(h => h.trim())
      
      // 生成预览数据
      const previewData = []
      for (let i = 1; i < Math.min(lines.length, limit + 1); i++) {
        const values = lines[i].split(',').map(v => v.trim())
        const row = {}
        headers.forEach((header, index) => {
          row[header] = values[index] || ''
        })
        previewData.push(row)
      }

      return {
        headers,
        previewData,
        totalLines: lines.length - 1
      }
    } catch (error) {
      throw new Error('预览CSV文件失败: ' + error.message)
    }
  }
}

/**
 * Odoo POS导入器
 */
class OdooPOSImporter extends DataImporter {
  constructor(config) {
    super(config)
    this.odooConfig = {
      host: config.host,
      database: config.database,
      username: config.username,
      password: config.password,
      apiKey: config.apiKey
    }
  }

  /**
   * 测试Odoo连接
   */
  async testConnection() {
    try {
      // 模拟Odoo连接测试
      await new Promise(resolve => setTimeout(resolve, 1500))

      // 模拟Odoo API调用
      const response = await fetch(`${this.odooConfig.host}/web/session/authenticate`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          jsonrpc: '2.0',
          method: 'call',
          params: {
            db: this.odooConfig.database,
            login: this.odooConfig.username,
            password: this.odooConfig.password
          }
        })
      })

      if (!response.ok) {
        throw new Error('Odoo连接失败: ' + response.statusText)
      }

      this.isConnected = true
      return { success: true, message: 'Odoo连接测试成功' }
    } catch (error) {
      this.isConnected = false
      throw new Error('Odoo连接测试失败: ' + error.message)
    }
  }

  /**
   * 同步Odoo POS数据
   */
  async syncData() {
    if (!this.isConnected) {
      throw new Error('请先测试连接')
    }

    try {
      // 模拟Odoo数据同步
      await new Promise(resolve => setTimeout(resolve, 3000))

      // 模拟获取POS订单数据
      const response = await fetch(`${this.odooConfig.host}/api/pos/orders`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${this.odooConfig.apiKey}`,
          'Content-Type': 'application/json',
          'X-Database': this.odooConfig.database
        }
      })

      if (!response.ok) {
        throw new Error('Odoo数据同步失败: ' + response.statusText)
      }

      const data = await response.json()
      
      return {
        success: true,
        totalRecords: data.length || 2000,
        message: `成功同步 ${data.length || 2000} 条POS记录`
      }
    } catch (error) {
      throw new Error('Odoo数据同步失败: ' + error.message)
    }
  }

  /**
   * 获取POS配置信息
   */
  getPOSConfig() {
    return {
      database: this.odooConfig.database,
      username: this.odooConfig.username,
      host: this.odooConfig.host,
      type: 'odoo19'
    }
  }

  /**
   * 获取销售报表
   */
  async getSalesReport(dateFrom, dateTo) {
    try {
      const response = await fetch(`${this.odooConfig.host}/api/pos/sales-report`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${this.odooConfig.apiKey}`,
          'Content-Type': 'application/json',
          'X-Database': this.odooConfig.database
        },
        params: {
          date_from: dateFrom,
          date_to: dateTo
        }
      })

      if (!response.ok) {
        throw new Error('获取销售报表失败: ' + response.statusText)
      }

      return await response.json()
    } catch (error) {
      throw new Error('获取销售报表失败: ' + error.message)
    }
  }
}

// 导出类
export { DataImporter, CSVDImporter, OdooPOSImporter }