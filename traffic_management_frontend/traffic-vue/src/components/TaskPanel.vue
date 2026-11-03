<template>
  <section class="panel">
    <header>
      <h3>运输任务</h3>
      <span class="count">{{ pending.length + active.length + done.length }} 条</span>
    </header>

    <div class="group">
      <h4>待接单 <em>{{ pending.length }}</em></h4>
      <ul v-if="pending.length">
        <li v-for="m in pending" :key="m.id">
          <span class="goods">{{ m.goodsType }}</span>
          <span class="route">{{ nameOf(m.factoryId) }} → {{ nameOf(m.destFactoryId) }}</span>
          <span class="km">{{ m.distanceKm }} km</span>
        </li>
      </ul>
      <p v-else class="empty">暂无</p>
    </div>

    <div class="group">
      <h4>进行中 <em>{{ active.length }}</em></h4>
      <ul v-if="active.length">
        <li v-for="m in active" :key="m.id" class="active-item">
          <div class="line">
            <span class="goods">{{ m.goodsType }}</span>
            <span class="badge">{{ m.status }}</span>
            <span class="car">车{{ m.carId }}</span>
          </div>
          <div class="route-line">{{ nameOf(m.factoryId) }} → {{ nameOf(m.destFactoryId) }}</div>
          <div class="bar"><i :style="{ width: percent(m) }"></i></div>
          <div class="line tiny">
            <span>{{ m.elapsedMinutes ?? 0 }} / {{ m.totalMinutes ?? 0 }} 分</span>
            <span>{{ m.distanceKm }} km</span>
          </div>
        </li>
      </ul>
      <p v-else class="empty">暂无</p>
    </div>

    <div class="group">
      <h4>已完成 <em>{{ done.length }}</em></h4>
      <ul v-if="done.length">
        <li v-for="m in done" :key="m.id" class="done-item">
          <span class="goods">{{ m.goodsType }}</span>
          <span class="route">{{ nameOf(m.factoryId) }} → {{ nameOf(m.destFactoryId) }}</span>
          <span class="km">车{{ m.carId }}</span>
        </li>
      </ul>
      <p v-else class="empty">暂无</p>
    </div>
  </section>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  pending: { type: Array, default: () => [] },
  active: { type: Array, default: () => [] },
  done: { type: Array, default: () => [] },
  factories: { type: Array, default: () => [] },
})

const nameById = computed(() => {
  const map = new Map()
  props.factories.forEach((f) => map.set(f.id, f.factoryName))
  return map
})

function nameOf(factoryId) {
  return nameById.value.get(factoryId) || `工厂${factoryId}`
}

function percent(mission) {
  const total = Number(mission.totalMinutes) || 0
  const elapsed = Number(mission.elapsedMinutes) || 0
  if (total <= 0) return '0%'
  return `${Math.min(100, Math.round((elapsed / total) * 100))}%`
}
</script>

<style scoped>
.panel {
  position: absolute;
  top: 64px;
  right: 16px;
  width: 330px;
  max-height: calc(100vh - 100px);
  overflow-y: auto;
  background: rgba(255, 255, 255, 0.96);
  border-radius: 10px;
  box-shadow: 0 6px 18px rgba(0, 0, 0, 0.16);
  padding: 12px 14px 14px;
  font-size: 13px;
  color: #303133;
  z-index: 20;
}

header {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  margin-bottom: 8px;
}

h3 {
  margin: 0;
  font-size: 14px;
  font-weight: 600;
}

.count {
  color: #909399;
  font-size: 12px;
}

.group {
  margin-bottom: 10px;
}

.group:last-child {
  margin-bottom: 0;
}

h4 {
  margin: 0 0 6px;
  font-size: 12px;
  font-weight: 600;
  color: #606266;
}

h4 em {
  font-style: normal;
  color: #409eff;
  margin-left: 4px;
}

ul {
  list-style: none;
  margin: 0;
  padding: 0;
}

li {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 4px 0;
  border-bottom: 1px dashed #ebeef5;
  font-size: 12px;
}

li:last-child {
  border-bottom: none;
}

.goods {
  font-weight: 600;
  flex: none;
}

.route {
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  color: #606266;
}

.km {
  flex: none;
  color: #909399;
  font-size: 11px;
}

.active-item {
  display: block;
  padding: 6px 8px;
  margin-bottom: 4px;
  background: #f5f7fa;
  border-radius: 6px;
  border-bottom: none;
}

.line {
  display: flex;
  align-items: center;
  gap: 6px;
}

.line.tiny {
  justify-content: space-between;
  font-size: 11px;
  color: #909399;
  margin-top: 3px;
}

.route-line {
  margin: 3px 0;
  font-size: 11px;
  color: #606266;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.badge {
  padding: 0 5px;
  border-radius: 3px;
  background: #ecf5ff;
  color: #409eff;
  font-size: 11px;
}

.car {
  margin-left: auto;
  color: #409eff;
  font-size: 11px;
}

.bar {
  height: 4px;
  margin: 4px 0 2px;
  border-radius: 2px;
  background: #e4e7ed;
  overflow: hidden;
}

.bar > i {
  display: block;
  height: 100%;
  background: #67c23a;
  transition: width 0.4s ease;
}

.done-item {
  color: #909399;
}

.done-item .goods {
  color: #909399;
}

.empty {
  margin: 0 0 4px;
  font-size: 12px;
  color: #c0c4cc;
}
</style>
