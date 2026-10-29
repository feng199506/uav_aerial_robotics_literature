# 无人机与空中机器人资料收集：最终报告

检索日：2026-10-30。目录：`/root/uav_aerial_robotics_literature/`。本轮只收集整理，未安装软件、未编译固件、未启动仿真、未连接无人机。完成后停止，不扩展下一类别。

## 1. 成功数量（仅已核验全文/整包）

| 类型 | 已核验 | 目标 | 判定 |
|---|---|---|---|
| 完整教材/参考书/专著 | 16 | 15–25 | 达标（下限附近） |
| 大学官方课程或讲义包 | 11 | 10–15 | 达标（其中 MIT VNAV 2020 课程包与 2023 公开笔记为同一课不同年份，独立课程序列约 10 门） |
| 论文/综述/学术教程 | 56 | 约 50 | 达标 |
| 官方工具文档 | 19 份文件 / 约 11 套不重复工具 | 8–12 套 | 达标；HTML 与 git 源并行，不按 19 套计 |
| 实验/参考项目 | 15 | 10–15 | 达标 |
| **全库去重条目** | **117** | — | — |

- 新下载：106  
- 已有复用（核验后复制，原件未移动）：11（控制/优化/估计教材与 MIT 16.30、EE363、Kalman、16.322、Underactuated 笔记）

失败 18（教材缺口、短预印本、标题核验失败等），待办 0。HTML 镜像事后核验通过的已计入 docs 文件数。

## 2. 论文近三年

- 窗口：2023-10-30 … 2026-10-30  
- 近三年：52 / 56 = **92.9%**（目标 ≥ 85%）  
- 年份：2026 年 44，2025 年 5，2024 年 2，2023 年 1；窗口外经典 4  

经典及理由：

| 编号 | 年 | 理由 |
|---|---|---|
| UA03P01 Lee et al. | 2010 | SE(3) 几何跟踪，后续几何飞控标准引用 |
| UA03P03 Faessler et al. | 2018 | 含旋翼阻力的微分平坦，高速跟踪基线 |
| UA04P01 Qin et al. VINS-Mono | 2018 | 单目 VIO 开源基线 |
| UA05P00 Xu et al. FAST-LIO2 | 2022 | 激光惯性里程计，GNSS 弱环境常用 |

未计入：Mellinger 2011（无合法全文）；Mahony 2012 CSM（无合法全文）；OpenVINS 与 “Learning high-speed flight in the wild” PDF 标题核验失败。

仿真论文未标为实飞；作者“实验/实飞”仅转述正文声明。

## 3. 覆盖情况

**基础理论：** NASA 气动、MIT 动力学/气动课、四元数与李群、惯性导航。缺：Beard/McLain 系统教材、Diebel 姿态讲义、Soler 航空航天导论 PDF。

**建模与飞控：** Beuchat N-rotor（多旋翼主教材）、16.333 与 Stengel 固定翼、Feedback Systems、LQR/MPC/凸优化、Underactuated 四旋翼章、近三年 MPC/CBF/倾转旋翼论文。VTOL 以倾转桨/倾转旋翼论文为主，缺少完整 VTOL 专著。

**估计与感知：** Barfoot、Särkkä、因子图、16.322、VNAV、TU Graz 相机无人机、FAST-LIVO2、主动 SLAM。室内/弱 GNSS 有方法覆盖；本库无自有实飞数据。

**规划与学习：** LaValle、近三年规划/探索/VLN 论文、Brunton、学习综述。Mellinger 原文缺失，用 VNAV 笔记与 Faessler 衔接。

**软件与仿真：** PX4 v1.17 指南源 + 部分 HTML（达配额）、ArduPilot wiki 源 + 部分 HTML、QGroundControl 与 Mission Planner HTML、MAVLink 指南/XML/HTML、MAVSDK、MAVROS（兼容路径）、Gazebo 与 JSBSim 文档源及 HTML、pyulog。ROS 2 默认路径按 PX4 文档记为 uXRCE-DDS。

**部署与民用：** 故障/风险/AAM 综述、FAA Part 107 学习指南（美国）。缺 EASA 规章全文、缺测绘专著 Eisenbeiss。

**多机：** 近三年去中心化规划、SwarmNxt、Crazyswarm2、MRS 文档；聚焦民用。

## 4. 失败、残缺、待核实

见 [download_failures_cn.csv](download_failures_cn.csv)。要点：

- 教材：Beard 作者 PDF、Soler、Diebel、Eisenbeiss、EASA Easy Access Rules  
- 课程：D-FaLL 习题页 404；UNR 课程页未解析到 PDF；CVUT 讲义仓库不可匿名克隆；BYU 幻灯片仓库无讲义  
- 论文：若干短预印本不足 6 页、错误 arXiv 号标题不匹配  
- HTML 镜像：PX4、ArduPilot 达配额但仍通过“部分镜像”核验（197 / 541 页 HTML）；QGC、Mission Planner、MAVLink、MAVSDK、PX4 ROS 2、Gazebo Harmonic、JSBSim 镜像完整通过  

ETH Research Collection 对部分 IP 显示反爬；Beuchat 全文改经 bitstream API 取得。

## 5. 实际路径与续跑

```
/root/uav_aerial_robotics_literature/
```

```bash
cd /root/uav_aerial_robotics_literature
python3 -I scripts/fetch_en.py status
python3 -I scripts/fetch_en.py run --retry-failed
python3 -I scripts/build_catalog_en.py
```

状态在 `state/items/<ID>.json`。已 `ok` 的条目默认不重下。

## 6. 使用注意

- 官方文档版本以 catalog 中的 git 提交号和检索日为准。  
- 美国 FAA 指南不可当作欧盟/中国运行要求。  
- 参考项目未复现；不得把仓库存在写成“已跑通”。  
- 未做 SHA256 整库回扫（按任务要求）。
