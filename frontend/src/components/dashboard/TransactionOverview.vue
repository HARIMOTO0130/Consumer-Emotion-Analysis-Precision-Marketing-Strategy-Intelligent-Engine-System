<template>
  <el-card class="data-card" shadow="hover" @click="openTransactionOverviewDialog">
    <template #header>
      <div class="card-header">
        <div class="header-title">
          <mdicon name="currency-usd" size="28"/>
          <h3>今日总流水</h3>
          <span class="transaction-count">{{ transactionStats.totalSales }}</span>
        </div>
        <div class="data-source-breakdown">
          <span class="source-label">数据来源:</span>
          <div class="source-items">
            <el-tag 
              v-for="source in transactionStats.dataSources" 
              :key="source.name"
              :type="getSourceType(source.name)"
              size="small"
              :style="{ backgroundColor: source.color + '20', color: source.color, borderColor: source.color }"
            >
              <span class="source-icon">{{ source.icon }}</span>
              {{ source.name }} {{ source.percentage }}%
            </el-tag>
          </div>
        </div>
      </div>
    </template>
    <div class="transaction-content">
      <div class="transaction-item">
        <span class="item-label">订单数</span>
        <span class="item-value">{{ transactionStats.orderCount }}</span>
      </div>
      <div class="transaction-item">
        <span class="item-label">客单价</span>
        <span class="item-value">{{ transactionStats.avgOrderValue }}</span>
      </div>
    </div>
  </el-card>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue'
import { ElCard, ElTag } from 'element-plus'
import mdicon from 'vue-material-design-icons'

const props = defineProps({
  transactionStats: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['open-transaction-overview'])

const openTransactionOverviewDialog = () => {
  emit('open-transaction-overview')
}

const getSourceType = (sourceName) => {
  const map = {
    'Odoo19': 'info',
    'CSV文件': 'success',
    '其他POS系统': 'warning'
  }
  return map[sourceName] || 'info'
}
</script>

<style scoped>
.data-card {
  border-radius: 12px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s ease;
}

.data-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
}

.card-header {
  padding: 16px 20px;
}

.header-title {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 8px;
}

.header-title .card-icon {
  font-size: 20px;
  margin: 0;
}

.header-title h3 {
  font-size: 18px;
  font-weight: bold;
  margin: 0;
  color: #333;
}

.header-title .transaction-count {
  background: var(--color-success);
  color: white;
  font-size: 12px;
  padding: 3px 8px;
  border-radius: 10px;
  margin-left: 10px;
  font-weight: bold;
}

.data-source-breakdown {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
}

.source-label {
  font-size: 14px;
  color: #666;
  font-weight: 500;
}

.source-items {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.source-icon {
  font-size: 16px;
  margin-right: 4px;
}

.transaction-content {
  padding: 0 20px 20px;
}

.transaction-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px;
  background: #f9f9f9;
  border-radius: 8px;
  margin-bottom: 8px;
  transition: all 0.3s ease;
}

.transaction-item:hover {
  background: #f0f0f0;
  transform: translateX(5px);
}

.item-label {
  font-size: 14px;
  color: #666;
  font-weight: 500;
}

.item-value {
  font-size: 16px;
  font-weight: bold;
  color: #333;
}
</style>