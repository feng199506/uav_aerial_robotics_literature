# 无人机与空中机器人文献库

本目录只收集整理公开资料，不安装软件、不编译固件、不启动仿真、不连接或操作无人机。属于按类别的系统资料库，不宣称穷尽。

- 检索执行日：2026-10-30
- 论文时间窗口：首次公开日期 2023-10-30 至 2026-10-30。窗口外经典论文单列。
- 计数规则：只计已完整保存在本地且核验通过的条目。摘要、试读、失败、待核验不计。

## 总进度

| 类型 | 已核验 | 目标 | 新下载 | 已有复用 | 状态 |
|---|---|---|---|---|---|
| 教材/参考书/专著 | 16 | 15–25 | 8 | 8 | 达标 |
| 大学官方课程或讲义 | 11 | 10–15 | 8 | 3 | 达标 |
| 研究论文/综述/学术教程 | 56 | 约 50 | 56 | 0 | 达标 |
| 官方工具文档或系统教程 | 19（约 11 套不重复工具；其余为 HTML 镜像与 git 源并行） | 8–12 套 | 19 | 0 | 达标；同工具双格式不另凑数 |
| 公开实验/参考项目/实践案例 | 15 | 10–15 | 15 | 0 | 达标 |
| **全库去重条目** | **117** | — | **106** | **11** | — |

论文近三年：52 / 56（92.9%）。窗口外经典 4 篇（几何控制、微分平坦、VINS-Mono、FAST-LIO2）。

重点覆盖多旋翼；固定翼与垂直起降通过 MIT 16.333/16.07/16.100、Princeton MAE 331、JSBSim、倾转旋翼论文补充。FAA 学习指南仅适用于美国 Part 107，不是全球规则。

## 目录结构

| 路径 | 内容 |
|---|---|
| [catalog_cn.csv](catalog_cn.csv) | 全库已核验目录 |
| [progress_cn.csv](progress_cn.csv) | 分类型进度 |
| [download_failures_cn.csv](download_failures_cn.csv) | 失败与待办（不计） |
| [search_log_cn.md](search_log_cn.md) | 检索与筛选记录 |
| [learning_path_cn.md](learning_path_cn.md) | 学习路线（关联已下载资料） |
| [tools_map_cn.md](tools_map_cn.md) | 飞控/仿真/中间件对照 |
| [practice_index_cn.md](practice_index_cn.md) | 实践索引（本轮不执行） |
| [final_report_cn.md](final_report_cn.md) | 本轮最终报告 |
| `01_foundations/` … `12_civil_applications/` | 十二个子方向 |
| `papers/` | 已核验论文 PDF（去重） |
| `scripts/` | 种子、下载与编目脚本 |
| `state/items/` | 断点状态 |

十二个子方向：

| 编号 | 目录 | 主题 |
|---|---|---|
| 01 | `01_foundations` | 飞行原理、刚体、旋转、传感器与嵌入式基础 |
| 02 | `02_modeling_dynamics` | 多旋翼/固定翼/VTOL 建模与辨识 |
| 03 | `03_flight_control` | 姿态到轨迹：PID、LQR、MPC、非线性与学习辅助 |
| 04 | `04_state_estimation` | IMU/GNSS/视觉惯性与滤波 |
| 05 | `05_perception_localization_mapping` | 视觉/激光感知、SLAM、弱 GNSS 导航 |
| 06 | `06_planning_autonomy` | 轨迹规划、避障、探索与自主任务 |
| 07 | `07_learning_aerial_robotics` | RL、模仿、仿真到现实、视觉语言导航 |
| 08 | `08_multi_uav` | 多机协作（民用） |
| 09 | `09_flight_software_communications` | PX4/ArduPilot、MAVLink、ROS 2、地面站 |
| 10 | `10_simulation_testing` | SITL/HIL、传感器仿真、日志评测 |
| 11 | `11_reliability_deployment` | 故障、容错、运行约束 |
| 12 | `12_civil_applications` | 测绘、巡检、农业、环境监测、搜救 |

## 核验标准（摘要）

- PDF：`%PDF-` 头、pypdf 可解析、标题词匹配、正文可提取。
- 课程包：官方 zip 或成套讲义 PDF；仅 README 的仓库不计。
- 文档：官方 git 文档源或 HTML 镜像；记录版本/提交号与保存范围。
- 参考项目：许可证或 README、稀疏检出、丢弃固件二进制与大权重；**不执行源码**。

## 续跑

```bash
cd /root/uav_aerial_robotics_literature
python3 -I scripts/fetch_en.py run --retry-failed
python3 -I scripts/build_catalog_en.py
```

本轮完成后停止，不自动扩展下一类别。
