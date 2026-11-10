# 交通管理系统（traffic_management）

前后端分离的**货运调度仿真系统**：车辆按马尔科夫状态机概率转移，任务按空闲缺口生成，行驶路线来自真实道路规划。

- 仓库：<https://github.com/legdos/traffic_management_full>（前后端放在同一个仓库）
- 后端：`traffic_management_backend`，Spring Boot 4 + MyBatis + MariaDB，端口 **8080**
- 前端：`traffic_management_frontend/traffic-vue`，Vue 3 + Vite + 高德地图 JS API，端口 **5173**

## 目录结构

```
traffic_management/
├── .gitignore
├── README.md
├── trafficdata.sql                      # 建库脚本（表结构 + 初始数据）
├── mission_sim_upgrade.sql              # mission 表的仿真字段升级脚本
├── traffic_management_backend/          # Spring Boot 后端
│   ├── pom.xml
│   ├── mvnw / mvnw.cmd                  # Maven Wrapper，无需本机安装 Maven
│   └── src/main/
│       ├── java/com/example/traffic_management/
│       │   ├── controller/              # REST 接口
│       │   ├── service/ + service/impl/ # 业务逻辑（含马表仿真、路线服务）
│       │   ├── mapper/                  # MyBatis Mapper 接口
│       │   ├── entity/                  # 实体
│       │   ├── enums/                   # 车辆状态机、任务状态常量
│       │   ├── config/                  # 仿真参数
│       │   ├── dto/                     # /sim/state 的返回体
│       │   └── util/                    # 地理计算、折线算法、高德客户端
│       └── resources/
│           ├── application.yaml         # 端口 8080 + 数据库连接 + sim.* 参数
│           └── mapper/*.xml             # MyBatis SQL
└── traffic_management_frontend/
    └── traffic-vue/                     # Vue 3 + Vite 工程（实际启动目录）
        ├── package.json
        ├── vite.config.js               # 代理到 http://localhost:8080
        └── src/
```

## 一、环境要求

| 组件 | 版本要求 | 说明 |
| --- | --- | --- |
| JDK | 17 及以上 | 后端 `pom.xml` 中 `java.version=17`；实测 JDK 26 也能编译运行 |
| Node.js | ^22.18.0 或 >=24.12.0 | 见 `traffic-vue/package.json` 的 `engines` |
| MySQL / MariaDB | 5.7+ / 10.x | 使用 XAMPP 自带的 MySQL 即可 |
| Maven | 不需要 | 用 `mvnw.cmd`；首次运行会把 Maven 3.9.16 下载到 `~/.m2/wrapper` |

## 二、准备数据库

1. 打开 XAMPP 控制面板，启动 **MySQL**（监听 `localhost:3306`）。
2. 用 Navicat 连接 `localhost:3306`，用户名 `root`，密码为空。
3. 新建数据库 `traffic`（字符集 `utf8mb4`）。
4. 在该库上右键「运行 SQL 文件」，选择根目录的 `trafficdata.sql` 导入。
5. 如果 `mission` 表缺少仿真字段，再执行一次 `mission_sim_upgrade.sql`（幂等，可重复执行）。

导入后应包含这些表：`action`、`factory`、`goods`、`mission`、`need`、`poi`、`route`、`vehicle`。

后端连接信息写在 `traffic_management_backend/src/main/resources/application.yaml`：

```yaml
url: jdbc:mysql://localhost:3306/traffic?...
username: root
password:
```

## 三、启动后端（端口 8080）

方式一：命令行

```powershell
cd D:\traffic_management\traffic_management_backend
.\mvnw.cmd spring-boot:run
```

方式二：IDEA 打开 `traffic_management_backend` 目录（以 Maven 项目导入），运行 `TrafficManagementApplication`（详细配置见第五章）。

启动成功的标志：控制台出现 `Tomcat started on port 8080` 以及 `马表仿真服务已就绪`。

验证：浏览器访问 <http://localhost:8080/vehicles> 应返回 JSON 数组。

## 四、启动前端（端口 5173）

```powershell
cd D:\traffic_management\traffic_management_frontend\traffic-vue
npm install          # 首次运行；node_modules 已存在时可跳过
npm run dev
```

浏览器打开 <http://localhost:5173> 即可看到地图与车辆列表。**页面加载后会自动开始仿真**，工具栏只保留「暂停 / 继续 / 重置 / 抓取真实工厂」。

> 前端所有请求都写成 `/factories`、`/vehicles`、`/sim/...` 这样的相对路径，
> 由 `vite.config.js` 的 `server.proxy` 转发到 `http://localhost:8080`。
> 因此后端地址变化时只改 `vite.config.js` 里的 `BACKEND_TARGET` 一处即可。

## 五、IDE 配置（IDEA / VS Code）

> `.idea` 目录被 `.gitignore` 排除，换电脑后需要按本节重新配置一次；`.vscode` 只提交了扩展推荐。

### 5.1 IDEA 启动后端

| 依赖项 | 要求 | 说明 |
| --- | --- | --- |
| JDK | **17 及以上**（推荐 17 / 21） | 对应 `pom.xml` 的 `java.version=17` |
| Maven | **不需要单独安装** | 项目自带 `mvnw`，IDEA 直接用 Maven 面板导入即可 |
| Lombok | IDEA 已内置该插件，**无需单独安装** | 但**必须开启注解处理**，否则 `getXxx()/setXxx()` 满屏报红 |
| 数据库工具 | 可选 | IDEA 自带 Database，可连 `localhost:3306/traffic`（root / 空密码）以便查看任务表 |

**首次打开步骤：**

1. `File → Open`，选择 **`traffic_management_backend`** 目录（含 `pom.xml` 的那一层）。
   ⚠️ 不要打开仓库根目录——根目录没有 `pom.xml`，IDEA 会提示「未定义模块 JDK」。
2. 右下角弹出 `Load Maven Project` 时点击加载；若没有弹出，打开右侧 **Maven** 面板 → `Reload All Maven Projects`。
3. `File → Project Structure`（`Ctrl+Alt+Shift+S`）→ **Project** → SDK 选择 JDK 17 及以上；
   再到 **Modules** → 选中模块 → **Dependencies** → `Module SDK` 选 `Project SDK`。
4. `Settings → Build, Execution, Deployment → Compiler → Annotation Processors`
   → 勾选 **Enable annotation processing**（Lombok 生成 getter/setter 依赖它）。
5. 运行 `com.example.traffic_management.TrafficManagementApplication`（Spring Boot 配置，端口 8080）。

**验证**：控制台出现 `Tomcat started on port 8080` 和 `马表仿真服务已就绪`；
浏览器访问 <http://localhost:8080/sim/state> 应返回 JSON。

### 5.2 VS Code 打开前端

| 依赖项 | 要求 | 说明 |
| --- | --- | --- |
| Node.js | **^22.18.0 或 ≥24.12.0** | 由 `package.json` 的 `engines` 约束 |
| 扩展 **Vue - Official** | **必装** | 扩展 ID `Vue.volar`（原 Volar），提供 `.vue` 语法高亮、模板检查、组件跳转 |

`traffic-vue/.vscode/extensions.json` 已经推荐了 `Vue.volar`，打开该目录时 VS Code 会提示安装。

**可选扩展**（不装也能跑）：

| 扩展 | 用途 |
| --- | --- |
| `esbenp.prettier-vscode` | 代码格式化 |
| `vscjava.vscode-java-pack` | 如果也想在 VS Code 里阅读后端 Java 代码 |
| `vmware.vscode-spring-boot` | Spring Boot 配置提示、`application.yaml` 补全 |

**打开方式**：直接打开 **`traffic_management_frontend\traffic-vue`** 目录（`package.json` 所在层）。
如果打开的是仓库根目录，VS Code 不会读取 `traffic-vue/.vscode` 里的扩展推荐。

**启动**：

```powershell
cd D:\traffic_management\traffic_management_frontend\traffic-vue
npm install      # 首次
npm run dev      # http://localhost:5173
```

> 提示：后端建议用 IDEA（Java 生态支持完整），前端建议用 VS Code（Vue 工具链轻量），
> 两者可以同时开着，互不影响。

## 六、接口一览

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| GET | `/factories`、`/factories/{id}` | 工厂列表 / 详情 |
| POST | `/factories`、`PUT /factories` | 新增 / 更新工厂 |
| POST | `/factories/import` | 按 `[{factoryName, address, phone, factoryLatitude, factoryLongitude}]` 批量导入工厂（同名同坐标自动跳过） |
| POST | `/factories/{id}/generate-need?material=木头` | 为工厂生成需求 |
| GET | `/vehicles`、`/vehicles/active`、`/vehicles/{id}` | 车辆列表 / 未删除车辆 / 详情 |
| POST/PUT/DELETE | `/vehicles` | 新增 / 修改 / 删除车辆 |
| GET | `/needs`、`/needs/{id}` | 需求列表 / 详情 |
| GET | `/missions` | 任务列表 |
| POST | `/missions/assign/{needId}`、`/missions/batch-assign` | 指派任务 |
| POST | `/sim/start`、`/sim/stop`、`/sim/reset` | 启动 / 暂停 / 重置仿真 |
| GET | `/sim/state` | 仿真实时快照：轮次、车辆、待接单/进行中/已完成任务（含 `remainMinutes` 真实剩余） |
| GET | `/routes/{id}`、`/routes/{id}/points` | 路线详情 / 折线点 `[[lng,lat],...]` |
| PUT | `/routes/{id}/points` | 前端规划出真实道路后回写折线，后端重算长度并标记「导航路线」 |
| GET/PUT | `/sim/pickup/{vehicleId}/{missionId}/points` | 接单段（车辆 → 装货点）折线的读取 / 回写 |

## 七、整理目录时修正的路径相关配置

1. `traffic_management_backend/src/main/resources/application.yaml`
   - 显式声明 `server.port: 8080`，与前端代理目标对齐；
   - 数据库地址固定为 `localhost:3306/traffic`，补充 `allowPublicKeyRetrieval`、`useUnicode` 等参数。
2. `traffic_management_frontend/traffic-vue/vite.config.js`
   - `@` 别名改为 `fileURLToPath(new URL('./src', import.meta.url))`：原来的 `URL.pathname` 在 Windows 上会得到 `/D:/...` 这种非法路径，移动目录后极易报「找不到模块」；
   - 后端地址提取为 `BACKEND_TARGET` 常量，并补齐 `/needs`、`/missions`、`/routes` 代理。
3. `mapper` 相关（目录移动后重新核对数据库新结构时发现的必然报错）
   - `VehicleMapper.xml` 的 `update` 语句补全逗号、修正 `#{isDeleted}` 括号，并把新增列 `remaining_time`、`distance_to_pickup`、`transport_distance` 纳入查询；
   - `findFreeVehicles` 原来用 `CurrentAction = '空闲'` 比较 int 列，改为 `currentAction = 1`；
   - `FactoryMapper.updateNeedId` 补上 `@Param`，否则 `generate-need` 接口会抛「参数找不到」。
4. Maven / Vite 均未使用绝对路径，仓库整体可以随意移动，不受盘符影响。

## 八、马表仿真（状态机 + 任务驱动）

### 8.1 每轮循环做什么

默认 **5 秒一轮，一轮代表现实 5 分钟**：

1. 按「空闲车辆数 − 待接单数」的缺口补充运输任务（每轮上限 `tasks-per-tick`，默认 5 条），随机起点/终点工厂、随机货物类型；
2. 逐车推进：状态没结束就扣减剩余时间、沿路线折线前进；状态结束时按马尔科夫表抽样下一个状态；
3. 新状态是「接单行驶」时，原子抢占距离装货点最近的待接单任务；
4. 全部落库，前端每 1 秒轮询 `/sim/state`，并在两次坐标之间做插值动画。

车辆状态存在 `vehicle.currentAction / remaining_time / 经纬度`，任务状态存在 `mission.status`，
二者通过 `mission.car_id` 关联。

### 8.2 状态转换表

| 从 \ 到 | 接单行驶 | 装货 | 运货行驶 | 卸货 | 停留等待 | 空闲 |
| --- | --- | --- | --- | --- | --- | --- |
| 接单行驶 | 0.05 | 0.90 | 0.00 | 0.00 | 0.05 | 0.00 |
| 装货 | 0.00 | 0.02 | 0.95 | 0.02 | 0.01 | 0.00 |
| 运货行驶 | 0.00 | 0.00 | 0.00 | 0.98 | 0.02 | 0.00 |
| 卸货 | 0.00 | 0.00 | 0.00 | 0.00 | 0.02 | 0.98 |
| 停留等待 | 0.10 | 0.05 | 0.05 | 0.00 | 0.20 | 0.60 |
| 空闲 | 0.90 | 0.00 | 0.00 | 0.00 | 0.10 | 0.00 |

抽样方式：`Random.nextInt(100) + 1` 得 1~100，按行概率累加划分区间。
以「接单行驶」为例：1–5 继续接单行驶、6–95 转装货、96–100 转停留等待。
矩阵常量在 `enums/VehicleState.java`，枚举声明顺序必须与矩阵行列一致。

### 8.3 时长规则（统一 60 km/h，即 1 km = 1 分钟）

| 状态 | 时长 |
| --- | --- |
| 接单行驶 | 车辆当前位置 → 起点工厂的距离（km） |
| 装货 | 30 分钟 |
| 运货行驶 | 起点工厂 → 终点工厂的距离（km） |
| 卸货 | 30 分钟 |
| 停留等待 | 5 分钟 |
| 空闲 | 0（下一轮立即重新抽样） |

抽到的状态若是接单/装货/运货/卸货，但车上既无任务、待接单池也为空，则降级为「空闲」。

### 8.4 可调参数

`application.yaml` 的 `sim.*`：

| 参数 | 默认 | 说明 |
| --- | --- | --- |
| `tick-seconds` | 5 | 每轮的真实间隔（秒），调小可加速演示 |
| `minutes-per-tick` | 5 | 一轮代表现实多少分钟 |
| `speed-kmh` | 60 | 统一车速 |
| `loading-minutes` / `unloading-minutes` | 30 / 30 | 装卸货耗时 |
| `waiting-minutes` | 5 | 停留等待耗时 |
| `task-probability` | 0.9 | 生成任务时的成功概率 |
| `tasks-per-tick` | 5 | 每轮最多新增几条任务；实际按「空闲车数 − 待接单数」的缺口生成 |
| `max-pending-tasks` | 50 | 待接单任务上限，防止无人接单时无限堆积 |
| `amap-web-key` | 空 | 高德「Web服务」key；留空则用合成折线，填了就走真实驾车路径 |

### 8.5 数据库变更

`mission` 表新增 5 列（脚本见根目录 `mission_sim_upgrade.sql`，已在当前库执行过）：

`goods_type`、`dest_factory_id`、`distance_km`、`total_minutes`、`elapsed_minutes`

任务状态流转：`待接单` → `接单中` → `装货中` → `运输中` → `卸货中` → `已完成`。
`mission.remainMinutes` 是**非数据库字段**，由 `/sim/state` 按当前状态实时估算后下发。

### 8.6 前端结构

| 文件 | 作用 |
| --- | --- |
| `src/api/sim.js` | 仿真接口封装（状态轮询、路线回写、取货路线回写） |
| `src/components/MapView.vue` | 地图、车辆标记、当前行驶段高亮（带方向箭头）、1 秒轮询 + 插值动画、顶部控制条 |
| `src/components/VehiclePanel.vue` | 左栏车辆卡片（状态、本状态剩余、任务剩余与进度条） |
| `src/components/TaskPanel.vue` | 右栏任务看板（待接单 / 进行中 / 已完成） |

### 8.7 路线实体（route / poi）

车辆**不走两点直线**，而是沿路线折线行驶：

- 每生成一条任务，就按「起点工厂 → 终点工厂」查/建一条 `route` 记录，折线点存 `keyPoint`
  （JSON 数组 `[[lng,lat],...]`）；任务的 `route_id` 指向它。
- `route.startPoint / endPoint` 引用 `poi.id`（形如 `F864`）。`poi` 表按工厂生成，
  新增工厂时后端会自动补一条（`INSERT IGNORE`）。
- **几何来源可切换**：
  - 配置了 `sim.amap-web-key`（必须是高德控制台里「**Web服务**」类型的 key，JS API 的 key 会返回 `USERKEY_PLAT_NOMATCH`）→ 后端直接调驾车路径规划；
  - 否则先由 `PolylineUtil` 合成折线兜底（弯曲系数约 1.05~1.10），前端用**同一把 JS API key** 调 `AMap.Driving` 规划真实道路，再通过
    `PUT /routes/{id}/points` 回写，后端重算长度并标记为「导航路线」。
- 车辆**沿折线推进**：每个 tick 先把当前位置投影到折线上求得弧长，再前进 5km（60km/h × 5min）。
  用投影而不是记进度索引，所以重启后仅凭数据库里的经纬度就能恢复位置。
- 接单段（车辆当前位置 → 装货工厂）同样走路线，但起点是实时位置，按「车辆+任务」缓存在内存、不落库；
  离开接单行驶状态时清掉。前端通过 `PUT /sim/pickup/{vehicleId}/{missionId}/points` 回写真实折线。
- 前端不再为每条任务画线，只**高亮车辆当前正在行驶的那一段**（接单段或运货段），带方向箭头。

### 8.8 性能与一致性

- **性能**：50 辆车时每轮约 100 条 UPDATE。优化前每轮约 1.5 秒，优化后计算耗时约 100ms：
  整轮放进一个事务（消除上百次 fsync）、进行中任务批量加载、路线折线内存缓存、无变化车辆跳过回写。
- **一致性**：任务状态守恒，任意时刻 `总数 = 待接单 + 进行中 + 已完成`；
  `待接单` 必无车辆、`进行中` 必有车辆、无悬空 `car_id`。抢单使用
  `UPDATE ... WHERE status='待接单'` 条件更新，保证一车一单。

## 九、常见问题

- **前端请求 404 / 500**：先确认后端是否在 8080 启动，且终端里 `TrafficManagementApplication` 无异常。
- **后端启动报 `Communications link failure`**：MySQL 没启动，或端口不是 3306；到 XAMPP 面板点 Start。
- **端口被占用**：后端改 `application.yaml` 的 `server.port` 同时要改 `vite.config.js` 的 `BACKEND_TARGET`；前端改 `vite.config.js` 的 `server.port`。
- **导入 SQL 报外键错误**：脚本已带 `SET FOREIGN_KEY_CHECKS=0`，请整份执行，不要只选中部分语句。
- **IDEA 里打开根目录报「未定义模块 JDK」**：不要打开仓库根目录，打开 `traffic_management_backend`（含 `pom.xml` 的那层）。
- **IDEA 里 Lombok 报红**：`Settings → Compiler → Annotation Processors` 勾选 Enable annotation processing。
- **VS Code 里 `.vue` 没高亮/没提示**：安装 `Vue - Official`（`Vue.volar`）扩展，并确认打开的是 `traffic-vue` 目录。
- **`git push` 报 `Failed to connect ... over proxy`**：检查本机代理端口，执行
  `git config --global http.proxy http://127.0.0.1:7890`（端口按实际代理改）。
- **命令行导入的中文变成 `?`**：`mysql.exe -e "..."` 会按 ANSI 代码页传参，中文会丢；
  改用 SQL 文件执行，或用 `CONVERT(0x... USING utf8mb4)` 十六进制字面量。
