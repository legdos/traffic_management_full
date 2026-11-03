<template>
  <section class="panel">
    <header>
      <h3>车辆状态</h3>
      <span class="count">{{ vehicles.length }} 辆</span>
    </header>

    <ul class="vehicles">
      <li v-for="row in rows" :key="row.vehicle.id">
        <div class="row">
          <span class="vid">车辆 {{ row.vehicle.id }}</span>
          <span class="state" :style="{ color: colorOf(row.vehicle.currentAction) }">
            {{ textOf(row.vehicle.currentAction) }}
          </span>
          <span class="rest">本状态剩 {{ row.vehicle.remainingTime ?? 0 }} 分</span>
        </div>

        <div v-if="row.mission" class="mission">
          <div class="row small">
            <span class="goods">{{ row.mission.goodsType }}</span>
            <span class="route">
              {{ nameOf(row.mission.factoryId) }} → {{ nameOf(row.mission.destFactoryId) }}
            </span>
          </div>
          <div class="bar">
            <i :style="{ width: percent(row.mission) }"></i>
          </div>
          <div class="row tiny">
            <span>{{ row.mission.status }}</span>
            <span>任务剩 {{ remainOf(row.mission) }} 分 · 已用 {{ row.mission.elapsedMinutes ?? 0 }} 分</span>
          </div>
        </div>

        <div v-else class="row tiny muted">暂无任务</div>
      </li>
    </ul>
  </section>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  vehicles: { type: Array, default: () => [] },
  /** 进行中的任务，用来和车辆关联 */
  missions: { type: Array, default: () => [] },
  factories: { type: Array, default: () => [] },
})

const STATUS_TEXT = { 1: '空闲', 2: '接单行驶', 3: '装货', 4: '运货行驶', 5: '卸货', 6: '停留等待', 7: '初始状态' }
const STATUS_COLOR = { 1: '#909399', 2: '#409EFF', 3: '#E6A23C', 4: '#67C23A', 5: '#F56C6C', 6: '#B37FEB', 7: '#606266' }

const nameById = computed(() => {
  const map = new Map()
  props.factories.forEach((f) => map.set(f.id, f.factoryName))
  return map
})

const missionByCar = computed(() => {
  const map = new Map()
  props.missions.forEach((m) => map.set(m.carId, m))
  return map
})

/** 车辆 + 它当前的任务，模板里直接遍历，避免反复查 Map */
const rows = computed(() =>
  props.vehicles.map((vehicle) => ({
    vehicle,
    mission: missionByCar.value.get(vehicle.id) || null,
  })),
)

/** 任务剩余分钟：后端已按「当前状态剩余 + 后续阶段估算」算好 */
function remainOf(mission) {
  const remain = Number(mission.remainMinutes)
  if (Number.isFinite(remain) && remain >= 0) {
    return remain
  }
  const total = Number(mission.totalMinutes) || 0
  const elapsed = Number(mission.elapsedMinutes) || 0
  return Math.max(0, total - elapsed)
}

function percent(mission) {
  const elapsed = Number(mission.elapsedMinutes) || 0
  const total = elapsed + remainOf(mission)
  if (total <= 0) return '0%'
  return `${Math.min(100, Math.round((elapsed / total) * 100))}%`
}

function textOf(actionId) {
  return STATUS_TEXT[actionId] || '未知'
}

function colorOf(actionId) {
  return STATUS_COLOR[actionId] || '#909399'
}

function nameOf(factoryId) {
  return nameById.value.get(factoryId) || `工厂${factoryId}`
}
</script>

<style scoped>
.panel {
  position: absolute;
  top: 64px;
  left: 16px;
  width: 300px;
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

.vehicles {
  list-style: none;
  margin: 0;
  padding: 0;
}

.vehicles > li {
  padding: 8px 0;
  border-bottom: 1px solid #ebeef5;
}

.vehicles > li:last-child {
  border-bottom: none;
}

.row {
  display: flex;
  align-items: center;
  gap: 8px;
}

.row.small {
  font-size: 12px;
  color: #606266;
}

.row.tiny {
  font-size: 11px;
  color: #909399;
  justify-content: space-between;
}

.vid {
  font-weight: 600;
  min-width: 62px;
}

.state {
  font-weight: 600;
}

.rest {
  margin-left: auto;
  color: #909399;
  font-size: 12px;
}

.mission {
  margin-top: 6px;
  padding: 6px 8px;
  background: #f5f7fa;
  border-radius: 6px;
}

.goods {
  font-weight: 600;
  color: #303133;
}

.route {
  margin-left: auto;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  max-width: 190px;
}

.bar {
  height: 4px;
  margin: 5px 0 3px;
  border-radius: 2px;
  background: #e4e7ed;
  overflow: hidden;
}

.bar > i {
  display: block;
  height: 100%;
  background: #409eff;
  transition: width 0.4s ease;
}

.muted {
  color: #c0c4cc;
}
</style>
