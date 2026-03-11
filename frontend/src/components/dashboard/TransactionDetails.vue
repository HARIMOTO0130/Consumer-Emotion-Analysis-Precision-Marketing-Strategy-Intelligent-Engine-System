<template>
  <el-card class="data-card" shadow="hover" @click="openTransactionDetailsDialog">
    <template #header>
      <div class="card-header">
        <div class="header-title">
          <mdicon name="table" size="28"/>
          <h3>总订单数</h3>
          <span class="transaction-count">{{ transactionStats.totalOrders }}</span>
        </div>
        <div class="data-source-tag">
          <span class="source-label">数据来源:</span>
          <el-tag size="small" type="info">{{ transactionStats.dataSource }}</el-tag>
        </div>
      </div>
    </template>
    <div class="transaction-content">
      <div class="transaction-item">
        <span class="item-label">已完成</span>
        <span class="item-value positive">{{ transactionStats.completedOrders }}</span>
      </div>
      <div class="transaction-item">
        <span class="item-label">进行中</span>
        <span class="item-value warning">{{ transactionStats.pendingOrders }}</span>
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

const emit = defineEmits(['open-transaction-details'])

const openTransactionDetailsDialog = () => {
  emit('open-transaction-details')
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

.data-source-tag {
  display: flex;
  align-items: center;
  gap: 8px;
}

.source-label {
  font-size: 14px;
  color: #666;
  font-weight: 500;
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

.item-value.positive {
  color: #52c41a;
}

.item-value.warning {
  color: #faad14;
}
</style>