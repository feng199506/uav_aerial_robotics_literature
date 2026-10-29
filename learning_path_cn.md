# 学习路线（仅关联已核验本地资料）

总顺序：数学与飞行基础 → 动力学 → 经典飞控 → 状态估计与传感器融合 → 感知导航 → 规划与自主任务 → 仿真测试 → 集成部署 → 民用应用。

下列路径都指向本库已下载条目。先修不足时回到 01/03 的控制教材，不要跳到学习飞控或实机日志。本轮不运行仿真、不飞行。

## 0. 共同基础

1. NASA SP-367《Introduction to the Aerodynamics of Flight》（UA01B01）：大气、翼型、螺旋桨/旋翼、坐标系。
2. MIT 16.07 Dynamics（UA01C01）+ MIT 16.100 Aerodynamics（UA01C02）：刚体、旋转坐标系、固定翼气动。
3. Joan Solà《Quaternion kinematics for the error-state KF》（UA01B04）与《A micro Lie theory》（UA01B05）：飞控姿态与 VIO 的旋转语言。
4. Woodman《An introduction to inertial navigation》（UA01B06）：IMU 与捷联惯性。
5. Åström & Murray《Feedback Systems》（UA03B01，已有复用）：PID 与环路，后面所有飞控的先修。

## 1. 飞控与状态估计路线

**目标：** 能读懂多旋翼级联 PID / 几何控制 / LQR / MPC，并能把 IMU、GNSS、视觉惯性接到状态估计。

| 阶段 | 资料 | 说明 |
|---|---|---|
| 多旋翼模型与本科控制 | Beuchat《N-rotor vehicles》（UA02B02） | CC BY 完整讲义：N 旋翼动力学、PID/LQR、估计 |
| 固定翼稳定与自动驾驶仪 | MIT 16.333（UA03C01）+ Princeton MAE 331（UA02C03） | 纵横向模态、自动驾驶仪；固定翼主线 |
| 反馈与 LQR | MIT 16.30（UA03C02）+ Stanford EE363（UA03C05） | 航空反馈课 + LQR/Kalman 课件 |
| 几何与最优 | Lee 2010 SE(3) 跟踪（UA03P01）+ Liberzon 最优控制（UA03B04）+ Boyd 凸优化（UA03B03） | 经典几何控制；轨迹优化数学 |
| 欠驱动与四旋翼专章 | Tedrake Underactuated notes（UA03B05） | 含平面/三维四旋翼 |
| MPC | Rawlings MPC（UA03B02）+ 近三年四旋翼 MPC 论文（UA03P05–P08） | 理论教材 + 竞速/降落/稳定性论文 |
| 滤波 | Särkkä（UA04B02）+ UCCS ECE5550（UA04C01）+ MIT 16.322（UA04C02） | 从贝叶斯滤波到航空随机估计 |
| 惯性与 VIO | Barfoot（UA04B01）+ Dellaert/Kaess 因子图（UA04B03）+ VINS-Mono（UA04P01）+ FAST-LIO2（UA05P00） | 估计教材接到开源实现论文 |
| 阻力与高速 | Faessler 2018 微分平坦（UA03P03） | 高速跟踪时必须读的气动修正 |

**输出自评：** 能画出多旋翼级联结构，写出误差状态四元数更新，能说明 PX4 多旋翼位置环与几何控制器的差别（对照 UA09T10 文档，不改固件）。

## 2. 感知、导航与自主规划路线

**目标：** GNSS 不可用或弱纹理环境下的定位、建图、轨迹与避障。

| 阶段 | 资料 | 说明 |
|---|---|---|
| 视觉导航课 | MIT 16.485 VNAV OCW 2020（UA05C01） | 完整课程包：四旋翼、轨迹、VIO、SLAM |
| 更新讲义 | VNAV 2023 notes（UA05C02） | 几何控制与轨迹优化笔记，作为 2020 包的补丁而非另一门课 |
| 相机无人机 | TU Graz Camera Drones 2024（UA05C03） | 传感器融合、三维、航线；奥地利法规一讲勿当全球规则 |
| 规划算法 | LaValle《Planning Algorithms》（UA06B01） | 采样规划与微分约束 |
| 激光/视觉里程计 | FAST-LIVO2（UA05P01）、LiDAR 空中综述（UA05P02）、RAVEN 主动 SLAM（UA05P03） | 近三年感知 |
| 杂乱环境规划 | NMPP（UA06P02）、TransNav（UA06P03）、CBF 导航（UA03P11） | 规划与安全约束 |
| 参考实现（只读） | OpenVINS（UA04X01）、VINS-Fusion（UA05X01，ROS1 历史）、FAST-LIO（UA05X02）、Fast-Planner（UA06X02）、ETH 多项式轨迹（UA06X01，ROS1 历史） | 见实践索引；不运行 |

**输出自评：** 能说明单目 VIO 与激光惯性的传感器假设，以及最小 snap / MPC 规划各自约束什么。

## 3. 无人机 AI 与学习控制路线

**目标：** 分清哪些结果来自仿真、哪些来自作者报告的实飞；把学习方法接到经典飞控，而不是替换它。

| 阶段 | 资料 | 说明 |
|---|---|---|
| 数据驱动先修 | Brunton《Data-Driven Science and Engineering》（UA07B01） | DMD、稀疏识别、数据驱动控制 |
| 综述 | 2024 多旋翼学习算法综述（UA07P02）+ VLA 空中综述（UA07P08） | 先建立地图再读单篇 |
| 竞速与对比 | Song 等 MPC vs RL（UA03P04） | 作者报告实飞；本库未复现 |
| 可微仿真 / 世界模型 | DiffDreamer（UA07P04）、穿狭缝可微仿真（UA07P03） | **仿真结果，不得写成实飞** |
| 视觉语言 | AeroDASH（UA07P06）、SatNav 基准（UA07P07） | VLN/VLA；基准论文不等于系统评测完成 |
| 参考平台 | Agilicious（UA07X01）、gym-pybullet-drones（UA10X02） | 只读许可证与说明 |

**输出自评：** 能指出一篇学习飞控论文的训练域、评价域、是否 sim-to-real，以及与级联 PID/MPC 如何分工。

## 4. 民用应用集成路线

**目标：** 把飞控—感知—规划接到测绘、巡检、农业、环境监测，并分清地区运行规则。

| 阶段 | 资料 | 说明 |
|---|---|---|
| 美国远程驾驶员 | FAA-G-8082-22（UA12B02） | **仅美国 Part 107**；空域、气象、人的因素 |
| 巡检综述 | UAV 基础设施巡检（UA12P01） | 文献综述，不是某次任务评测 |
| 农业/三维 | UAV3DCrop（UA12P05）、语音引导采收（UA12P04） | 农田三维与作业 |
| 环境/交通 | 甲烷多机规划（UA08P04）、交通监测综述（UA12P03）、信天翁无人机调查（UA12P06） | 民用遥感 |
| 多机作业 | SwarmNxt（UA08P03）、双机吊运（UA08P05）、去中心化轨迹（UA08P01） | 民用协同，非武器 |
| 可靠性 | UAS 风险综述（UA11P03）、故障容错（UA11P01）、AAM/eVTOL 安全综述（UA11P04） | 部署约束 |
| 欧盟规章 | EASA Easy Access Rules **未取得全文**（见缺口） | 不得用美国指南代替欧盟要求 |

**输出自评：** 能为一类民用任务列出传感器、定位条件、适用地区规则来源，并标明本库未做飞行验证。

## 与仿真、软件的衔接

读完对应理论后，用 [tools_map_cn.md](tools_map_cn.md) 对照 PX4 v1.17 / ArduPilot / MAVLink / ROS 2，用 [practice_index_cn.md](practice_index_cn.md) 选只读项目。仿真与日志工具在 10；不要把 SITL 截图当成实机性能。
