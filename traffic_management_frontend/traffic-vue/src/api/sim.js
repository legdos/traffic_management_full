/**
 * 仿真相关接口封装。所有路径都是相对路径，由 vite.config.js 的代理转发到后端。
 */

async function readJson(response) {
  if (!response.ok) {
    throw new Error(`HTTP ${response.status}`)
  }
  return response.json()
}

async function readText(response) {
  if (!response.ok) {
    throw new Error(`HTTP ${response.status}`)
  }
  return response.text()
}

/** 一次拿到轮次、车辆、三组任务 */
export function fetchState() {
  return fetch('/sim/state').then(readJson)
}

/** 某条路线的折线点 [[lng,lat],...] */
export function fetchRoutePoints(routeId) {
  return fetch(`/routes/${routeId}/points`).then(readJson)
}

/** 路线详情，用 roadType 判断是否已经是导航路线 */
export function fetchRoute(routeId) {
  return fetch(`/routes/${routeId}`).then(readJson)
}

/** 把高德 JS API 规划出的真实道路折线回写给后端 */
export function updateRoutePoints(routeId, points) {
  return fetch(`/routes/${routeId}/points`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(points),
  }).then(readText)
}

/** 回写「车辆当前位置 → 装货工厂」的取货段真实折线 */
export function updatePickupPoints(vehicleId, missionId, points) {
  return fetch(`/sim/pickup/${vehicleId}/${missionId}/points`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(points),
  }).then(readText)
}

export function startSim() {
  return fetch('/sim/start', { method: 'POST' }).then(readText)
}

export function stopSim() {
  return fetch('/sim/stop', { method: 'POST' }).then(readText)
}

/** 清空任务、车辆回到空闲 */
export function resetSim() {
  return fetch('/sim/reset', { method: 'POST' }).then(readText)
}
