# 飞控与工具对照（检索日 2026-10-30）

只记录本库已保存的公开文档/源码说明。不安装、不刷写、不连接飞控。旧项目标为历史参考，不作为“当前推荐”。

## 当前主栈（民用科研/工程常见）

| 用途 | 当前公开主线 | 本库资料 | 版本/提交 | 兼容关系 |
|---|---|---|---|---|
| 飞控 | **PX4 Autopilot 稳定版 v1.17** | UA09T10 指南源 + UA09T01 部分 HTML（197 页，达配额） | git 提交 / 检索日镜像 | 多旋翼/固定翼/VTOL；不以 `main` 为推荐版本 |
| 飞控（并行生态） | **ArduPilot** Copter/Plane | UA09T11 wiki 源 + UA09T02 部分 HTML（541 页，达配额） | git 提交 / 检索日镜像 | 与 PX4 并列，不是同一套参数/模式 |
| 地面站 | **QGroundControl** | UA09T03 HTML + UA09T12 仓库 docs | 检索日镜像 / git 提交见 catalog | 通过 MAVLink 连 PX4 或 ArduPilot；不保存安装包 |
| 地面站（ArduPilot 常用） | **Mission Planner** | UA09T04 HTML | 检索日 `ardupilot.org/planner` | 与 ArduPilot wiki 配套 |
| 消息 | **MAVLink v2** | UA09T05 HTML + UA09T09 指南源 + UA09T14 XML | 检索日 / git | PX4 v1.17 默认 MAVLink v2；v1 为兼容 |
| 伴随计算机 SDK | **MAVSDK** | UA09T06 HTML + UA09T13 仓库文档 | 检索日 / git | 官方 offboard API；SITL UDP 14540 为常见约定（以 PX4 文档为准） |
| ROS 2 默认中间件（PX4） | **uXRCE-DDS / px4_msgs** | UA09T07 HTML + UA09T10 `en/ros2/` | v1.17 指南 | **PX4 v1.17 对 ROS 2 的当前推荐路径** |
| ROS 桥（兼容） | **MAVROS** | UA09T08 | 提交见 catalog | 仍维护，但是 PX4 文档中的兼容/历史 ROS 路径，不是 v1.17 默认 |
| 仿真（多旋翼 SITL） | **Gazebo（Harmonic；PX4 1.17 另列更新发行版）** | UA10T01 HTML + UA10T04 文档源 | 检索日 / git | Gazebo Classic / RotorS **不作为当前推荐** |
| 仿真（固定翼 FDM） | **JSBSim** | UA10T02 HTML + UA10T05 文档源 | 检索日 / git | ArduPilot SITL 常用 FDM 之一 |
| 日志 | **pyulog + Flight Review** | UA10T03、实践 UA10X04 | 提交见 catalog | 解析 ULog；不代替实飞评测 |

PX4 / ArduPilot HTML 为配额内部分镜像（离线可读，范围见 catalog 的 `完整性/备注`）。套数按工具计，不把 HTML 与 git 源算成两套。

## 历史或非默认（可参考，不推荐当 2026 默认栈）

| 项目 | 状态（本库核实） | 资料 |
|---|---|---|
| MAVROS 作为 PX4↔ROS 2 默认 | 否；PX4 v1.17 默认 uXRCE-DDS | UA09T08 |
| VINS-Fusion / ETH mav_trajectory_generation / rpg_mpc | ROS1 时代参考实现，算法仍常被引用 | UA05X01、UA06X01、UA03X01 |
| Microsoft AirSim | 上游已归档趋势，本库不收为当前仿真推荐 | 未下载 |
| ETH RotorS | ROS1/Gazebo Classic，历史 | 未下载 |
| PX4 `main` 文档 | 开发枝 | 未镜像 |

## 感知与规划参考实现（不是飞控固件）

| 项目 | 角色 | 本库 | 注意 |
|---|---|---|---|
| OpenVINS | 开源 VIO | UA04X01 | 代码公开；本轮不跑、不下数据集 |
| FAST-LIO | 激光惯性里程计 | UA05X02 | GNSS 弱环境常用基线之一 |
| Fast-Planner | 高速避障规划 | UA06X02 | 学术实现 |
| Crazyswarm2 | 多 Crazyflie + ROS 2 | UA08X01 | 不连接实机、不编译固件 |
| CTU MRS 系统 | 多旋翼实验栈文档稀疏 | UA08X02 | 仅文档/结构，不全量克隆 |

## 组件关系（简图）

```
传感器/执行器 → 飞控（PX4 v1.17 或 ArduPilot）
                 ├─ MAVLink v2 → QGC / Mission Planner / MAVSDK
                 └─ ROS 2：PX4 推荐 uXRCE-DDS；MAVROS 为兼容层
SITL：Gazebo（多旋翼常见）或 JSBSim（固定翼常见）→ 同一 MAVLink/ROS 接口
日志：ULog → pyulog / Flight Review（只分析已有日志，本轮无飞行日志）
```

## 未下载（有意）

- 任何 `.px4` / `.apj` / `.bin` 固件二进制
- 仿真模型网格、大型数据集、权重
- 付费标准（ASTM/ISO 等）全文
