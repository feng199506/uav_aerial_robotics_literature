# 检索与执行日志

检索日：2026-10-30。只使用合法公开来源：arXiv、MIT OCW、大学课程页、项目 GitHub、NASA NTRS、FAA、ETH Research Collection API、作者公开 PDF。不绕过登录或付费墙。

## 论文

- 窗口：`submittedDate:[202310300000 TO 202610302359]`
- arXiv 检索词（节选）：`aerial robot/quadrotor/multirotor`；`UAV + control/navigation/SLAM/planning/inspection`；`survey/review`；`swarm`；`MPC`；应用类 `inspection/agriculture/air quality`。
- 排序：submittedDate 降序，因此近端 2026 篇较多；另用手选 2024–2025 综述与 FAST-LIVO2、Pegasus 等补覆盖。
- 排除：一般地面机器人、纯通信/6G 中仅把 UAV 当节点、军事对抗/欺骗为主且无民用方法贡献、普通航拍无飞控或感知方法。
- 速率：arXiv ≥ 4 s；曾遇 429，停止追加检索。
- 经典（窗口外，有公开全文才计）：Lee 2010；Faessler 2018；Qin VINS-Mono 2018；Xu FAST-LIO2 2022。
- 未计入经典：Mellinger 2011（IEEE 付费，作者 PDF 404）；Mahony 2012 CSM（无合法全文）；OpenVINS 2020 与 Loquercio 2021（PDF 首页无法提取标题词，核验失败）。

## 教材与课程

- 优先：作者/大学/OCW/CC 许可全文。
- 已有复用：Barfoot、Särkkä、Åström、Rawlings、Boyd、Liberzon、Tedrake、Brunton、MIT 16.30、EE363、ECE5550、MIT 16.322（核验后复制，未移动原件）。
- 失败后改源：Beuchat 课程页 PDF 404 → ETH bitstream `7016770e-…/content`（CC BY 4.0）。
- 仍缺：Beard/McLain 作者课程 PDF（站点 403/仓库无文件）；Soler 教材无直接 PDF；Diebel 2006；Eisenbeiss 学位论文（ETH 站点对抓取 IP 限制）；EASA Easy Access Rules 直链 404。
- BYU `mavsim_public` 无讲义幻灯片，仅 README，课程条目 UA02C02 不计。
- VNAV 2023 讲义按实际 `vnav.mit.edu/material/*.pdf` 文件名下载（初版文件名猜测 404）。

## 软件与实践

- PX4 以 **v1.17 稳定版** 用户指南源仓库为准，不以 `docs.px4.io/main` 为推荐。
- ROS 2：文档写明 uXRCE-DDS 为 PX4 v1.17 默认；MAVROS 标兼容路径。
- 仿真：Gazebo 文档源（仍维护）；JSBSim 文档；AirSim/RotorS 不收为当前推荐。
- Git 稀疏检出 + 打包时丢弃大二进制/权重大于阈值的文件；不执行 hook。
- HTML 全站镜像（完成后）：QGC、Mission Planner、MAVLink、MAVSDK、PX4 ROS 2、Gazebo Harmonic、JSBSim 完整通过。PX4 v1.17 约 191 MB / 197 页 HTML（达配额，标「部分」）；ArduPilot 约 171 MB / 541 页 HTML（达配额，标「部分」）。git 文档源与 HTML 为同一工具的两种离线格式，套数按工具计。

## 执行脚本

- `scripts/seed_core_en.py` / `seed_papers2_en.py`：种子
- `scripts/fetch_en.py`：下载核验（断点 `state/items/`）
- `scripts/search_papers_en.py`：arXiv 发现
- `scripts/build_catalog_en.py`：目录与进度
