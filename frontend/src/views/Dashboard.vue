<template>
  <div class="dashboard">
    <div class="dashboard-container">
      <div class="dashboard-title-section">
        <div class="title-content">
          <div style="display: flex;gap: 8px">
            <mdicon name="dashboard" size="35" />
            <div>
              <h2>情感分析仪表盘总览</h2>
              <p class="dashboard-subtitle">实时监控消费者情感变化与营销策略效果</p>
            </div>
          </div>
          
        </div>
        <div class="dashboard-controls">
          <div class="time-control">
            <span class="control-label" id="time-range-label">
              <mdicon name="calendar-month" size="20" />
              时间范围
            </span>
            <el-select 
              v-model="timeRange"
              class="time-select"
              placeholder="选择时间范围"
              @change="handleTimeChange"
              :disabled="loading"
              aria-labelledby="time-range-label"
              aria-describedby="time-range-description"
              tabindex="0"
            >
              <el-option label="最近1小时" value="1h" :aria-label="'时间范围：最近1小时'" />
              <el-option label="最近24小时" value="24h" :aria-label="'时间范围：最近24小时'" />
              <el-option label="最近7天" value="7d" :aria-label="'时间范围：最近7天'" />
              <el-option label="最近30天" value="30d" :aria-label="'时间范围：最近30天'" />
            </el-select>
            <span id="time-range-description" class="sr-only">选择数据统计的时间范围</span>
          </div>
          <button 
            class="btn-refresh" 
            @click="refreshData" 
            :disabled="loading"
            :aria-label="loading ? '数据加载中' : '刷新数据'"
            :aria-busy="loading"
            tabindex="0"
            role="button"
          >
            <mdicon name="refresh" size="20" color="#fff" />
            <span>{{ loading ? '加载中...' : '刷新数据' }}</span>
          </button>
        </div>
      </div>

      <!-- 错误提示 -->
      <el-alert
        v-if="error"
        :title="errorMessage"
        type="error"
        show-icon
        closable
        center
        @close="error = null; errorMessage = ''"
        class="error-alert"
      >
        <template #default>
          <div class="error-details">
            <p>建议：检查后端服务是否运行，网络连接是否正常</p>
            <el-button type="primary" size="small" @click="refreshData">重试</el-button>
          </div>
        </template>
      </el-alert>

      <!-- 加载遮罩 -->
      <div v-if="loading" v-loading="loading" class="loading-overlay">
      </div>

      <!-- 实时概览卡片 -->
      <div class="overview-grid">
        <div class="overview-card card-total" @click="openEmotionOverviewDialog">
          <div class="card-icon"><mdicon name="chat-outline-rounded" size="50" color="var(--color-primary)"/></div>
          <div class="card-content">
            <div class="card-value">{{ stats.totalReviews }}</div>
            <div class="card-label">今日新增评论</div>
            <div class="card-status">
              <span class="status-tag positive">正面 {{ stats.positiveCount }}</span>
              <span class="status-tag negative">负面 {{ stats.negativeCount }}</span>
            </div>
          </div>
        </div>
        
        <div class="overview-card card-success" @click="openTrendAnalysisDialog">
          <div class="card-icon"><mdicon name="show-chart" size="50" color="var(--color-success)"/></div>
          <div class="card-content">
            <div class="card-value">{{ stats.positiveRate }}%</div>
            <div class="card-label">整体正面率</div>
            <div class="card-trend positive status-tag">
              <span class="trend-icon"> 较昨日 +{{ stats.trendChange }}%</span>
            </div>
          </div>
        </div>
        
        <div class="overview-card card-warning" @click="openAlertMonitoringDialog">
          <div class="card-icon"><mdicon name="warning-outline-rounded" size="50" color="var(--color-warning)"/></div>
          <div class="card-content">
            <div class="card-value">{{ stats.alertCount }}</div>
            <div class="card-label">舆情预警数量</div>
            <div class="card-trend status-tag negative">
              <span class="trend-icon">需立即关注</span>
            </div>
          </div>
        </div>
        
        <div class="overview-card card-environment" @click="openTopicHotnessDialog">
          <div class="card-icon"><mdicon name="local-fire-department-outline-rounded" size="50" color="var(--color-danger)"/></div>
          <div class="card-content">
            <div class="card-value">{{ stats.hotTopicCount }}</div>
            <div class="card-label">热点话题数量</div>
            <div class="topic-info">
              <span class="topic-item">最热: {{ stats.topTopic }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 主要数据展示区域 -->
      <div class="main-data-section">
        <!-- 左侧：情感分布、实时流和流水数据 -->
        <div class="left-panel">
          <!-- 情感分布 -->
          <el-card class="data-card" shadow="hover" @click="openEmotionDistributionDialog">
            <template #header>
              <div class="card-header">
                <div class="header-title">
                  <mdicon name="insert-chart-outline" size="28"/>
                  <h3>情感分布分析</h3>
                </div>
                <div class="header-subtitle">按渠道、人群、产品线的情感分布对比</div>
              </div>
            </template>
            <div class="emotion-distribution">
              <div 
                v-for="(item, index) in emotionDistribution" 
                :key="item.channel" 
                class="dist-item"
              >
                <div class="dist-info">
                  <div class="dist-range">
                    <span>{{ getChannelName(item.channel) }}</span>
                  </div>
                  <div class="dist-count">{{ item.positive }}/{{ item.negative }}</div>
                  <div class="dist-percentage">正面: {{ item.positivePercent }}%</div>
                </div>
                <div class="dist-bar-container">
                  <div class="dist-bar">
                    <div 
                      class="bar-fill" 
                      :style="{ width: item.positivePercent + '%', background: getEmotionColor(index) }"
                    ></div>
                  </div>
                </div>
              </div>
            </div>
          </el-card>

          <!-- 实时监测流 -->
          <el-card class="data-card" shadow="hover" @click="openRealTimeStreamDialog">
            <template #header>
              <div class="card-header">
                <div class="header-title">
                  <mdicon name="area-chart" size="28" />
                  <h3>实时情感监测流</h3>
                </div>
                <div class="stream-controls">
                  <el-button 
                    size="small" 
                    @click.stop="toggleStream"
                    :aria-label="streamPaused ? '播放实时情感监测流' : '暂停实时情感监测流'"
                    tabindex="0"
                  >
                    {{ streamPaused ? '播放' : '暂停' }}
                  </el-button>
                </div>
              </div>
            </template>
            <div class="stream-container">
              <div class="stream-item" v-for="item in recentComments" :key="item.id">
                <div class="stream-emotion" :class="item.emotion">
                  <span v-if="item.emotion === 'positive'">😊</span>
                  <span v-if="item.emotion === 'neutral'">😐</span>
                  <span v-if="item.emotion === 'negative'">😞</span>
                </div>
                <div class="stream-content">
                  <div class="stream-text">{{ item.text }}</div>
                  <div class="stream-meta">
                    <span class="stream-source">{{ getChannelName(item.source) }}</span>
                    <span class="stream-time">{{ formatDate(item.time,"yyyy-mm") }}</span>
                  </div>
                </div>
              </div>
            </div>
          </el-card>

          <!-- 总体信息磁贴 -->
          <el-card class="data-card" shadow="hover" @click="openTransactionOverviewDialog">
            <template #header>
              <div class="card-header">
                <div class="header-title">
                  <mdicon name="attach-money" size="28"/>
                  <h3>今日总流水</h3>
                  <span class="transaction-count">{{ transactionStats.totalSales }}</span>
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
          
          <!-- 详细信息磁贴 -->
          <el-card class="data-card" shadow="hover" @click="openTransactionDetailsDialog">
            <template #header>
              <div class="card-header">
                <div class="header-title">
                  <mdicon name="table" size="28"/>
                  <h3>总订单数</h3>
                  <span class="transaction-count">{{ transactionStats.totalOrders }}</span>
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
        </div>

        <!-- 右侧：图表和营销效果 -->
        <div class="right-panel">
          <!-- 情感趋势分析 -->
          <el-card class="data-card" shadow="hover" @click="openTrendAnalysisDialog">
            <template #header>
              <div class="card-header">
                <div class="header-title">
                  <mdicon name="grouped-bar-chart" size="28"/>
                  <h3>情感趋势分析</h3>
                </div>
                <div class="chart-tabs">
                  <button 
                    v-for="tab in chartTabs" 
                    :key="tab.id"
                    :class="['chart-tab', { active: activeChart === tab.id }]"
                    @click.stop="activeChart = tab.id"
                    :aria-label="`切换到${tab.label}图表`"
                    :aria-selected="activeChart === tab.id"
                    role="tab"
                    tabindex="0"
                    @keydown.enter="activeChart = tab.id"
                    @keydown.space.prevent="activeChart = tab.id"
                  >
                    {{ tab.label }}
                  </button>
                </div>
              </div>
            </template>
            <div class="chart-container">
              <!-- 情感趋势图表 -->
              <div v-if="activeChart === 'emotion'" class="chart-content">
                <div class="chart-header">
                  <h4>近24小时情感趋势变化</h4>
                </div>
                <v-chart class="chart" :option="emotionTrendOption" autoresize />
              </div>
              
              <!-- 营销效果图表 -->
              <div v-if="activeChart === 'marketing'" class="chart-content">
                <div class="chart-header">
                  <h4>近期营销活动效果分析</h4>
                </div>
                <v-chart class="chart" :option="marketingEffectOption" autoresize />
              </div>
              
              <!-- 情感分类图表 -->
              <div v-if="activeChart === 'classification'" class="chart-content">
                <div class="chart-header">
                  <h4>情感分类分布</h4>
                </div>
                <v-chart class="chart" :option="emotionClassificationOption" autoresize />
              </div>
            </div>
          </el-card>

            <!-- 营销效果和智能洞察 -->
          <div class="bottom-section">
            <!-- 营销效果速览 -->
            <el-card class="data-card" shadow="hover" @click="openMarketingEffectDialog">
              <template #header>
                <div class="card-header">
                  <div class="header-title">
                    <mdicon name="rocket-launch-outline" size="28"/>
                    <h3>营销效果速览</h3>
                    <span class="marketing-count">{{ marketingActivities.length }}</span>
                  </div>
                </div>
              </template>
              <div class="marketing-list">
                <div 
                  v-for="activity in marketingActivities" 
                  :key="activity.id" 
                  :class="['marketing-item', `priority-${activity.priority}`]"
                >
                  <div class="marketing-content">
                    <div class="marketing-header">
                      <span class="activity-name">{{ activity.name }}</span>
                      <span class="effect-badge" :class="`badge-${activity.effect}`">
                        效果: {{ getEffectName(activity.effect) }}
                      </span>
                    </div>
                    <div class="marketing-details">
                      <div class="detail-item">
                        <span class="detail-label">参与度:</span>
                        <span class="detail-value">{{ activity.engagement }}%</span>
                      </div>
                      <div class="detail-item">
                        <span class="detail-label">转化率:</span>
                        <span class="detail-value">{{ activity.conversion }}%</span>
                      </div>
                    </div>
                    <div class="marketing-time">{{ formatDate(activity.date,"yyyy-mm-dd") }}</div>
                  </div>
                </div>
              </div>
            </el-card>

            <!-- 智能洞察摘要 -->
            <el-card class="insight-card" shadow="hover" @click="openInsightSummaryDialog">
              <template #header>
                <div class="card-header">
                  <div class="header-title">
                    <mdicon name="mindfulness-outline-rounded" size="28"/>
                    <h3>智能洞察摘要</h3>
                  </div>
                </div>
              </template>
              <div class="insight-content">
                <div class="insight-item" v-for="insight in insights" :key="insight.id">
                  <div class="insight-header">
                    <span class="insight-type">{{ getActionTypeName(insight.type) }}</span>
                    <span class="insight-date">{{ formatDate(insight.date,"yyyy-mm-dd") }}</span>
                  </div>
                  <div class="insight-text">{{ insight.text }}</div>
                  <div class="insight-action">
                    <el-button 
                      size="small" 
                      type="primary" 
                      @click.stop="takeAction(insight.action)"
                      :aria-label="`执行${insight.actionText}操作`"
                      tabindex="0"
                    >
                      {{ insight.actionText }}
                    </el-button>
                  </div>
                </div>
              </div>
            </el-card>
          </div>
        </div>
      </div>

      <!-- ========== 流水数据可视化弹窗 ========== -->
      <!-- 总体信息弹窗（含筛选） -->
      <el-dialog v-model="transactionOverviewDialogVisible" title="流水数据总体信息" width="80%" :before-close="closeDialog">
        <div class="dialog-content">
          <!-- 筛选区域 -->
          <el-form :inline="true" :model="overviewFilters" class="filter-form">
            <el-form-item label="日期范围">
              <el-date-picker
                v-model="overviewFilters.dateRange"
                type="daterange"
                range-separator="至"
                start-placeholder="开始日期"
                end-placeholder="结束日期"
                format="YYYY-MM-DD"
                value-format="YYYY-MM-DD"
              />
            </el-form-item>
            <el-form-item label="门店">
              <el-select v-model="overviewFilters.stores" multiple placeholder="全部门店" clearable>
                <el-option v-for="store in storeOptions" :key="store" :label="store" :value="store" />
              </el-select>
            </el-form-item>
            <el-form-item label="支付方式">
              <el-select v-model="overviewFilters.paymentMethods" multiple placeholder="全部方式" clearable>
                <el-option v-for="method in paymentMethodOptions" :key="method" :label="method" :value="method" />
              </el-select>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="applyOverviewFilters">查询</el-button>
              <el-button @click="resetOverviewFilters">重置</el-button>
            </el-form-item>
          </el-form>

          <h3>流水数据总体分析</h3>
          <p>今日总流水：{{ filteredStats.totalSales }}，订单数：{{ filteredStats.orderCount }}，客单价：{{ filteredStats.avgOrderValue }}</p>
          <p>数据来源：湘菜品牌销售系统</p>
          <div class="chart-placeholder">
            <p>流水趋势图</p>
            <div class="chart-wrapper" style="height: 400px;">
              <v-chart :option="filteredTrendOption" autoresize />
            </div>
          </div>
          <div class="chart-placeholder">
            <p>产品销售分布</p>
            <div class="chart-wrapper" style="height: 400px;">
              <v-chart :option="filteredProductOption" autoresize />
            </div>
          </div>
        </div>
      </el-dialog>

      <!-- 详细信息弹窗（含筛选+分页） -->
      <el-dialog v-model="transactionDetailsDialogVisible" title="流水数据详细信息" width="90%" :before-close="closeDialog">
        <div class="dialog-content">
          <!-- 筛选区域（可独立于总体） -->
          <el-form :inline="true" :model="detailFilters" class="filter-form">
            <el-form-item label="日期范围">
              <el-date-picker
                v-model="detailFilters.dateRange"
                type="daterange"
                range-separator="至"
                start-placeholder="开始日期"
                end-placeholder="结束日期"
                format="YYYY-MM-DD"
                value-format="YYYY-MM-DD"
              />
            </el-form-item>
            <el-form-item label="门店">
              <el-select v-model="detailFilters.stores" multiple placeholder="全部门店" clearable>
                <el-option v-for="store in storeOptions" :key="store" :label="store" :value="store" />
              </el-select>
            </el-form-item>
            <el-form-item label="支付方式">
              <el-select v-model="detailFilters.paymentMethods" multiple placeholder="全部方式" clearable>
                <el-option v-for="method in paymentMethodOptions" :key="method" :label="method" :value="method" />
              </el-select>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="applyDetailFilters">查询</el-button>
              <el-button @click="resetDetailFilters">重置</el-button>
            </el-form-item>
          </el-form>

          <h3>流水数据详细分析</h3>
          <p>总订单数：{{ filteredDetailStats.totalOrders }}，已完成：{{ filteredDetailStats.completedOrders }}，进行中：{{ filteredDetailStats.pendingOrders }}</p>
          <div class="transaction-table">
            <el-table :data="paginatedDetails" style="width: 100%" border>
              <el-table-column prop="transaction_id" label="交易ID" />
              <el-table-column prop="date" label="日期" />
              <el-table-column prop="time" label="时间" />
              <el-table-column prop="product_name" label="产品名称" />
              <el-table-column prop="category" label="类别"/>
              <el-table-column prop="quantity" label="数量" />
              <el-table-column prop="unit_price" label="单价" />
              <el-table-column prop="total_amount" label="总金额" />
              <el-table-column prop="payment_method" label="支付方式" />
              <el-table-column prop="customer_type" label="客户类型" />
              <el-table-column prop="store_location" label="门店位置" />
            </el-table>
            
            <el-pagination
              v-model:current-page="currentPage"
              v-model:page-size="pageSize"
              :page-sizes="[10, 20, 50, 100]"
              layout="total, sizes, prev, pager, next, jumper"
              :total="filteredDetails.length"
              @size-change="handleSizeChange"
              @current-change="handleCurrentChange"
              style="margin-top: 20px;"
            />
          </div>
        </div>
      </el-dialog>

      <!-- 其他原有弹窗（保持不变） -->
      <el-dialog v-model="emotionOverviewDialogVisible" title="情感态势总览详情" width="80%" :before-close="closeDialog">
        <div class="dialog-content">
          <h3>情感态势总览详细分析</h3>
          <p>本通过多维度数据分析，实时监控消费者对品牌、产品和服务的情感变化趋势。当前总体情感指数为{{ stats.positiveRate }}%，较昨日提升{{ stats.trendChange }}%。</p>
          <p>主要发现：</p>
          <ul>
            <li>正面情感主要集中在产品质量和客户服务方面</li>
            <li>负面情感主要源于价格敏感性和物流配送问题</li>
            <li>关键话题包括新品发布、价格调整、售后服务等</li>
          </ul>
          <div class="chart-placeholder">
            <p>情感变化趋势图</p>
            <div class="chart-wrapper" style="height: 400px;">
             <v-chart :option="overviewTrendOption" autoresize />
            </div>
          </div>
        </div>
      </el-dialog>
      
      <el-dialog v-model="realTimeStreamDialogVisible" title="实时情感监测流详情" width="80%" :before-close="closeDialog">
        <div class="dialog-content">
          <h3>实时情感监测流详细数据</h3>
          <p>以下是最新的消费者评论和社交媒体提及，按时间倒序排列。每条评论都经过情感分析算法处理，标注了情感倾向和强度。</p>
          <div class="comment-table">
            <el-table :data="detailedComments" style="width: 100%">
              <el-table-column prop="text" label="评论内容"   />
              <el-table-column prop="source" label="来源"  >
                <template #default="{ row }">
                    {{getChannelName(row.source)}}
                </template>
              </el-table-column>
              <el-table-column prop="sentiment" label="情感倾向"  >
                <template #default="{ row }">
                  <el-tag :type="row.sentiment === 'positive' ? 'success' : row.sentiment === 'negative' ? 'danger' : 'info'">
                    {{ getEmotionName(row.sentiment) }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column prop="intensity" label="情感强度"  >
                <template #default="{ row }">
                    {{getIntensityName(row.intensity)}}
                </template>
              </el-table-column>
              <el-table-column prop="timestamp" label="时间"   >
                <template #default="{row}">
                  {{formatDate(row.timestamp, "yyyy-mm-dd hh:mm:ss")}}
                </template>
              </el-table-column>
            </el-table>
          </div>
        </div>
      </el-dialog>
      
      <el-dialog v-model="emotionDistributionDialogVisible" title="多维度情感分布详情" width="80%" :before-close="closeDialog">
        <div class="dialog-content">
          <h3>多维度情感分布详细分析</h3>
          <p>按照不同维度分析消费者情感分布情况：</p>
          <el-tabs>
            <el-tab-pane label="按渠道分布">
              <div class="chart-placeholder">
                <p>渠道情感分布对比图</p>
                <div class="chart-wrapper" style="height: 400px;">
            <v-chart :option="channelDistOption" autoresize />
          </div>
              </div>
            </el-tab-pane>
            <el-tab-pane label="按人群分布">
              <div class="chart-placeholder">
                <p>人群情感分布对比图</p>
                <div class="chart-wrapper" style="height: 400px;">
            <v-chart :option="userGroupDistOption" autoresize />
          </div>
              </div>
            </el-tab-pane>
            <el-tab-pane label="按产品线分布">
              <div class="chart-placeholder">
                <p>产品线情感分布对比图</p>
                <v-chart :option="productLineDistOption" autoresize />
              </div>
            </el-tab-pane>
          </el-tabs>
        </div>
      </el-dialog>
      
    <el-dialog v-model="marketingEffectDialogVisible" title="营销效果详情" width="80%" :before-close="closeDialog">
      <div class="dialog-content">
        <h3>营销活动效果详细分析</h3>
        <p>近期开展的营销活动效果评估及情感影响分析：</p>
        <div class="activity-detail" v-for="activity in marketingActivities" :key="activity.id" style="margin-bottom: 30px; padding-bottom: 20px; border-bottom: 1px solid #eee;">
          <h4>{{ activity.name }}</h4>
          <div class="activity-info-grid" style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin-bottom: 15px;">
            <p><strong>活动时间：</strong>{{ formatDate(activity.date, "yyyy-mm-dd") }}</p>
            <p><strong>参与人数：</strong>{{ activity.participants }}</p>
            <p><strong>情感影响度：</strong>{{ getEffectName(activity.effect) }}</p>
            <p><strong>参与度：</strong>{{ activity.engagement }}%</p>
            <p><strong>转化率：</strong>{{ activity.conversion }}%</p>
          </div>
          
          <div class="activity-chart-container" style="height: 250px; width: 100%; background: #fafafa; padding: 10px; border-radius: 8px;">
            <v-chart :option="getActivityTrendOption(activity)" autoresize /> </div>
        </div>
      </div>
    </el-dialog>
      
      <el-dialog v-model="insightSummaryDialogVisible" title="智能洞察摘要详情" width="80%" :before-close="closeDialog">
        <div class="dialog-content">
          <h3>AI自动生成的消费者情感洞察</h3>
          <p>基于大数据和AI算法，自动生成的消费者情感洞察和行动建议：</p>
          <div class="insight-detail" v-for="insight in detailedInsights" :key="insight.id" style="margin-bottom: 20px; padding: 15px; background: #f9f9f9; border-radius: 4px;">
            <h4>{{ insight.title }}</h4>
            <p>{{ insight.description }}</p>
            <p><strong>建议行动：</strong>{{ insight.recommendation }}</p>
            <p><strong>紧急程度：</strong>{{ getPriorityName(insight.priority) }}</p>
            <p><strong>预期效果：</strong>{{ insight.expectedOutcome }}</p>
          </div>
        </div>
      </el-dialog>
      
      <el-dialog v-model="trendAnalysisDialogVisible" title="情感趋势分析详情" width="80%" :before-close="closeDialog">
        <div class="dialog-content">
          <h3>情感趋势详细分析</h3>
          <p>长期和短期情感趋势分析，识别情感变化的关键节点和影响因素：</p>
          <div class="chart-placeholder">
            <p>长期情感趋势图（30天）</p>
            <div class="chart-wrapper" style="height: 450px;">
        <v-chart :option="longTermTrendOption" autoresize />
      </div>
          </div>
          <div class="trend-insights">
            <h4>趋势洞察</h4>
            <ul>
              <li v-for="insight in trendInsights" :key="insight.id">{{ insight.text }}</li>
            </ul>
          </div>
        </div>
      </el-dialog>
      
      <el-dialog v-model="alertMonitoringDialogVisible" title="舆情预警详情" width="80%" :before-close="closeDialog">
        <div class="dialog-content">
          <h3>舆情预警详细信息</h3>
          <p>当前需要重点关注的舆情预警和潜在风险：</p>
          <el-table :data="alerts">
            <el-table-column prop="id" label="ID"   />
            <el-table-column prop="title" label="预警标题"   />
            <el-table-column prop="type" label="类型"  >
              <template #default="{ row }">
                <el-tag :type="row.type === 'risk' ? 'danger' : 'warning'">{{ getActionTypeName(row.type) }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="severity" label="严重程度"  >
              <template #default="{ row }">
                <el-tag :type="row.severity === 'high' ? 'danger' : row.severity === 'medium' ? 'warning' : 'info'">{{ getPriorityName(row.severity) }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="date" label="发生时间"   />
            <el-table-column prop="status" label="状态"  >
              <template #default="{ row }">
                <el-tag :type="row.status === 'pending' ? 'warning' : 'success'">{{ getAlertStatusName(row.status) }}</el-tag>
              </template>
            </el-table-column>
          </el-table>
        </div>
      </el-dialog>
      
      <el-dialog v-model="topicHotnessDialogVisible" title="热点话题详情" width="80%" :before-close="closeDialog">
        <div class="dialog-content">
          <h3>热点话题详细分析</h3>
          <p>当前最受关注的话题及其情感倾向分析：</p>
          <el-table :data="topics" style="width: 100%">
            <el-table-column prop="rank" label="排名"   />
            <el-table-column prop="name" label="话题名称" />
            <el-table-column prop="mentions" label="提及次数"   />
            <el-table-column prop="sentiment" label="情感倾向"  >
              <template #default="{ row }">
                <el-tag :type="row.sentiment === 'positive' ? 'success' : row.sentiment === 'negative' ? 'danger' : 'info'">{{ getEmotionName(row.sentiment) }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="trend" label="趋势"  >
              <template #default="{ row }">
                <span v-if="row.trend === 'rising'" style="color: green;">上升</span>
                <span v-if="row.trend === 'falling'" style="color: red;">下降</span>
                <span v-if="row.trend === 'stable'" style="color: orange;">平稳</span>
              </template>
            </el-table-column>
          </el-table>
        </div>
      </el-dialog>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { 
  ElCard, ElSelect, ElSwitch, ElDialog, ElTable, ElTableColumn, 
  ElTag, ElButton, ElTabs, ElTabPane, ElMessage, ElAlert,
  ElDatePicker, ElPagination, ElForm, ElFormItem, ElStatistic, ElRow, ElCol
} from 'element-plus'
import VChart from 'vue-echarts'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { LineChart, BarChart, PieChart } from 'echarts/charts'
import {
  GridComponent,
  TooltipComponent,
  LegendComponent,
  TitleComponent
} from 'echarts/components'
import axios from 'axios'
import {
  getChannelName,
  getEmotionName,
  getEffectName,
  getActionTypeName,
  getPriorityName,
  getIntensityName,
  getInsightTypeName,
  getAlertStatusName
} from '../utils/enum-mapping'
import {
  formatDate
} from "../utils/time-format"
import POSDataVisualization from '../components/pos-data-visualization.vue'

// 注册ECharts组件
use([
  CanvasRenderer,
  LineChart,
  BarChart,
  PieChart,
  GridComponent,
  TooltipComponent,
  LegendComponent,
  TitleComponent
])

const router = useRouter()

// 注册组件
const components = {
  VChart,
  POSDataVisualization
}

// 响应式数据
const timeRange = ref('24h')
const showHighPriority = ref(false)
const activeChart = ref('emotion')

// 弹窗可见性
const emotionOverviewDialogVisible = ref(false)
const realTimeStreamDialogVisible = ref(false)
const emotionDistributionDialogVisible = ref(false)
const marketingEffectDialogVisible = ref(false)
const insightSummaryDialogVisible = ref(false)
const trendAnalysisDialogVisible = ref(false)
const alertMonitoringDialogVisible = ref(false)
const topicHotnessDialogVisible = ref(false)
const transactionOverviewDialogVisible = ref(false)
const transactionDetailsDialogVisible = ref(false)

// 控制实时流
const streamPaused = ref(false)

// 加载状态
const loading = ref(false)
const loadingText = ref('正在加载数据...')

// 错误状态
const error = ref(null)
const errorMessage = ref('')

// ========== 新增：200条流水Mock数据 ==========
const generateMockTransactions = (count = 200) => {
  const stores = ['市中心店', '五一广场店', '岳麓山店', '高铁南站店'];
  const paymentMethods = ['微信支付', '支付宝', '现金', '银行卡', '会员卡'];
  const customerTypes = ['会员', '散客'];
  const products = [
    { name: '剁椒鱼头', category: '主菜', price: 98 },
    { name: '辣椒炒肉', category: '主菜', price: 48 },
    { name: '毛氏红烧肉', category: '主菜', price: 68 },
    { name: '小炒黄牛肉', category: '主菜', price: 58 },
    { name: '永州血鸭', category: '主菜', price: 55 },
    { name: '口味虾', category: '特色菜', price: 88 },
    { name: '口味蛇', category: '特色菜', price: 128 },
    { name: '湘西土匪鸡', category: '特色菜', price: 78 },
    { name: '干锅肥肠', category: '特色菜', price: 62 },
    { name: '臭豆腐', category: '小吃', price: 12 },
    { name: '糖油粑粑', category: '甜品', price: 8 },
    { name: '刮凉粉', category: '小吃', price: 10 },
    { name: '葱油饼', category: '小吃', price: 6 },
    { name: '酒酿圆子', category: '甜品', price: 15 },
    { name: '银耳莲子羹', category: '甜品', price: 12 },
    { name: '湖藕汤', category: '汤类', price: 28 },
    { name: '酸辣汤', category: '汤类', price: 18 },
    { name: '三鲜汤', category: '汤类', price: 22 }
  ];

  const data = [];
  // 使用最近30天的数据，确保包含今天
  const today = new Date();
  const startDate = new Date(today);
  startDate.setDate(today.getDate() - 29); // 最近30天
  const endDate = today;

  // 确保今天有一些数据
  const todayStr = today.toISOString().split('T')[0];
  const todayTransactionsCount = Math.floor(count * 0.3); // 今天占30%
  
  // 生成今天的交易数据
  for (let i = 0; i < todayTransactionsCount; i++) {
    const hour = Math.floor(Math.random() * 14) + 8; // 8:00 - 22:00
    const minute = Math.floor(Math.random() * 60);
    const timeStr = `${hour.toString().padStart(2, '0')}:${minute.toString().padStart(2, '0')}`;

    const product = products[Math.floor(Math.random() * products.length)];
    const quantity = Math.floor(Math.random() * 3) + 1;
    const total = product.price * quantity;

    data.push({
      transaction_id: `TX${todayStr.replace(/-/g, '')}${String(i).padStart(4, '0')}`,
      date: todayStr,
      time: timeStr,
      product_name: product.name,
      category: product.category,
      quantity: quantity,
      unit_price: product.price,
      total_amount: total,
      payment_method: paymentMethods[Math.floor(Math.random() * paymentMethods.length)],
      customer_type: customerTypes[Math.floor(Math.random() * customerTypes.length)],
      store_location: stores[Math.floor(Math.random() * stores.length)]
    });
  }

  // 生成其他日期的交易数据
  const otherTransactionsCount = count - todayTransactionsCount;
  for (let i = 0; i < otherTransactionsCount; i++) {
    const date = new Date(startDate.getTime() + Math.random() * (endDate - startDate));
    const dateStr = date.toISOString().split('T')[0];
    const hour = Math.floor(Math.random() * 14) + 8; // 8:00 - 22:00
    const minute = Math.floor(Math.random() * 60);
    const timeStr = `${hour.toString().padStart(2, '0')}:${minute.toString().padStart(2, '0')}`;

    const product = products[Math.floor(Math.random() * products.length)];
    const quantity = Math.floor(Math.random() * 3) + 1;
    const total = product.price * quantity;

    data.push({
      transaction_id: `TX${dateStr.replace(/-/g, '')}${String(i + 1000).padStart(4, '0')}`,
      date: dateStr,
      time: timeStr,
      product_name: product.name,
      category: product.category,
      quantity: quantity,
      unit_price: product.price,
      total_amount: total,
      payment_method: paymentMethods[Math.floor(Math.random() * paymentMethods.length)],
      customer_type: customerTypes[Math.floor(Math.random() * customerTypes.length)],
      store_location: stores[Math.floor(Math.random() * stores.length)]
    });
  }
  
  // 按日期和时间排序
  data.sort((a, b) => a.date.localeCompare(b.date) || a.time.localeCompare(b.time));
  return data;
};

const allTransactions = ref(generateMockTransactions(200));

// ========== 总体信息弹窗筛选 ==========
const overviewFilters = ref({
  dateRange: [],
  stores: [],
  paymentMethods: []
});

// 门店、支付方式选项（从数据中动态提取）
const storeOptions = computed(() => [...new Set(allTransactions.value.map(t => t.store_location))]);
const paymentMethodOptions = computed(() => [...new Set(allTransactions.value.map(t => t.payment_method))]);

// 过滤后的数据（用于总体弹窗）
const filteredOverviewTransactions = computed(() => {
  return allTransactions.value.filter(t => {
    // 日期范围
    if (overviewFilters.value.dateRange && overviewFilters.value.dateRange.length === 2) {
      const date = t.date;
      if (date < overviewFilters.value.dateRange[0] || date > overviewFilters.value.dateRange[1]) return false;
    }
    // 门店
    if (overviewFilters.value.stores.length && !overviewFilters.value.stores.includes(t.store_location)) return false;
    // 支付方式
    if (overviewFilters.value.paymentMethods.length && !overviewFilters.value.paymentMethods.includes(t.payment_method)) return false;
    return true;
  });
});

// 基于过滤后数据计算统计指标（用于总体弹窗）
const filteredStats = computed(() => {
  const trans = filteredOverviewTransactions.value;
  const totalSales = trans.reduce((sum, t) => sum + t.total_amount, 0);
  const orderCount = trans.length;
  const avgOrderValue = orderCount ? (totalSales / orderCount).toFixed(2) : 0;
  return {
    totalSales: '¥' + totalSales.toLocaleString(),
    orderCount,
    avgOrderValue: '¥' + avgOrderValue,
  };
});

// 动态趋势图配置（按小时聚合）
const filteredTrendOption = computed(() => {
  const hourData = Array(24).fill(0).map(() => ({ amount: 0, count: 0 }));
  filteredOverviewTransactions.value.forEach(t => {
    const hour = parseInt(t.time.split(':')[0]);
    hourData[hour].amount += t.total_amount;
    hourData[hour].count += 1;
  });
  const hours = Array.from({ length: 24 }, (_, i) => `${i.toString().padStart(2,'0')}:00`);
  const amountData = hourData.map(h => h.amount);
  const countData = hourData.map(h => h.count);

  const option = JSON.parse(JSON.stringify(transactionTrendOption.value));
  option.xAxis.data = hours;
  option.series[0].data = amountData;
  option.series[1].data = countData;
  return option;
});

// 动态产品销售分布（各品类销售金额）
const filteredProductOption = computed(() => {
  const categoryAmount = {};
  filteredOverviewTransactions.value.forEach(t => {
    categoryAmount[t.category] = (categoryAmount[t.category] || 0) + t.total_amount;
  });
  const data = Object.entries(categoryAmount).map(([name, value]) => ({ name, value }));
  const option = JSON.parse(JSON.stringify(productDistributionOption.value));
  option.series[0].data = data;
  return option;
});

const applyOverviewFilters = () => {
  // 可加加载状态
};
const resetOverviewFilters = () => {
  overviewFilters.value = { dateRange: [], stores: [], paymentMethods: [] };
};

// ========== 详细信息弹窗筛选 + 分页 ==========
const detailFilters = ref({
  dateRange: [],
  stores: [],
  paymentMethods: []
});

const filteredDetails = computed(() => {
  return allTransactions.value.filter(t => {
    if (detailFilters.value.dateRange && detailFilters.value.dateRange.length === 2) {
      if (t.date < detailFilters.value.dateRange[0] || t.date > detailFilters.value.dateRange[1]) return false;
    }
    if (detailFilters.value.stores.length && !detailFilters.value.stores.includes(t.store_location)) return false;
    if (detailFilters.value.paymentMethods.length && !detailFilters.value.paymentMethods.includes(t.payment_method)) return false;
    return true;
  });
});

const currentPage = ref(1);
const pageSize = ref(20);
const paginatedDetails = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value;
  const end = start + pageSize.value;
  return filteredDetails.value.slice(start, end);
});

const filteredDetailStats = computed(() => {
  const trans = filteredDetails.value;
  const totalOrders = trans.length;
  // 模拟已完成/进行中（假设所有订单都是已完成）
  const completedOrders = trans.length;
  const pendingOrders = 0;
  return { totalOrders, completedOrders, pendingOrders };
});

const applyDetailFilters = () => {
  currentPage.value = 1;
};
const resetDetailFilters = () => {
  detailFilters.value = { dateRange: [], stores: [], paymentMethods: [] };
  currentPage.value = 1;
};
const handleSizeChange = (size) => {
  pageSize.value = size;
  currentPage.value = 1;
};
const handleCurrentChange = (page) => {
  currentPage.value = page;
};

// ========== 原有统计数据（可保留，但卡片上的今日数据建议基于mock计算） ==========
// 计算今日数据（基于mock中日期为今天的交易）
const todayStr = new Date().toISOString().split('T')[0];
const todayTransactions = computed(() => allTransactions.value.filter(t => t.date === todayStr));

const transactionStats = computed(() => {
  const trans = todayTransactions.value;
  const totalSales = trans.reduce((sum, t) => sum + t.total_amount, 0);
  const orderCount = trans.length;
  const avgOrderValue = orderCount ? (totalSales / orderCount).toFixed(2) : 0;
  const totalOrders = allTransactions.value.length;
  const completedOrders = totalOrders; // 假设全部完成
  const pendingOrders = 0;
  return {
    totalSales: '¥' + totalSales.toLocaleString(),
    orderCount,
    avgOrderValue: '¥' + avgOrderValue,
    totalOrders,
    completedOrders,
    pendingOrders
  };
});

// 原有流水数据详细信息（可弃用，现用分页数据代替）
// 保留但不再使用，或者可以清空
// const transactionDetails = ref([]);

// 原有统计数据（情感部分）
const stats = ref({
  totalReviews: 1245,
  positiveCount: 789,
  negativeCount: 234,
  positiveRate: 72.3,
  trendChange: 3.5,
  alertCount: 12,
  hotTopicCount: 8,
  topTopic: "新品发布"
})

// 情感分布数据
const emotionDistribution = ref([
  { channel: '微博', positive: 245, negative: 67, positivePercent: 78.5 },
  { channel: '微信', positive: 189, negative: 45, positivePercent: 80.7 },
  { channel: '抖音', positive: 321, negative: 98, positivePercent: 76.5 },
  { channel: '电商', positive: 156, negative: 24, positivePercent: 86.7 }
])

// 近期评论数据
const recentComments = ref([
  { id: 1, text: "这款新产品真是太棒了，质量超赞！", source: '微博', time: '10:25', emotion: 'positive' },
  { id: 2, text: "物流有点慢，但是产品还不错", source: '淘宝', time: '10:22', emotion: 'neutral' },
  { id: 3, text: "客服态度很差，不会再买了", source: '京东', time: '10:20', emotion: 'negative' },
  { id: 4, text: "性价比很高，值得推荐", source: '小红书', time: '10:18', emotion: 'positive' },
  { id: 5, text: "产品质量有问题，申请退货", source: '天猫', time: '10:15', emotion: 'negative' }
])

// 详细评论数据
const detailedComments = ref([
  { text: "这款新产品真是太棒了，质量超赞！", source: '微博', sentiment: '正面', intensity: '强', timestamp: '2023-12-01 10:25:30' },
  { text: "物流有点慢，但是产品还不错", source: '淘宝', sentiment: '中性', intensity: '中', timestamp: '2023-12-01 10:22:15' },
  { text: "客服态度很差，不会再买了", source: '京东', sentiment: '负面', intensity: '强', timestamp: '2023-12-01 10:20:45' },
  { text: "性价比很高，值得推荐", source: '小红书', sentiment: '正面', intensity: '中', timestamp: '2023-12-01 10:18:20' },
  { text: "产品质量有问题，申请退货", source: '天猫', sentiment: '负面', intensity: '强', timestamp: '2023-12-01 10:15:10' },
  { text: "包装精美，送货很快，非常满意", source: '拼多多', sentiment: '正面', intensity: '中', timestamp: '2023-12-01 10:12:30' }
])

// 图表数据
const chartTabs = ref([
  { id: 'emotion', label: '情感趋势' },
  { id: 'marketing', label: '营销效果' },
  { id: 'classification', label: '情感分类' }
])

const marketingData = ref([
  { name: '新品推广', effectiveness: 85 },
  { name: '节日促销', effectiveness: 72 },
  { name: '品牌合作', effectiveness: 68 },
  { name: '内容营销', effectiveness: 76 }
])

const classificationDistribution = ref([
  { type: '非常满意', percentage: 25, color: '#52c41a' },
  { type: '满意', percentage: 35, color: '#73d13d' },
  { type: '一般', percentage: 20, color: '#ffd666' },
  { type: '不满意', percentage: 15, color: '#ff7875' },
  { type: '非常不满意', percentage: 5, color: '#ff4d4f' }
])

// 营销活动数据
const marketingActivities = ref([
  { id: 1, name: '双11促销活动', participants: '2.4万', effect: '优秀', engagement: 85, conversion: 12, date: '2023-11-11', priority: 'high' },
  { id: 2, name: '新品上市推广', participants: '1.8万', effect: '良好', engagement: 72, conversion: 8, date: '2023-10-15', priority: 'medium' },
  { id: 3, name: '品牌联合营销', participants: '1.2万', effect: '一般', engagement: 56, conversion: 5, date: '2023-09-20', priority: 'low' }
])

// 智能洞察数据
const insights = ref([
  { id: 1, type: '趋势洞察', date: '今日', text: '产品质量相关的正面情感显著增加，可能与最近的质量改进措施有关', action: 'continue_quality_improvement', actionText: '继续推进' },
  { id: 2, type: '风险预警', date: '本周', text: '物流配送相关的负面情感有所上升，需关注配送服务质量', action: 'improve_logistics', actionText: '优化物流' },
  { id: 3, type: '机会发现', date: '本月', text: '年轻用户群体对产品的互动功能表现出浓厚兴趣', action: 'develop_engagement_features', actionText: '开发功能' }
])

// 详细洞察数据
const detailedInsights = ref([
  { id: 1, title: '产品质量持续改善', description: '最近一个月，关于产品质量的正面评价增加了15%', recommendation: '继续保持高质量标准，并扩大宣传', priority: '高', expectedOutcome: '进一步提升品牌声誉' },
  { id: 2, title: '物流服务待优化', description: '物流配送相关的投诉在过去两周增加了8%', recommendation: '与物流合作伙伴协商改进服务标准', priority: '中', expectedOutcome: '减少负面评价，提高客户满意度' },
  { id: 3, title: '年轻用户互动需求', description: '18-30岁用户对社交分享功能的需求明显增长', recommendation: '开发更多社交互动功能', priority: '中', expectedOutcome: '提高用户粘性和活跃度' }
])

// 趋势洞察数据
const trendInsights = ref([
  { id: 1, text: '近一周正面情感呈稳步上升趋势，主要受益于新产品发布' },
  { id: 2, text: '价格敏感度在周末时段明显增加，可能与促销活动有关' },
  { id: 3, text: '负面情感主要集中在物流和售后环节，需重点关注' },
  { id: 4, text: '社交媒体上的情感波动较大，需加强监控' }
])

// 预警数据
const alerts = ref([
  { id: 1, title: '物流投诉增加', type: '风险', severity: '高', date: '2023-12-01 10:25', status: '待处理' },
  { id: 2, title: '产品质量质疑', type: '风险', severity: '中', date: '2023-12-01 09:45', status: '处理中' },
  { id: 3, title: '竞品负面营销', type: '风险', severity: '低', date: '2023-12-01 08:30', status: '已处理' },
  { id: 4, title: '服务态度投诉', type: '风险', severity: '中', date: '2023-11-30 17:20', status: '待处理' }
])

// 热点话题数据
const topics = ref([
  { rank: 1, name: '新品发布', mentions: 1245, sentiment: '正面', trend: '上升' },
  { rank: 2, name: '价格调整', mentions: 987, sentiment: '负面', trend: '平稳' },
  { rank: 3, name: '售后服务', mentions: 765, sentiment: '中性', trend: '下降' },
  { rank: 4, name: '物流配送', mentions: 654, sentiment: '负面', trend: '上升' },
  { rank: 5, name: '品牌活动', mentions: 543, sentiment: '正面', trend: '平稳' }
])

const overviewTrendOption = computed(() => ({
  tooltip: { trigger: 'axis' },
  legend: { data: ['正面指数', '负面指数'] },
  xAxis: { type: 'category', data: ['00:00', '04:00', '08:00', '12:00', '16:00', '20:00'] },
  yAxis: { type: 'value' },
  series: [
    { name: '正面指数', type: 'line', smooth: true, data: [65, 70, 68, 85, 90, 88], itemStyle: { color: '#67C23A' } },
    { name: '负面指数', type: 'line', smooth: true, data: [15, 12, 18, 10, 8, 5], itemStyle: { color: '#F56C6C' } }
  ]
}));

// 2. 渠道分布：堆叠柱状图
const channelDistOption = computed(() => ({
  tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },
  legend: { data: ['正面', '中性', '负面'] },
  xAxis: { type: 'category', data: ['小红书', '抖音', '微博', '京东', '天猫'] },
  yAxis: { type: 'value' },
  series: [
    { name: '正面', type: 'bar', stack: 'total', data: [320, 302, 301, 334, 390], itemStyle: { color: '#67C23A' } },
    { name: '中性', type: 'bar', stack: 'total', data: [120, 132, 101, 134, 90], itemStyle: { color: '#909399' } },
    { name: '负面', type: 'bar', stack: 'total', data: [20, 32, 91, 34, 10], itemStyle: { color: '#F56C6C' } }
  ]
}));

// 3. 人群分布：南丁格尔玫瑰图
const userGroupDistOption = computed(() => ({
  tooltip: { trigger: 'item' },
  series: [{
    type: 'pie',
    radius: [20, 140],
    roseType: 'area',
    itemStyle: { borderRadius: 5 },
    data: [
      { value: 40, name: 'Z世代' },
      { value: 33, name: '都市白领' },
      { value: 28, name: '精致妈妈' },
      { value: 22, name: '小镇青年' },
      { value: 18, name: '资深中产' }
    ]
  }]
}));

// 4. 30天长期趋势：面积图
const longTermTrendOption = computed(() => ({
  grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
  xAxis: { type: 'category', boundaryGap: false, data: Array.from({length: 30}, (_, i) => `${i+1}日`) },
  yAxis: { type: 'value' },
  series: [{
    name: '舆情热度',
    type: 'line',
    areaStyle: {
      color: {
        type: 'linear', x: 0, y: 0, x2: 0, y2: 1,
        colorStops: [{ offset: 0, color: 'rgba(64, 158, 255, 0.5)' }, { offset: 1, color: 'rgba(64, 158, 255, 0)' }]
      }
    },
    data: [120, 132, 101, 134, 90, 230, 210, 120, 132, 101, 134, 90, 230, 210, 120, 132, 101, 134, 90, 230, 210, 120, 132, 101, 134, 90, 230, 210, 180, 250]
  }]
}));

const generateTrendData = (base, type, seed) => {
  const points = 7;
  const data = [];
  for (let i = 0; i < points; i++) {
    const randomOffset = Math.sin(seed + i) * 10; 
    let value;
    if (type === 'positive') {
      value = base + (i * 5) + randomOffset;
    } else if (type === 'negative') {
      value = base - (i * 3) + randomOffset;
    } else {
      value = base + randomOffset;
    }
    data.push(Math.max(0, Math.round(value)));
  }
  return data;
};

const getActivityTrendOption = (activity) => {
  const themeColor = activity.effect === 'positive' ? '#67C23A' : (activity.effect === 'negative' ? '#F56C6C' : '#409EFF');
  const uniqueData = generateTrendData(
    activity.engagement || 50, 
    activity.effect, 
    activity.id
  );
  return {
    title: {
      text: `${activity.name} - 情感趋势走势`,
      textStyle: { fontSize: 13, color: '#606266', fontWeight: '500' },
      left: '0'
    },
    tooltip: { 
      trigger: 'axis',
      backgroundColor: 'rgba(255, 255, 255, 0.9)',
      borderWidth: 1,
      borderColor: themeColor
    },
    grid: { left: '30', right: '10', top: '50', bottom: '20', containLabel: true },
    xAxis: {
      type: 'category',
      boundaryGap: false,
      data: ['阶段1', '阶段2', '阶段3', '阶段4', '阶段5', '阶段6', '阶段7'],
      axisTick: { show: false },
      axisLine: { lineStyle: { color: '#DCDFE6' } }
    },
    yAxis: {
      type: 'value',
      splitLine: { lineStyle: { type: 'dashed', color: '#EBEEF5' } }
    },
    series: [
      {
        name: '影响指数',
        type: 'line',
        smooth: true,
        symbol: 'circle',
        symbolSize: 8,
        data: uniqueData,
        itemStyle: { color: themeColor },
        areaStyle: {
          color: {
            type: 'linear', x: 0, y: 0, x2: 0, y2: 1,
            colorStops: [
              { offset: 0, color: `${themeColor}60` },
              { offset: 1, color: `${themeColor}00` }
            ]
          }
        },
        lineStyle: { width: 3 }
      }
    ]
  };
};

// 计算属性
const filteredAlerts = computed(() => {
  if (showHighPriority.value) {
    return alerts.value.filter(alert => alert.severity === '高')
  }
  return alerts.value
})

// 饼图路径计算方法
const getPieSegmentPath = (index) => {
  const data = classificationDistribution.value
  let startAngle = 0
  let endAngle = 0
  
  // 计算起始和结束角度
  for (let i = 0; i <= index; i++) {
    startAngle = endAngle
    endAngle = startAngle + (data[i].percentage / 100) * 360
  }
  
  // 转换为弧度
  const startRad = (startAngle - 90) * Math.PI / 180
  const endRad = (endAngle - 90) * Math.PI / 180
  
  // 饼图中心点和半径
  const cx = 50
  const cy = 50
  const radius = 40
  
  // 计算起点和终点坐标
  const x1 = cx + radius * Math.cos(startRad)
  const y1 = cy + radius * Math.sin(startRad)
  const x2 = cx + radius * Math.cos(endRad)
  const y2 = cy + radius * Math.sin(endRad)
  
  // 大弧标志
  const largeArcFlag = (endAngle - startAngle) > 180 ? 1 : 0
  
  // 生成SVG路径
  return `
    M ${cx} ${cy}
    L ${x1} ${y1}
    A ${radius} ${radius} 0 ${largeArcFlag} 1 ${x2} ${y2}
    Z
  `
}

// 辅助方法
const getChannelIcon = (index) => {
  const icons = ['🐦', '💬', '🎬', '🛒']
  return icons[index] || '🐦'
}

const getEmotionColor = (index) => {
  const colors = ['var(--color-primary)', 'var(--color-success)', 'var(--color-error)', 'var(--color-warning)']
  return colors[index] || '#52c41a'
}

const getPriorityText = (priority) => {
  const map = { high: '高', medium: '中', low: '低' }
  return map[priority] || '低'
}

// 弹窗打开方法
const openEmotionOverviewDialog = () => {
  emotionOverviewDialogVisible.value = true
}

const openRealTimeStreamDialog = () => {
  realTimeStreamDialogVisible.value = true
}

const openEmotionDistributionDialog = () => {
  emotionDistributionDialogVisible.value = true
}

const openMarketingEffectDialog = () => {
  marketingEffectDialogVisible.value = true
}

const openInsightSummaryDialog = () => {
  insightSummaryDialogVisible.value = true
}

const openTrendAnalysisDialog = () => {
  trendAnalysisDialogVisible.value = true
}

const openAlertMonitoringDialog = () => {
  alertMonitoringDialogVisible.value = true
}

const openTopicHotnessDialog = () => {
  topicHotnessDialogVisible.value = true
}

const openTransactionOverviewDialog = () => {
  transactionOverviewDialogVisible.value = true
}

const openTransactionDetailsDialog = () => {
  transactionDetailsDialogVisible.value = true
}

// 关闭弹窗方法
const closeDialog = (done) => {
  done()
}

// 控制实时流
const toggleStream = () => {
  streamPaused.value = !streamPaused.value
}

// 执行洞察建议的方法
const takeAction = (action) => {
  console.log('执行行动:', action)
  switch(action) {
    case 'continue_quality_improvement':
      ElMessage.success('已安排继续推进质量改进措施')
      break
    case 'improve_logistics':
      ElMessage.success('已安排优化物流服务方案')
      break
    case 'develop_engagement_features':
      ElMessage.success('已安排开发用户互动功能')
      break
    default:
      ElMessage.info('已记录该行动建议')
  }
}

// 主要方法
const toggleAlertFilter = () => {
  console.log('切换报警过滤:', showHighPriority.value ? '仅高优先级' : '显示全部')
}

const handleTimeChange = () => {
  console.log('时间范围更改为:', timeRange.value)
  fetchData()
}

const refreshData = () => {
  console.log('刷新数据...')
  fetchData()
}

const handleLogout = () => {
  console.log('退出登录')
  router.push('/login')
}

// 从后端API获取数据（情感部分，保留）
const fetchData = async () => {
  loading.value = true
  loadingText.value = '正在加载数据...'
  error.value = null
  errorMessage.value = ''
  
  try {
    const data_url = import.meta.env.VITE_SERVER_API_ENDPOINT || "http://localhost:8000";
    const batchResponse = await axios.get( data_url + '/batch-data', {
      params: { time_range: timeRange.value }
    })
    
    const batchData = batchResponse.data

    stats.value = batchData.stats
    emotionDistribution.value = batchData.emotionDistribution
    recentComments.value = batchData.recentComments
    detailedComments.value = batchData.detailedComments
    marketingActivities.value = batchData.marketingActivities
    insights.value = batchData.insights
    detailedInsights.value = batchData.detailedInsights
    trendInsights.value = batchData.trendInsights
    alerts.value = batchData.alerts
    topics.value = batchData.topics
    console.log('数据加载成功')
  } catch (err) {
    console.error('数据加载失败:', err)
    error.value = err
    errorMessage.value = err.response?.data?.message || '网络请求失败，请检查后端服务是否正常运行'
  } finally {
    loading.value = false
  }
}

// 图表配置选项
const emotionTrendOption = ref({
  title: {
    text: '近24小时情感趋势变化',
    left: 'center',
    textStyle: {
      fontSize: 16,
      fontWeight: 'bold'
    }
  },
  tooltip: {
    trigger: 'axis',
    axisPointer: {
      type: 'cross'
    }
  },
  legend: {
    data: ['正面情感', '负面情感'],
    top: '10%'
  },
  grid: {
    left: '3%',
    right: '4%',
    bottom: '3%',
    containLabel: true
  },
  xAxis: {
    type: 'category',
    boundaryGap: false,
    data: ['0H', '4H', '8H', '12H', '16H', '20H', '24H']
  },
  yAxis: {
    type: 'value',
    name: '情感指数'
  },
  series: [
    {
      name: '正面情感',
      type: 'line',
      stack: '情感',
      data: [62, 78, 85, 90, 88, 82, 75],
      smooth: true,
      lineStyle: {
        color: '#52c41a',
        width: 3
      },
      areaStyle: {
        color: {
          type: 'linear',
          x: 0, y: 0, x2: 0, y2: 1,
          colorStops: [
            { offset: 0, color: 'rgba(82, 196, 26, 0.3)' },
            { offset: 1, color: 'rgba(82, 196, 26, 0.05)' }
          ]
        }
      }
    },
    {
      name: '负面情感',
      type: 'line',
      stack: '情感',
      data: [25, 20, 18, 15, 12, 18, 22],
      smooth: true,
      lineStyle: {
        color: '#ff4d4f',
        width: 3
      },
      areaStyle: {
        color: {
          type: 'linear',
          x: 0, y: 0, x2: 0, y2: 1,
          colorStops: [
            { offset: 0, color: 'rgba(255, 77, 79, 0.3)' },
            { offset: 1, color: 'rgba(255, 77, 79, 0.05)' }
          ]
        }
      }
    }
  ]
});

const marketingEffectOption = ref({
  title: {
    text: '近期营销活动效果分析',
    left: 'center',
    textStyle: {
      fontSize: 16,
      fontWeight: 'bold'
    }
  },
  tooltip: {
    trigger: 'axis',
    axisPointer: { type: 'shadow' }
  },
  grid: {
    left: '3%',
    right: '4%',
    bottom: '3%',
    containLabel: true
  },
  xAxis: {
    type: 'category',
    data: ['新品推广', '节日促销', '品牌合作', '内容营销'],
    axisTick: {
      alignWithLabel: true
    }
  },
  yAxis: {
    type: 'value',
    name: '效果指数'
  },
  series: [
    {
      name: '营销效果',
      type: 'bar',
      barWidth: '60%',
      data: [
        {
          value: 85,
          itemStyle: { color: '#52c41a' }
        },
        {
          value: 72,
          itemStyle: { color: '#73d13d' }
        },
        {
          value: 68,
          itemStyle: { color: '#ffd666' }
        },
        {
          value: 76,
          itemStyle: { color: '#1890ff' }
        }
      ],
      emphasis: {
        itemStyle: {
          shadowBlur: 10,
          shadowOffsetX: 0,
          shadowColor: 'rgba(0,0,0,0.5)'
        }
      }
    }
  ]
});

const emotionClassificationOption = ref({
  title: {
    text: '情感分类分布',
    left: 'center',
    textStyle: {
      fontSize: 16,
      fontWeight: 'bold'
    }
  },
  tooltip: {
    trigger: 'item',
    formatter: '{a} <br/>{b}: {c} ({d}%)'
  },
  legend: {
    orient: 'vertical',
    left: 'left',
    data: ['非常满意', '满意', '一般', '不满意', '非常不满意']
  },
  series: [
    {
      name: '情感分布',
      type: 'pie',
      radius: ['40%', '70%'],
      avoidLabelOverlap: false,
      itemStyle: {
        borderRadius: 10,
        borderColor: '#fff',
        borderWidth: 2
      },
      label: {
        show: true,
        formatter: '{b}: {d}%'
      },
      emphasis: {
        label: {
          show: true,
          fontSize: 16,
          fontWeight: 'bold'
        }
      },
      data: [
        { value: 25, name: '非常满意', itemStyle: { color: '#52c41a' } },
        { value: 35, name: '满意', itemStyle: { color: '#73d13d' } },
        { value: 20, name: '一般', itemStyle: { color: '#ffd666' } },
        { value: 15, name: '不满意', itemStyle: { color: '#ff7875' } },
        { value: 5, name: '非常不满意', itemStyle: { color: '#ff4d4f' } }
      ]
    }
  ]
});

// 原有流水趋势图表配置保持不变
const transactionTrendOption = ref({
  title: {
    text: '今日流水趋势',
    left: 'center',
    textStyle: {
      fontSize: 16,
      fontWeight: 'bold'
    }
  },
  tooltip: {
    trigger: 'axis',
    axisPointer: {
      type: 'cross'
    }
  },
  legend: {
    data: ['流水金额', '订单数量'],
    top: '10%'
  },
  grid: {
    left: '3%',
    right: '4%',
    bottom: '3%',
    containLabel: true
  },
  xAxis: {
    type: 'category',
    boundaryGap: false,
    data: ['08:00', '10:00', '12:00', '14:00', '16:00', '18:00', '20:00', '22:00']
  },
  yAxis: [
    {
      type: 'value',
      name: '流水金额(元)',
      position: 'left',
      axisLabel: {
        formatter: '{value}'
      }
    },
    {
      type: 'value',
      name: '订单数量',
      position: 'right',
      axisLabel: {
        formatter: '{value}'
      }
    }
  ],
  series: [
    {
      name: '流水金额',
      type: 'line',
      smooth: true,
      data: [12000, 18000, 25000, 22000, 28000, 35000, 28000, 15000],
      smoothMonotone: 'x',
      lineStyle: {
        color: '#52c41a',
        width: 3
      },
      areaStyle: {
        color: {
          type: 'linear',
          x: 0, y: 0, x2: 0, y2: 1,
          colorStops: [
            { offset: 0, color: 'rgba(82, 196, 26, 0.3)' },
            { offset: 1, color: 'rgba(82, 196, 26, 0.05)' }
          ]
        }
      }
    },
    {
      name: '订单数量',
      type: 'bar',
      yAxisIndex: 1,
      data: [12, 18, 25, 22, 28, 35, 28, 15],
      itemStyle: {
        color: '#1890ff'
      }
    }
  ]
});

// 产品销售分布图表配置（作为动态图表的基础模板）
const productDistributionOption = ref({
  title: {
    text: '产品销售分布',
    left: 'center',
    textStyle: {
      fontSize: 16,
      fontWeight: 'bold'
    }
  },
  tooltip: {
    trigger: 'item',
    formatter: '{a} <br/>{b}: {c} ({d}%)'
  },
  legend: {
    orient: 'vertical',
    left: 'left',
    data: [] // 动态
  },
  series: [
    {
      name: '销售额分布',
      type: 'pie',
      radius: ['40%', '70%'],
      avoidLabelOverlap: false,
      itemStyle: {
        borderRadius: 10,
        borderColor: '#fff',
        borderWidth: 2
      },
      label: {
        show: true,
        formatter: '{b}: {d}%'
      },
      emphasis: {
        label: {
          show: true,
          fontSize: 16,
          fontWeight: 'bold'
        }
      },
      data: [] // 动态
    }
  ]
});

onMounted(async () => {
  console.log('情感分析仪表盘组件已挂载')
  await fetchData()
})
</script>


<style scoped>
.dashboard {
  min-height: 100vh;
  background-color: #f5f7fa;
  font-family: 'PingFang SC', 'Microsoft YaHei', sans-serif;
}

.dashboard-container {
  padding: 40px;
  position: relative;
}

/* 错误提示样式 */
.error-alert {
  margin-bottom: 20px;
  border-radius: 8px;
}

.error-details {
  display: flex;
  justify-content:center;
  align-items: center;
  flex-wrap: nowrap;
  gap: 10px;
}

.error-details p {
  color: var(--color-info-dark);
}

/* 加载遮罩样式 */
.loading-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(255, 255, 255, 0.9);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  border-radius: 8px;
}

.loading-content {
  text-align: center;
  padding: 30px;
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
}

.loading-content p {
  margin-top: 15px;
  font-size: 16px;
  color: #666;
}

/* 响应式适配 */
@media (max-width: 1200px) {
  .dashboard-container {
    padding: 30px;
  }
  
  .title-content h2 {
    font-size: 24px;
  }
  
  .dashboard-subtitle {
    font-size: 14px;
  }
  
  .overview-card {
    padding: 20px;
  }
  
  .card-content .card-value {
    font-size: 28px;
  }
  
  .card-content .card-label {
    font-size: 14px;
  }
}

@media (max-width: 992px) {
  .dashboard-container {
    padding: 25px;
  }
  
  .overview-grid {
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 15px;
  }
  
  .overview-card {
    padding: 18px;
  }
  
  .card-icon {
    font-size: 30px;
    margin-bottom: 12px;
  }
  
  .card-content .card-value {
    font-size: 24px;
  }
}

@media (max-width: 768px) {
  .dashboard-container {
    padding: 20px;
  }
  
  .dashboard-title-section {
    flex-direction: column;
    align-items: stretch;
  }
  
  .dashboard-controls {
    justify-content: space-around;
  }
  
  .overview-grid {
    grid-template-columns: 1fr;
    gap: 12px;
  }
  
  .overview-card {
    padding: 16px;
  }
  
  .card-icon {
    font-size: 28px;
  }
  
  .card-content .card-value {
    font-size: 22px;
  }
  
  .card-content .card-label {
    font-size: 13px;
  }
  
  .card-status {
    gap: 8px;
  }
  
  .status-tag {
    padding: 3px 10px;
    font-size: 11px;
  }
}

@media (max-width: 576px) {
  .dashboard-container {
    padding: 15px;
  }
  
  .title-content h2 {
    font-size: 20px;
  }
  
  .dashboard-subtitle {
    font-size: 12px;
  }
  
  .dashboard-controls {
    justify-content: space-around;
    align-items: stretch;
    gap: 10px;
  }
  
  .time-control {
    justify-content: space-between;
  }
  
  .overview-card {
    padding: 14px;
  }
  
  .card-icon {
    font-size: 24px;
    margin-bottom: 10px;
  }
  
  .card-content .card-value {
    font-size: 20px;
  }
  
  .card-content .card-label {
    font-size: 12px;
    margin-bottom: 8px;
  }
  
  .card-trend {
    font-size: 12px;
  }
  
  .topic-info {
    font-size: 12px;
  }
}

.dashboard-title-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 32px;
  flex-wrap: wrap;
  gap: 24px;
}

.title-content h2 {
  font-size: 32px;
  font-weight: 700;
  margin: 0 0 12px 0;
  color: #2c3e50;
  line-height: 1.2;
}

.dashboard-subtitle {
  font-size: 16px;
  color: #7f8c8d;
  margin: 0;
  line-height: 1.4;
}

.dashboard-controls {
  display: flex;
  align-items: center;
  gap: 24px;
  flex-wrap: wrap;
}

.time-control {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px 16px;
  background-color: rgba(24, 144, 255, 0.05);
  border-radius: 8px;
}

.control-label {
  align-items: center;
  display: flex;
  gap:4px;
  font-size: 14px;
  font-weight: 500;
  color: #546e7a;
  white-space: nowrap;
}

.time-select {
  min-width: 160px;
}

.btn-refresh {
  background-color: var(--color-primary);
  border: none;
  color: white;
  padding: 10px 20px;
  border-radius: 8px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.3s ease;
  font-weight: 500;
}

.btn-refresh:hover:not(:disabled) {
  background-color: var(--color-primary-hover);
}

.btn-refresh:disabled {
  background: #d9d9d9;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.overview-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 24px;
  margin-bottom: 32px;
}

.overview-card {
  background: white;
  border-radius: 16px;
  padding: 28px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
  cursor: pointer;
  transition: all 0.3s ease;
  border: 2px solid transparent;
  position: relative;
  overflow: hidden;
}

.overview-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, var(--color-primary-hover), #36cfc9);
  transform: scaleX(0);
  transition: transform 0.3s ease;
}

.overview-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.12);
  border-color: rgba(24, 144, 255, 0.2);
}

.overview-card:hover::before {
  transform: scaleX(1);
}

.card-total:hover {
  border-color: rgba(82, 196, 26, 0.3);
}

.card-total::before {
  background: linear-gradient(90deg, #52c41a, #73d13d);
}

.card-success:hover {
  border-color: rgba(115, 209, 61, 0.3);
}

.card-success::before {
  background: linear-gradient(90deg, #73d13d, #95de64);
}

.card-warning:hover {
  border-color: rgba(250, 173, 20, 0.3);
}

.card-warning::before {
  background: linear-gradient(90deg, #faad14, #ffd666);
}

.card-environment:hover {
  border-color: rgba(250, 140, 22, 0.3);
}

.card-environment::before {
  background: linear-gradient(90deg, #fa8c16, #ffad46);
}

.card-total:hover {
  border-color: #52c41a;
}

.card-success:hover {
  border-color: #73d13d;
}

.card-warning:hover {
  border-color: #faad14;
}

.card-environment:hover {
  border-color: #fa8c16;
}

.card-icon {
  font-size: 42px;
  margin-bottom: 20px;
  display: block;
}

.card-content {
  position: relative;
  z-index: 1;
}

.card-content .card-value {
  font-size: 36px;
  font-weight: 700;
  color: #2c3e50;
  margin-bottom: 12px;
  line-height: 1.1;
}

.card-content .card-label {
  font-size: 18px;
  color: #7f8c8d;
  margin-bottom: 16px;
  font-weight: 400;
}

.card-status {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
  align-items: center;
}

.status-tag {
  padding: 6px 16px;
  border-radius: 16px;
  font-size: 13px;
  font-weight: 500;
  transition: all 0.3s ease;
}

.status-tag:hover {
  transform: translateY(-2px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.status-tag.positive {
  background: rgba(82, 196, 26, 0.15);
  color: #52c41a;
}

.status-tag.negative {
  background: rgba(255, 77, 79, 0.15);
  color: #ff4d4f;
}

.card-trend {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 15px;
  font-weight: 600;
  padding: 8px 12px;
  background-color: rgba(0, 0, 0, 0.02);
  border-radius: 8px;
  width: fit-content;
  transition: all 0.3s ease;
}

.card-trend:hover {
  background-color: rgba(0, 0, 0, 0.04);
  transform: translateY(-2px);
}

.card-trend.positive {
  color: #52c41a;
}

.card-trend.warning {
  color: #faad14;
}

.card-trend.neutral {
  color: #1890ff;
}

.topic-info {
  font-size: 15px;
  color: #7f8c8d;
  line-height: 1.4;
}

.topic-item {
  font-weight: 600;
  color: #2c3e50;
  display: inline-block;
  margin-left: 4px;
  padding: 4px 8px;
  background-color: rgba(24, 144, 255, 0.1);
  border-radius: 6px;
  transition: all 0.3s ease;
}

.topic-item:hover {
  background-color: rgba(24, 144, 255, 0.2);
  transform: translateY(-2px);
}

.main-data-section {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 32px;
  margin-bottom: 32px;
}

@media (max-width: 1200px) {
  .main-data-section {
    grid-template-columns: 1fr;
  }
}

.left-panel,
.right-panel {
  display: flex;
  flex-direction: column;
  gap: 28px;
}

/* 数据卡片样式优化 */
.data-card {
  border-radius: 16px !important;
  border: none !important;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08) !important;
  transition: all 0.3s ease !important;
  overflow: hidden;
}

.data-card:hover {
  transform: translateY(-4px) !important;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.12) !important;
}

.data-card .card-header {
  padding: 20px 24px !important;
  background-color: rgba(24, 144, 255, 0.02) !important;
  border-bottom: 1px solid rgba(0, 0, 0, 0.05) !important;
}

.data-card .header-title {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 8px;
}

.data-card .header-title .card-icon {
  font-size: 24px;
  margin: 0;
}

.data-card .header-title h3 {
  font-size: 20px;
  font-weight: 600;
  color: #2c3e50;
  margin: 0;
}

.data-card .header-subtitle {
  font-size: 14px;
  color: #7f8c8d;
  margin: 0;
  line-height: 1.4;
}

.data-card .el-card__body {
  padding: 24px !important;
}

/* 实时监测流样式优化 */
.stream-container {
  max-height: 300px;
  overflow-y: auto;
  padding-right: 8px;
}

.stream-container::-webkit-scrollbar {
  width: 6px;
}

.stream-container::-webkit-scrollbar-track {
  background: rgba(0, 0, 0, 0.05);
  border-radius: 3px;
}

.stream-container::-webkit-scrollbar-thumb {
  background: rgba(0, 0, 0, 0.2);
  border-radius: 3px;
}

.stream-container::-webkit-scrollbar-thumb:hover {
  background: rgba(0, 0, 0, 0.3);
}

.stream-item {
  display: flex;
  align-items: flex-start;
  gap: 16px;
  padding: 16px;
  background-color: rgba(0, 0, 0, 0.02);
  border-radius: 12px;
  margin-bottom: 12px;
  transition: all 0.3s ease;
  border-left: 4px solid transparent;
}

.stream-item:hover {
  background-color: rgba(0, 0, 0, 0.04);
  transform: translateX(4px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.stream-item:nth-child(odd) {
  background-color: rgba(24, 144, 255, 0.02);
}

.stream-item:nth-child(odd):hover {
  background-color: rgba(24, 144, 255, 0.05);
}

.stream-emotion {
  font-size: 24px;
  flex-shrink: 0;
  margin-top: 4px;
}

.stream-content {
  flex: 1;
}

.stream-text {
  font-size: 15px;
  color: #2c3e50;
  margin-bottom: 8px;
  line-height: 1.4;
  text-align: start;
}

.stream-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 12px;
  font-size: 13px;
  color: #95a5a6;
}

.stream-source {
  font-weight: 500;
  background-color: rgba(0, 0, 0, 0.05);
  padding: 2px 8px;
  border-radius: 12px;
}

.stream-time {
  font-family: monospace;
}

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

.header-subtitle {
  font-size: 14px;
  color: #666;
  margin: 0;
}

.emotion-distribution {
  padding: 0 20px 20px;
}

.dist-item {
  margin-bottom: 20px;
}

.dist-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
  flex-wrap: wrap;
  gap: 10px;
}

.dist-range {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  color: #333;
  font-weight: 500;
}

.range-icon {
  font-size: 16px;
}

.dist-count {
  font-size: 14px;
  color: #666;
}

.dist-percentage {
  font-size: 14px;
  font-weight: 500;
  color: #52c41a;
}

.dist-bar-container {
  width: 100%;
  height: 8px;
  background: #f0f0f0;
  border-radius: 4px;
  overflow: hidden;
}

.dist-bar {
  width: 100%;
  height: 100%;
}

.bar-fill {
  height: 100%;
  border-radius: 4px;
  transition: width 0.6s ease;
}

.stream-container {
  max-height: 300px;
  overflow-y: auto;
  padding: 0 20px 20px;
}

.stream-item {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 16px;
  background: #f9f9f9;
  border-radius: 8px;
  margin-bottom: 12px;
  transition: all 0.3s ease;
}

.stream-item:hover {
  background: #f0f0f0;
  transform: translateX(5px);
}

.stream-emotion {
  font-size: 20px;
  min-width: 30px;
}

.stream-content {
  flex: 1;
}

.stream-text {
  font-size: 14px;
  color: #333;
  margin-bottom: 8px;
  line-height: 1.4;
}

.stream-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 12px;
  color: #999;
}

.stream-controls {
  display: flex;
  gap: 10px;
}

.chart-container {
  padding: 20px;
}

.chart-tabs {
  display: flex;
  gap: 10px;
}

.chart-tab {
  padding: 6px 16px;
  border-radius: 20px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s ease;
  background: #f0f0f0;
  color: #666;
  border: none;
  outline: none;
}

.chart-tab:hover {
  background: #e0e0e0;
}

.chart-tab.active {
  background: var(--color-primary-dark);
  color: white;
}

.chart-content {
  margin-top: 20px;
}

.chart-content h4 {
  font-size: 16px;
  font-weight: bold;
  margin: 0 0 16px 0;
  color: #333;
}

.chart {
  height: 300px;
}

.bottom-section {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

@media (max-width: 768px) {
  .bottom-section {
    grid-template-columns: 1fr;
  }
}

.data-card,
.insight-card {
  border-radius: 12px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s ease;
}

.data-card:hover,
.insight-card:hover,
.transaction-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
}

.header-title .marketing-count {
  background: var(--color-error);
  color: white;
  font-size: 12px;
  padding: 3px 8px;
  border-radius: 10px;
  margin-left: 10px;
  font-weight: bold;
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

.marketing-list {
  padding: 0 20px 20px;
}

.marketing-item {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 16px;
  background: #f9f9f9;
  border-radius: 8px;
  margin-bottom: 12px;
  transition: all 0.3s ease;
}

.marketing-item:hover {
  background: #f0f0f0;
  transform: translateX(5px);
}

.marketing-item.priority-high {
  border-left: 4px solid var(--color-danger);
}

.marketing-item.priority-medium {
  border-left: 4px solid var(--color-warning);
}

.marketing-item.priority-low {
  border-left: 4px solid var(--color-info);
}

.marketing-icon {
  font-size: 20px;
  min-width: 30px;
}

.marketing-content {
  flex: 1;
}

.marketing-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
  flex-wrap: wrap;
  gap: 10px;
}

.activity-name {
  font-size: 14px;
  font-weight: bold;
  color: #333;
}

.effect-badge {
  font-size: 12px;
  padding: 2px 8px;
  border-radius: 10px;
  font-weight: 500;
}

.badge-excellent {
  background: var(--color-success-hover);
  color: white;
}

.badge-good {
  background: var(--color-primary-hover);
  color: #fff;
}

.badge-average {
  background: var(--color-warning-hover);
  color: #fff;
}
.badge-poor {
  background: var(--color-danger-hover);
  color: #fff;
}

.marketing-details {
  display: flex;
  gap: 20px;
  margin-bottom: 8px;
  flex-wrap: wrap;
}

.detail-item {
  display: flex;
  align-items: center;
  gap: 5px;
}

.detail-label {
  font-size: 12px;
  color: #666;
}

.detail-value {
  font-size: 12px;
  font-weight: 500;
  color: #333;
}

.marketing-time {
  font-size: 12px;
  color: #999;
  justify-self: end;
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

.insight-content {
  padding: 0 20px 20px;
}

.insight-item {
  padding: 16px;
  background: #f9f9f9;
  border-radius: 8px;
  margin-bottom: 12px;
  transition: all 0.3s ease;
}

.insight-item:hover {
  background: #f0f0f0;
  transform: translateX(5px);
}

.insight-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
  flex-wrap: wrap;
  gap: 10px;
}

.insight-type {
  background: var(--color-primary-dark);
  color: white;
  font-size: 12px;
  padding: 2px 8px;
  border-radius: 10px;
  font-weight: 500;
}

.insight-date {
  font-size: 12px;
  color: #999;
}

.insight-text {
  font-size: 14px;
  color: #333;
  margin-bottom: 12px;
  line-height: 1.4;
}

.insight-action {
  display: flex;
  justify-content: flex-end;
}

.dialog-content {
  max-height: 70vh;
  overflow-y: auto;
}

.dialog-content h3 {
  font-size: 20px;
  font-weight: bold;
  margin: 0 0 20px 0;
  color: #333;
}

.dialog-content p {
  font-size: 14px;
  color: #666;
  line-height: 1.6;
  margin: 0 0 16px 0;
}

.dialog-content ul {
  margin: 0 0 20px 20px;
  padding: 0;
}

.dialog-content li {
  font-size: 14px;
  color: #666;
  line-height: 1.6;
  margin-bottom: 8px;
}

.chart-placeholder {
  margin: 20px 0;
  text-align: center;
}

.chart-placeholder p {
  font-size: 14px;
  color: #999;
  margin-bottom: 10px;
}

.activity-detail h4 {
  font-size: 16px;
  font-weight: bold;
  margin: 0 0 12px 0;
  color: #333;
}

.insight-detail h4 {
  font-size: 16px;
  font-weight: bold;
  margin: 0 0 12px 0;
  color: #333;
}

.trend-insights h4 {
  font-size: 16px;
  font-weight: bold;
  margin: 20px 0 12px 0;
  color: #333;
}

@media (max-width: 768px) {
  .dashboard-container {
    padding: 20px;
  }
  
  .dashboard-header {
    padding: 20px;
    flex-direction: column;
    align-items: flex-start;
    gap: 20px;
  }
  
  .header-right {
    width: 100%;
    justify-content: space-between;
  }
  
  .dashboard-title-section {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .overview-grid {
    grid-template-columns: 1fr;
  }
  
  .main-data-section {
    grid-template-columns: 1fr;
  }
  
  .bottom-section {
    grid-template-columns: 1fr;
  }
}

/* 无障碍访问样式 */
/* 屏幕阅读器专用样式 */
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}

/* 确保颜色对比度符合无障碍标准 */
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}

/* 高对比度模式支持 */
@media (prefers-contrast: high) {
  .overview-card {
    border: 2px solid #000;
  }
  
  .data-card {
    border: 2px solid #000 !important;
  }
  
  .btn-refresh {
    border: 2px solid #000;
  }
}
</style>