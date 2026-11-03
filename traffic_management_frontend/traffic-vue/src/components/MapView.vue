<template>
  <div class="sim-page">
    <div id="map-container"></div>

    <!-- 顶部控制条 -->
    <div class="toolbar">
      <span class="item">第 <b>{{ state.tick }}</b> 轮</span>
      <span class="item">仿真 <b>{{ state.simMinutes }}</b> 分钟</span>
      <span class="badge" :class="state.running ? 'on' : 'off'">
        {{ state.running ? '运行中' : '已停止' }}
      </span>
      <button v-if="!state.running" @click="run(startSim)">继续</button>
      <button v-else class="ghost" @click="run(stopSim)">暂停</button>
      <button class="ghost" @click="resetAndStart">重置</button>
      <button class="ghost" :disabled="importing" @click="importFactoriesFromAmap">
        {{ importing ? '抓取中…' : '抓取真实工厂' }}
      </button>
    </div>

    <VehiclePanel :vehicles="state.vehicles" :missions="state.activeMissions" :factories="factories" />
    <TaskPanel
      :pending="state.pendingMissions"
      :active="state.activeMissions"
      :done="state.doneMissions"
      :factories="factories"
    />

    <div v-if="errorMsg" class="toast">{{ errorMsg }}</div>
    <div v-if="notice" class="toast info">{{ notice }}</div>
  </div>
</template>

<script setup>
import { onMounted, onUnmounted, reactive, ref } from 'vue'
import AMapLoader from '@amap/amap-jsapi-loader'
import {
  fetchRoute,
  fetchRoutePoints,
  fetchState,
  resetSim,
  startSim,
  stopSim,
  updatePickupPoints,
  updateRoutePoints,
} from '../api/sim'
import VehiclePanel from './VehiclePanel.vue'
import TaskPanel from './TaskPanel.vue'

/** 高德地图 key 与安全密钥 */
const AMAP_KEY = '4fe176fc16d356769714d97913538dce'
const AMAP_SECURITY_CODE = 'bb2549ae73d47cd79a1a27535a9e8f25'

/** 后端 route.roadType 的取值：表示这条折线是 JS API 规划出的真实道路 */
const NAVIGATION_ROAD_TYPE = '导航路线'

/** 轮询间隔（毫秒）：后端 tick 时位置会变，前端按 tickSeconds 做插值，所以可以频繁拉取 */
const POLL_INTERVAL = 1000

/** 位移超过这个距离（km）就不做动画，直接吸附（例如重置、瞬移） */
const SNAP_KM = 30

const STATUS_COLOR = {
  1: '#909399',
  2: '#409EFF',
  3: '#E6A23C',
  4: '#67C23A',
  5: '#F56C6C',
  6: '#B37FEB',
  7: '#606266',
}

const state = reactive({
  running: false,
  tick: 0,
  simMinutes: 0,
  /** 后端每轮的真实秒数，前端用它作为位移动画时长 */
  tickSeconds: 5,
  vehicles: [],
  pendingMissions: [],
  activeMissions: [],
  doneMissions: [],
})

const factories = ref([])
const errorMsg = ref('')
const notice = ref('')
const importing = ref(false)

let map = null
let AMap = null
let pollTimer = null

const factoryById = new Map()
const vehicleMarkers = new Map()
/** 工厂点位标记，重新导入工厂时需要整体清掉 */
const factoryMarkers = []
/** 每辆车的动画状态：当前插值位置 + 目标位置 */
const markerState = new Map()
/** 已规划过取货路线的「车辆:任务」，避免重复请求 */
const pickupPlanned = new Set()
/** 已规划出的取货段折线 */
const pickupPaths = new Map()
/** 每辆车当前行驶段的路线高亮：vehicleId -> Polyline */
const legLines = new Map()
let rafId = null
let lastFrame = 0
/** 路线折线缓存：routeId -> [[lng,lat],...] */
const routeCache = new Map()
/** 正在请求中的路线，避免同一路线并发重复请求 */
const routeLoading = new Map()

onMounted(async () => {
  window._AMapSecurityConfig = { securityJsCode: AMAP_SECURITY_CODE }
  try {
    AMap = await AMapLoader.load({
      key: AMAP_KEY,
      version: '2.0',
      plugins: ['AMap.Scale', 'AMap.ToolBar', 'AMap.Driving', 'AMap.PlaceSearch'],
    })
    map = new AMap.Map('map-container', {
      viewMode: '2D',
      zoom: 12,
      center: [104.0668, 30.5728],
    })
    map.addControl(new AMap.Scale())
    map.addControl(new AMap.ToolBar())

    await loadFactories()
    await loadState()
    setTimeout(() => map && map.resize(), 200)
    window.addEventListener('resize', handleResize)
    pollTimer = setInterval(loadState, POLL_INTERVAL)
    rafId = requestAnimationFrame(animate)
    await ensureAutoStart()
  } catch (e) {
    errorMsg.value = `地图加载失败：${e.message}`
  }
})

onUnmounted(() => {
  if (pollTimer) {
    clearInterval(pollTimer)
    pollTimer = null
  }
  if (rafId) {
    cancelAnimationFrame(rafId)
    rafId = null
  }
  window.removeEventListener('resize', handleResize)
  if (map) {
    map.destroy()
    map = null
  }
  factoryById.clear()
  vehicleMarkers.clear()
  factoryMarkers.length = 0
  markerState.clear()
  pickupPlanned.clear()
  pickupPaths.clear()
  legLines.clear()
  routeCache.clear()
  routeLoading.clear()
})

/** 每帧把车辆标记朝目标点插值推进，形成平滑移动 */
function animate(timestamp) {
  rafId = requestAnimationFrame(animate)
  if (timestamp - lastFrame < 40) {
    return
  }
  lastFrame = timestamp

  markerState.forEach((st, id) => {
    if (st.duration <= 0) {
      return
    }
    let t = (timestamp - st.start) / st.duration
    if (t >= 1) {
      t = 1
      st.duration = 0
    }
    const marker = vehicleMarkers.get(id)

    if (st.path && st.cum) {
      // 沿折线按弧长推进，拐弯处不会切角
      const s = st.sFrom + (st.sTo - st.sFrom) * t
      const point = pointAtPath(st.path, st.cum, s)
      st.curLat = point[0]
      st.curLng = point[1]
      if (marker) {
        marker.setPosition([point[1], point[0]])
      }
      return
    }

    st.curLat = st.fromLat + (st.toLat - st.fromLat) * t
    st.curLng = st.fromLng + (st.toLng - st.fromLng) * t
    if (marker) {
      marker.setPosition([st.curLng, st.curLat])
    }
  })
}

function distanceKm(lat1, lng1, lat2, lng2) {
  const R = 6371
  const rad = Math.PI / 180
  const dLat = (lat2 - lat1) * rad
  const dLng = (lng2 - lng1) * rad
  const a =
    Math.sin(dLat / 2) * Math.sin(dLat / 2) +
    Math.cos(lat1 * rad) * Math.cos(lat2 * rad) * Math.sin(dLng / 2) * Math.sin(dLng / 2)
  return 2 * R * Math.asin(Math.min(1, Math.sqrt(a)))
}

/** 窗口尺寸变化时让地图重新铺满容器 */
function handleResize() {
  if (map) {
    map.resize()
  }
}

/** 工厂点位只加载一次，用 CircleMarker 以支撑 300+ 个点位的渲染性能 */
async function loadFactories() {
  const response = await fetch('/factories')
  if (!response.ok) {
    throw new Error(`工厂接口 HTTP ${response.status}`)
  }
  const list = await response.json()
  factories.value = list

  const markers = []
  list.forEach((f) => {
    const lng = Number(f.factoryLongitude)
    const lat = Number(f.factoryLatitude)
    if (!Number.isFinite(lng) || !Number.isFinite(lat)) {
      return
    }
    factoryById.set(f.id, { id: f.id, name: f.factoryName, lng, lat })
    const dot = new AMap.CircleMarker({
      center: [lng, lat],
      radius: 4,
      strokeColor: '#1d6fd8',
      strokeWeight: 1,
      fillColor: '#409EFF',
      fillOpacity: 0.7,
      zIndex: 50,
    })
    dot.setMap(map)
    markers.push(dot)
  })

  factoryMarkers.push(...markers)

  // 初始视野自适应到全部工厂，否则 zoom=12 只能看到十来个点位
  if (markers.length && map) {
    map.setFitView(markers, false, [60, 60, 60, 60], 11)
  }
}

async function loadState() {
  try {
    const snapshot = await fetchState()
    const prevTick = state.tick
    state.running = snapshot.running
    state.tick = snapshot.tick
    state.simMinutes = snapshot.simMinutes
    state.tickSeconds = snapshot.tickSeconds || 5
    state.vehicles = snapshot.vehicles || []
    state.pendingMissions = snapshot.pendingMissions || []
    state.activeMissions = snapshot.activeMissions || []
    state.doneMissions = snapshot.doneMissions || []
    errorMsg.value = ''

    // 轮次回退或刚重置时，车辆应该直接吸到新位置，不要慢悠悠地飘过去
    const snap = snapshot.tick <= 1 || snapshot.tick < prevTick
    renderVehicles(state.vehicles, state.activeMissions, snap)
    planTaskRoutes(state.activeMissions)
    planPickupRoutes(state.vehicles, state.activeMissions)
    renderLegs(state.vehicles, state.activeMissions)
  } catch (e) {
    errorMsg.value = `获取仿真状态失败：${e.message}（后端是否已启动？）`
  }
}

function renderVehicles(vehicles, missions, snap = false) {
  const alive = new Set()
  const now = performance.now()
  const animMs = Math.max(600, (state.tickSeconds || 5) * 1000)
  const missionByCar = new Map()
  missions.forEach((m) => {
    if (m.carId) {
      missionByCar.set(m.carId, m)
    }
  })

  vehicles.forEach((v) => {
    const lng = Number(v.currentLongitude)
    const lat = Number(v.currentLatitude)
    if (!Number.isFinite(lng) || !Number.isFinite(lat)) {
      return
    }
    alive.add(v.id)
    const color = STATUS_COLOR[v.currentAction] || '#909399'
    const html = `<div class="veh-marker" style="border-color:${color};color:${color}">🚚 ${v.id}</div>`

    const marker = vehicleMarkers.get(v.id)
    if (!marker) {
      const created = new AMap.Marker({
        position: [lng, lat],
        content: html,
        offset: new AMap.Pixel(-24, -14),
        zIndex: 300,
      })
      created.setMap(map)
      vehicleMarkers.set(v.id, created)
      markerState.set(v.id, {
        curLat: lat,
        curLng: lng,
        fromLat: lat,
        fromLng: lng,
        toLat: lat,
        toLng: lng,
        path: null,
        cum: null,
        sFrom: 0,
        sTo: 0,
        start: now,
        duration: 0,
      })
      return
    }

    marker.setContent(html)

    const st = markerState.get(v.id)
    if (!st) {
      return
    }
    const moved = distanceKm(st.curLat, st.curLng, lat, lng)
    if (moved < 0.005) {
      // 这一轮车辆没动（装货/卸货/等待），保持当前动画即可
      return
    }

    // 有当前路段的折线就沿折线按弧长插值，避免在拐弯处走直线弦
    const path = legPathOf(v, missionByCar.get(v.id))
    if (path && path.length > 1) {
      const cum = pathCumulative(path)
      st.path = path
      st.cum = cum
      st.sFrom = projectOnPath(path, cum, st.curLat, st.curLng)
      st.sTo = projectOnPath(path, cum, lat, lng)
    } else {
      st.path = null
      st.cum = null
      st.fromLat = st.curLat
      st.fromLng = st.curLng
      st.toLat = lat
      st.toLng = lng
    }

    st.start = now
    // 重置/瞬移或手动指定 snap 时直接吸附，不做动画
    st.duration = snap || moved > SNAP_KM ? 0 : animMs
    if (st.duration === 0) {
      st.curLat = lat
      st.curLng = lng
      st.sFrom = st.sTo
      marker.setPosition([lng, lat])
    }
  })

  vehicleMarkers.forEach((marker, id) => {
    if (!alive.has(id)) {
      marker.setMap(null)
      vehicleMarkers.delete(id)
      markerState.delete(id)
    }
  })
}

/** 车辆当前行驶段的折线：接单段用规划结果，运货段用路线折线 */
function legPathOf(vehicle, mission) {
  if (!mission) {
    return null
  }
  const action = Number(vehicle.currentAction)
  if (action === 2) {
    return pickupPaths.get(`${vehicle.id}:${mission.id}`) || null
  }
  if (action === 4 && mission.routeId) {
    return routeCache.get(mission.routeId) || null
  }
  return null
}

/** 折线各点到起点的累计弧长（km） */
function pathCumulative(points) {
  const cum = [0]
  for (let i = 1; i < points.length; i++) {
    cum.push(
      cum[i - 1] +
        distanceKm(points[i - 1][1], points[i - 1][0], points[i][1], points[i][0]),
    )
  }
  return cum
}

/** 把坐标投影到折线上，返回从起点算起的弧长（km） */
function projectOnPath(points, cum, lat, lng) {
  let bestDistance = Infinity
  let bestSeg = 1
  let bestT = 0
  const kLng = 111.32 * Math.cos((lat * Math.PI) / 180)

  for (let i = 1; i < points.length; i++) {
    const ax = (points[i - 1][0] - lng) * kLng
    const ay = (points[i - 1][1] - lat) * 110.574
    const bx = (points[i][0] - lng) * kLng
    const by = (points[i][1] - lat) * 110.574
    const dx = bx - ax
    const dy = by - ay
    const len2 = dx * dx + dy * dy
    let t = len2 === 0 ? 0 : -(ax * dx + ay * dy) / len2
    t = Math.max(0, Math.min(1, t))
    const d = Math.hypot(ax + t * dx, ay + t * dy)
    if (d < bestDistance) {
      bestDistance = d
      bestSeg = i
      bestT = t
    }
  }
  return cum[bestSeg - 1] + bestT * (cum[bestSeg] - cum[bestSeg - 1])
}

/** 折线上弧长 s 处的坐标，返回 [lat, lng] */
function pointAtPath(points, cum, s) {
  if (s <= 0) {
    return [points[0][1], points[0][0]]
  }
  for (let i = 1; i < points.length; i++) {
    if (s <= cum[i]) {
      const segLength = cum[i] - cum[i - 1]
      const t = segLength <= 0 ? 0 : (s - cum[i - 1]) / segLength
      return [
        points[i - 1][1] + (points[i][1] - points[i - 1][1]) * t,
        points[i - 1][0] + (points[i][0] - points[i - 1][0]) * t,
      ]
    }
  }
  const last = points[points.length - 1]
  return [last[1], last[0]]
}

/** 任务路线只用于规划几何（供后端推进车辆），不再在地图上画线 */
function planTaskRoutes(missions) {
  missions.forEach((m) => {
    const from = factoryById.get(m.factoryId)
    const to = factoryById.get(m.destFactoryId)
    if (!from || !to || !m.routeId) {
      return
    }
    ensureRouteGeometry(m.routeId, from, to).catch(() => {})
  })
}

/** 接单行驶段也要走真实道路：规划「车辆当前位置 → 装货工厂」并回写给后端 */
function planPickupRoutes(vehicles, missions) {
  const missionByCar = new Map()
  missions.forEach((m) => {
    if (m.carId) {
      missionByCar.set(m.carId, m)
    }
  })

  vehicles.forEach((v) => {
    // 2 = 接单行驶
    if (Number(v.currentAction) !== 2) {
      return
    }
    const mission = missionByCar.get(v.id)
    const target = mission ? factoryById.get(mission.factoryId) : null
    if (!mission || !target) {
      return
    }
    const key = `${v.id}:${mission.id}`
    if (pickupPlanned.has(key)) {
      return
    }
    const from = { lng: Number(v.currentLongitude), lat: Number(v.currentLatitude) }
    if (!Number.isFinite(from.lng) || !Number.isFinite(from.lat)) {
      return
    }
    pickupPlanned.add(key)
    planRoute(from, target)
      .then((points) => {
        if (points && points.length > 1) {
          pickupPaths.set(key, points)
          return updatePickupPoints(v.id, mission.id, points)
        }
        return null
      })
      .catch(() => {})
  })
}

/**
 * 高亮每辆车当前正在行驶的那一段路线（接单段 / 运货段），带方向箭头。
 * 没拿到真实折线时先用直线占位，下一轮拿到后再替换。
 */
function renderLegs(vehicles, missions) {
  const missionByCar = new Map()
  missions.forEach((m) => {
    if (m.carId) {
      missionByCar.set(m.carId, m)
    }
  })

  const alive = new Set()
  vehicles.forEach((v) => {
    const action = Number(v.currentAction)
    const mission = missionByCar.get(v.id)
    let path = null

    if (action === 2 && mission) {
      // 接单行驶：车辆当前位置 → 装货工厂
      const planned = pickupPaths.get(`${v.id}:${mission.id}`)
      const origin = factoryById.get(mission.factoryId)
      if (planned && planned.length > 1) {
        path = planned
      } else if (origin) {
        path = [
          [Number(v.currentLongitude), Number(v.currentLatitude)],
          [origin.lng, origin.lat],
        ]
      }
    } else if (action === 4 && mission && mission.routeId) {
      // 运货行驶：沿任务路线的折线
      const cached = routeCache.get(mission.routeId)
      const from = factoryById.get(mission.factoryId)
      const to = factoryById.get(mission.destFactoryId)
      if (cached && cached.length > 1) {
        path = cached
      } else if (from && to) {
        path = [
          [from.lng, from.lat],
          [to.lng, to.lat],
        ]
      }
    }

    if (!path) {
      return
    }
    alive.add(v.id)

    const line = legLines.get(v.id)
    if (!line) {
      const created = new AMap.Polyline({
        path,
        strokeColor: '#1d6fd8',
        strokeWeight: 5,
        strokeOpacity: 0.55,
        lineJoin: 'round',
        showDir: true,
        zIndex: 90,
      })
      created.setMap(map)
      legLines.set(v.id, created)
    } else {
      line.setPath(path)
    }
  })

  legLines.forEach((line, id) => {
    if (!alive.has(id)) {
      line.setMap(null)
      legLines.delete(id)
    }
  })
}

/**
 * 取路线几何：已经是导航路线就直接用库里的折线；
 * 还是合成路线就用 JS API 规划一次真实道路，并把折线回写给后端，
 * 这样后续所有走这条线的车辆都会贴着真实道路行驶。
 */
function ensureRouteGeometry(routeId, from, to) {
  if (routeCache.has(routeId)) {
    return Promise.resolve(routeCache.get(routeId))
  }
  if (routeLoading.has(routeId)) {
    return routeLoading.get(routeId)
  }

  const task = (async () => {
    try {
      const detail = await fetchRoute(routeId).catch(() => null)
      if (detail && detail.roadType === NAVIGATION_ROAD_TYPE) {
        const points = await fetchRoutePoints(routeId).catch(() => [])
        routeCache.set(routeId, points)
        return points
      }

      const planned = await planRoute(from, to)
      if (planned && planned.length > 1) {
        try {
          await updateRoutePoints(routeId, planned)
          routeCache.set(routeId, planned)
          return planned
        } catch (e) {
          // 回写失败就退回到后端已有的合成折线
        }
      }

      const fallback = await fetchRoutePoints(routeId).catch(() => [])
      routeCache.set(routeId, fallback)
      return fallback.length > 1 ? fallback : null
    } finally {
      routeLoading.delete(routeId)
    }
  })()

  routeLoading.set(routeId, task)
  return task
}

/** 用高德 JS API（与地图同一个 key）规划驾车路线，返回折线点 */
function planRoute(from, to) {
  return new Promise((resolve) => {
    if (!AMap) {
      resolve(null)
      return
    }
    try {
      const driving = new AMap.Driving({ policy: 0 })
      driving.search(
        new AMap.LngLat(from.lng, from.lat),
        new AMap.LngLat(to.lng, to.lat),
        (status, result) => {
          if (status !== 'complete' || !result || !result.routes || !result.routes.length) {
            resolve(null)
            return
          }
          const points = []
          result.routes[0].steps.forEach((step) => {
            ;(step.path || []).forEach((p) => {
              const lng = typeof p.getLng === 'function' ? p.getLng() : p.lng
              const lat = typeof p.getLat === 'function' ? p.getLat() : p.lat
              const last = points[points.length - 1]
              if (!last || last[0] !== lng || last[1] !== lat) {
                points.push([lng, lat])
              }
            })
          })
          resolve(points.length > 1 ? points : null)
        },
      )
    } catch (e) {
      resolve(null)
    }
  })
}

async function run(action) {
  try {
    await action()
    await loadState()
    errorMsg.value = ''
  } catch (e) {
    errorMsg.value = e.message
  }
}

/** 打开页面即自动开始仿真，工具栏只保留「暂停 / 继续」 */
async function ensureAutoStart() {
  try {
    await startSim()
    await loadState()
  } catch (e) {
    errorMsg.value = `自动启动失败：${e.message}`
  }
}

/** 重置后立刻重新开始，避免用户还要再点一次继续 */
async function resetAndStart() {
  try {
    await resetSim()
    await startSim()
    await loadState()
  } catch (e) {
    errorMsg.value = e.message
  }
}

/** 用高德 POI 检索抓取成都的真实工厂/园区坐标，导入后端 */
async function importFactoriesFromAmap() {
  if (!AMap || importing.value) {
    return
  }
  importing.value = true
  notice.value = ''
  try {
    const items = new Map()
    const keywords = ['工厂', '物流园', '仓库', '产业园']
    const search = new AMap.PlaceSearch({ city: '成都', citylimit: true, pageSize: 50, extensions: 'base' })

    // JS API 2.0 的 PlaceSearch 没有 gotoPage，翻页要先 setPageIndex 再 search
    const pageable = typeof search.setPageIndex === 'function'
    const pages = pageable ? 4 : 1

    for (const keyword of keywords) {
      for (let page = 1; page <= pages; page++) {
        if (page > 1) {
          search.setPageIndex(page)
        }
        const result = await new Promise((resolve) => {
          const handler = (status, res) => resolve(status === 'complete' ? res : null)
          search.search(keyword, handler)
        })
        const pois = (result && result.poiList && result.poiList.pois) || []
        if (!pois.length) {
          break
        }
        pois.forEach((p) => {
          const lng = p.location && p.location.lng
          const lat = p.location && p.location.lat
          if (!lng || !lat || !p.name) {
            return
          }
          const key = `${p.name}@${lng.toFixed(4)},${lat.toFixed(4)}`
          if (items.has(key)) {
            return
          }
          items.set(key, {
            factoryName: String(p.name).slice(0, 50),
            address: String(p.address || '').slice(0, 100),
            phone: String(p.tel || '').slice(0, 20),
            factoryLongitude: lng,
            factoryLatitude: lat,
          })
        })
      }
    }

    const list = [...items.values()]
    if (!list.length) {
      notice.value = '没有检索到工厂点位（可能是配额或城市限制）'
      return
    }
    const response = await fetch('/factories/import', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(list),
    })
    const text = await response.text()
    notice.value = `${text}（检索到 ${list.length} 个点位）`
    await reloadFactories()
  } catch (e) {
    notice.value = `抓取失败：${e.message}`
  } finally {
    importing.value = false
    setTimeout(() => {
      notice.value = ''
    }, 6000)
  }
}

/** 重新加载工厂点位（先清掉旧标记） */
async function reloadFactories() {
  factoryMarkers.forEach((marker) => marker.setMap(null))
  factoryMarkers.length = 0
  factoryById.clear()
  await loadFactories()
}
</script>

<style>
.sim-page {
  position: relative;
  width: 100vw;
  height: 100vh;
  overflow: hidden;
}

#map-container {
  width: 100%;
  height: 100%;
  background: #eef1f5;
}

/* 车辆标记（由 AMap 直接插入 DOM，不能用 scoped） */
.veh-marker {
  padding: 2px 8px;
  border: 2px solid #409eff;
  border-radius: 12px;
  background: #fff;
  font-size: 12px;
  font-weight: 600;
  white-space: nowrap;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
}

.toolbar {
  position: absolute;
  top: 16px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 14px;
  background: rgba(255, 255, 255, 0.96);
  border-radius: 10px;
  box-shadow: 0 6px 18px rgba(0, 0, 0, 0.16);
  font-size: 13px;
  color: #303133;
  z-index: 30;
}

.toolbar .item b {
  color: #409eff;
  font-size: 15px;
  margin: 0 2px;
}

.badge {
  padding: 1px 8px;
  border-radius: 10px;
  font-size: 12px;
}

.badge.on {
  background: #f0f9eb;
  color: #67c23a;
}

.badge.off {
  background: #f4f4f5;
  color: #909399;
}

.toolbar button {
  padding: 4px 12px;
  border: 1px solid #409eff;
  border-radius: 6px;
  background: #409eff;
  color: #fff;
  font-size: 12px;
  cursor: pointer;
}

.toolbar button.ghost {
  background: #fff;
  color: #409eff;
}

.toolbar button:disabled {
  border-color: #dcdfe6;
  background: #f5f7fa;
  color: #c0c4cc;
  cursor: not-allowed;
}

.toast {
  position: absolute;
  bottom: 24px;
  left: 50%;
  transform: translateX(-50%);
  padding: 8px 16px;
  border-radius: 8px;
  background: rgba(245, 108, 108, 0.95);
  color: #fff;
  font-size: 13px;
  z-index: 40;
}

.toast.info {
  background: rgba(103, 194, 58, 0.95);
}
</style>
