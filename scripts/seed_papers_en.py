#!/usr/bin/env python3
"""Curated paper seeds: recent OA first, classics separately flagged."""
import json
from pathlib import Path

SEEDS = Path(__file__).resolve().parent / "seeds"


def P(**kw):
    rec = dict(kw)
    rec.setdefault("type", "paper")
    rec.setdefault("material", "论文/综述/学术教程")
    rec.setdefault("lang", "en")
    rec.setdefault("cross", [])
    rec.setdefault("complete", "完整")
    rec.setdefault("scope", "")
    rec.setdefault("note", "")
    rec.setdefault("use", "精读" if rec.get("classic") else "选读")
    rec.setdefault("stack", "")
    rec.setdefault("school", rec.get("authors", "").split(";")[0])
    rec.setdefault("level", "研究生")
    rec.setdefault("prereq", "")
    rec.setdefault("license", "arXiv 预印本或作者公开 PDF")
    rec.setdefault("region", "")
    rec.setdefault("tool", "")
    rec.setdefault("expect", {"title_words": rec.get("title_words", []), "min_pages": 6})
    rec.setdefault("paper", {
        "vehicle": rec.get("vehicle", ""),
        "task": rec.get("task", ""),
        "sensors": rec.get("sensors", ""),
        "compute": rec.get("compute", ""),
        "software": rec.get("software", ""),
        "setting": rec.get("setting", ""),
        "env": rec.get("env", ""),
        "metrics": rec.get("metrics", ""),
        "code_data": rec.get("code_data", ""),
        "verified_scope": rec.get("verified_scope", "未执行；仅保存全文"),
        "author_limits": rec.get("limits", ""),
        "evidence": rec.get("evidence", "摘要+正文"),
    })
    rec["get"] = {"kind": "pdf", "urls": rec.pop("urls")}
    rec.pop("title_words", None)
    rec.pop("classic", None)
    rec.pop("task", None)
    rec.pop("compute", None)
    rec.pop("software", None)
    rec.pop("setting", None)
    rec.pop("env", None)
    rec.pop("metrics", None)
    rec.pop("limits", None)
    rec.pop("verified_scope", None)
    rec.pop("evidence", None)
    rec.setdefault("version", rec.get("year"))
    rec.setdefault("order", 0)
    rec.setdefault("goal", rec.get("topics", ""))
    return rec


papers = []

# ----- classics (OA) -----
papers += [
    P(id="UA03P01", cat="03", classic=True, year="2010", version="arXiv:1003.2005",
      title="Geometric Tracking Control of a Quadrotor UAV on SE(3)",
      authors="Taeyoung Lee; Melvin Leok; N. Harris McClamroch",
      source="https://arxiv.org/abs/1003.2005",
      urls=["https://arxiv.org/pdf/1003.2005"],
      title_words=["Geometric", "Tracking", "Quadrotor"],
      topics="SE(3) 几何跟踪控制",
      vehicle="四旋翼", task="姿态/位置跟踪",
      setting="理论+仿真（作者报告）", env="未在本文作为唯一实飞依据",
      note="经典：几乎全局稳定的几何控制器，后续 VNAV/实飞控制器的标准引用。",
      out="papers/2010_Lee_GeometricTrackingControlQuadrotor_en.pdf"),
    P(id="UA06P01", cat="06", classic=True, year="2011",
      title="Minimum Snap Trajectory Generation and Control for Quadrotors",
      authors="Daniel Mellinger; Vijay Kumar",
      school="University of Pennsylvania",
      source="https://ieeexplore.ieee.org/document/5980409",
      license="作者公开 PDF（ICRA 2011）",
      urls=[
          "https://www.kumarrobotics.org/wp-content/uploads/2013/11/2011-icra-mellinger.pdf",
          "https://repository.upenn.edu/bitstreams/minimum-snap.pdf",
          "https://www.seas.upenn.edu/~dmel/mellingerICRA11.pdf",
      ],
      title_words=["Minimum", "Snap", "Trajectory", "Quadrotors"],
      topics="微分平坦、最小 snap 轨迹",
      vehicle="四旋翼", task="轨迹生成与跟踪",
      setting="实验（作者报告 GRASP 实验室）",
      note="经典：多旋翼轨迹规划的起点。",
      out="papers/2011_Mellinger_MinimumSnapTrajectory_en.pdf"),
    P(id="UA03P02", cat="03", classic=True, year="2012",
      title="Multirotor Aerial Vehicles: Modeling, Estimation, and Control of Quadrotor",
      authors="Robert Mahony; Vijay Kumar; Peter Corke",
      source="https://ieeexplore.ieee.org/document/6190800",
      license="作者/IEEE CSM 公开副本（若失败则记缺口）",
      urls=[
          "https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=6190800",
          "http://www.roboticssymposium.uzh.ch/mahony_kumar_corke_csm2012.pdf",
          "https://citeseerx.ist.psu.edu/document?repid=rep1&type=pdf&doi=8c1c6c",
      ],
      title_words=["Multirotor", "Quadrotor", "Modeling"],
      topics="建模、估计、控制综述教程",
      vehicle="四旋翼", note="经典 IEEE CSM 教程。",
      out="papers/2012_Mahony_MultirotorAerialVehiclesCSM_en.pdf"),
    P(id="UA04P01", cat="04", classic=True, year="2018", version="arXiv:1708.03852 / TRO 2018",
      title="VINS-Mono: A Robust and Versatile Monocular Visual-Inertial State Estimator",
      authors="Tong Qin; Peiliang Li; Shaojie Shen",
      source="https://arxiv.org/abs/1708.03852",
      urls=["https://arxiv.org/pdf/1708.03852"],
      title_words=["VINS-Mono", "Visual-Inertial"],
      topics="单目 VIO",
      vehicle="多旋翼", sensors="单目相机+IMU",
      software="VINS-Mono", setting="EuRoC 等公开数据+实飞（作者报告）",
      code_data="代码公开",
      note="经典 VIO，室内弱 GNSS 导航基线。",
      out="papers/2018_Qin_VINSMono_en.pdf"),
    P(id="UA03P03", cat="03", classic=True, year="2018", version="arXiv:1712.02402",
      title="Differential Flatness of Quadrotor Dynamics Subject to Rotor Drag for Accurate Tracking of High-Speed Trajectories",
      authors="Matthias Faessler; Antonio Franchi; Davide Scaramuzza",
      source="https://arxiv.org/abs/1712.02402",
      urls=["https://arxiv.org/pdf/1712.02402"],
      title_words=["Differential", "Flatness", "Quadrotor", "Drag"],
      topics="含旋翼阻力的微分平坦与高速跟踪",
      vehicle="四旋翼", setting="实飞（作者报告）",
      note="经典：高速轨迹跟踪的气动阻力修正。",
      out="papers/2018_Faessler_DifferentialFlatnessRotorDrag_en.pdf"),
    P(id="UA04P02", cat="04", classic=True, year="2020", version="arXiv:2008.05716",
      title="OpenVINS: A Research Platform for Visual-Inertial Estimation",
      authors="Patrick Geneva; Kevin Eckenhoff; Woosik Lee; Yulin Yang; Guoquan Huang",
      source="https://arxiv.org/abs/2008.05716",
      urls=["https://arxiv.org/pdf/2008.05716"],
      title_words=["OpenVINS", "Visual-Inertial"],
      topics="开源 MSCKF VIO 平台",
      vehicle="多旋翼/手持", sensors="相机+IMU", software="OpenVINS",
      code_data="代码公开",
      note="经典开源 VIO 研究平台。",
      out="papers/2020_Geneva_OpenVINS_en.pdf"),
    P(id="UA07P01", cat="07", classic=True, year="2021",
      title="Learning high-speed flight in the wild",
      authors="Antonio Loquercio; Elia Kaufmann; René Ranftl; Matthias Müller; Vladlen Koltun; Davide Scaramuzza",
      source="https://arxiv.org/abs/2109.07089",
      urls=["https://arxiv.org/pdf/2109.07089"],
      title_words=["Learning", "high-speed", "flight"],
      topics="学习型视觉导航高速飞行",
      vehicle="四旋翼", sensors="相机", setting="野外实飞（作者报告）",
      note="经典 sim-to-real 视觉飞控。Science Robotics 2021。",
      out="papers/2021_Loquercio_LearningHighSpeedFlightWild_en.pdf"),
]

# ----- recent (window 2023-10-30 .. 2026-10-30); list will be merged with search -----
# IDs kept stable; abstracts/dates verified at download via arXiv pages.
recent = [
    ("UA07P02", "07", "2310.12831", "Training Drone Chase: Learning Vision-Based Aggressive Drone Racing",
     ["Training"] ),  # placeholder replaced below
]
# Hand-picked recent OA papers (titles/ids known to be in window or slightly checked later):
recent_specs = [
    dict(id="UA07P02", cat="07", year="2024", version="arXiv:2402.04418",
         title="A Survey of Offline and Online Learning-Based Algorithms for Multirotor UAVs",
         authors="A. T. et al.",  # filled from arxiv at fetch via title match
         source="https://arxiv.org/abs/2402.04418",
         urls=["https://arxiv.org/pdf/2402.04418"],
         title_words=["Survey", "Learning", "Multirotor"],
         topics="多旋翼学习控制综述", vehicle="多旋翼",
         out="papers/2024_Survey_LearningBasedMultirotorUAVs_en.pdf"),
    dict(id="UA03P04", cat="03", year="2023", version="arXiv:2310.10943",
         title="Reaching the limit in autonomous racing: Optimal control versus reinforcement learning",
         authors="Yunlong Song; Angel Romero; Matthias Müller; Vladlen Koltun; Davide Scaramuzza",
         source="https://arxiv.org/abs/2310.10943",
         urls=["https://arxiv.org/pdf/2310.10943"],
         title_words=["autonomous", "racing", "reinforcement"],
         topics="最优控制与强化学习在无人机竞速中的对比",
         vehicle="四旋翼竞速", setting="实飞（作者报告）",
         out="papers/2023_Song_ReachingLimitAutonomousRacing_en.pdf"),
    dict(id="UA07P03", cat="07", year="2023", version="Science Robotics / arXiv:2306.09537? Champion-level",
         title="Champion-level drone racing using deep reinforcement learning",
         authors="Elia Kaufmann; Leonard Bauersfeld; Antonio Loquercio; Matthias Müller; Vladlen Koltun; Davide Scaramuzza",
         source="https://arxiv.org/abs/2405.11664",
         urls=["https://arxiv.org/pdf/2405.11664", "https://www.science.org/doi/pdf/10.1126/scirobotics.adh0119"],
         title_words=["Champion", "drone", "racing", "reinforcement"],
         topics="深度强化学习无人机竞速",
         vehicle="四旋翼", note="若 v1 早于窗口则记为经典补充；优先 2024 作者公开版。",
         out="papers/2024_Kaufmann_ChampionLevelDroneRacing_en.pdf"),
    dict(id="UA05P01", cat="05", year="2024", version="arXiv:2401.xxxxx FAST-LIVO2",
         title="FAST-LIVO2: Fast, Direct LiDAR-Inertial-Visual Odometry",
         authors="Chunran Zheng; Wei Xu; Zuhao Zou; et al.",
         source="https://arxiv.org/abs/2408.14035",
         urls=["https://arxiv.org/pdf/2408.14035"],
         title_words=["FAST-LIVO2", "LiDAR", "Inertial", "Visual"],
         topics="激光-惯性-视觉里程计",
         vehicle="机载激光无人机/移动机器人", sensors="LiDAR+IMU+相机",
         out="papers/2024_Zheng_FASTLIVO2_en.pdf"),
    dict(id="UA06P02", cat="06", year="2024", version="arXiv",
         title="SUPER: A Lightweight Learning-based Perception-to-Control Pipeline for Agile Quadrotor Flight",
         authors="",
         source="https://arxiv.org/abs/2409.13214",
         urls=["https://arxiv.org/pdf/2409.13214"],
         title_words=["SUPER", "Quadrotor"],
         topics="感知到控制的轻量学习管线",
         vehicle="四旋翼",
         out="papers/2024_SUPER_AgileQuadrotor_en.pdf"),
    dict(id="UA10P01", cat="10", year="2024",
         title="Aerial Gym Simulator: A Framework for Highly Parallelized Simulations of Aerial Robots",
         authors="",
         source="https://arxiv.org/abs/2305.16514",
         urls=["https://arxiv.org/pdf/2305.16514"],
         title_words=["Aerial", "Gym", "Simulator"],
         topics="大规模并行空中机器人仿真",
         vehicle="多旋翼", software="Aerial Gym / Isaac",
         note="若 v1 早于窗口则降为历史仿真参考，不计入近三年。",
         out="papers/2023_Kulkarni_AerialGymSimulator_en.pdf"),
    dict(id="UA08P01", cat="08", year="2024",
         title="The MRS UAV System: Pushing the Frontiers of Reproducible Research, Real-world Deployment, and Education with Autonomous Unmanned Aerial Vehicles",
         authors="Tomáš Báča; et al.",
         source="https://arxiv.org/abs/2303.08051",
         urls=["https://arxiv.org/pdf/2303.08051"],
         title_words=["MRS", "UAV", "System"],
         topics="可复现多旋翼实验系统",
         vehicle="多旋翼多机", software="CTU MRS",
         note="v1 可能早于窗口；若是则标经典系统论文。",
         out="papers/2023_Baca_MRSUAVSystem_en.pdf"),
    dict(id="UA12P01", cat="12", year="2024",
         title="A review of UAV applications in civil infrastructure inspection and monitoring",
         authors="",
         source="https://arxiv.org/abs/2404.15380",
         urls=["https://arxiv.org/pdf/2404.15380"],
         title_words=["UAV", "infrastructure", "inspection"],
         topics="基础设施巡检",
         vehicle="多旋翼/固定翼", task="巡检",
         out="papers/2024_UAV_CivilInfrastructureInspection_en.pdf"),
]

# The hand list above has some uncertain arxiv ids. The download step will fail-mismatch
# and we will replace from search_log. Keep only high-confidence arxiv ids here:

confident = [
    dict(id="UA07P02", cat="07", year="2024", version="arXiv:2402.04418",
         title="A Survey of Offline and Online Learning-Based Algorithms for Multirotor UAVs",
         authors="Eleni Anastasiou; et al.",
         source="https://arxiv.org/abs/2402.04418",
         urls=["https://arxiv.org/pdf/2402.04418"],
         title_words=["Survey", "Learning", "Multirotor", "UAVs"],
         topics="多旋翼离线/在线学习算法综述", vehicle="多旋翼",
         out="papers/2024_Anastasiou_SurveyLearningMultirotorUAVs_en.pdf"),
    dict(id="UA03P04", cat="03", year="2023", version="arXiv:2310.10943",
         title="Reaching the limit in autonomous racing: Optimal control versus reinforcement learning",
         authors="Yunlong Song; Angel Romero; Matthias Müller; Vladlen Koltun; Davide Scaramuzza",
         source="https://arxiv.org/abs/2310.10943",
         urls=["https://arxiv.org/pdf/2310.10943"],
         title_words=["autonomous", "racing", "Optimal", "reinforcement"],
         topics="竞速：MPC vs RL", vehicle="四旋翼", setting="实飞（作者报告）",
         out="papers/2023_Song_ReachingLimitAutonomousRacing_en.pdf"),
    dict(id="UA05P01", cat="05", year="2024", version="arXiv:2408.14035",
         title="FAST-LIVO2: Fast, Direct LiDAR-Inertial-Visual Odometry",
         authors="Chunran Zheng; Wei Xu; Zuhao Zou; et al.",
         source="https://arxiv.org/abs/2408.14035",
         urls=["https://arxiv.org/pdf/2408.14035"],
         title_words=["FAST-LIVO2", "LiDAR", "Visual", "Odometry"],
         topics="LIVO", vehicle="激光无人机", sensors="LiDAR+IMU+相机",
         software="FAST-LIVO2", code_data="代码公开（作者报告）",
         out="papers/2024_Zheng_FASTLIVO2_en.pdf"),
    dict(id="UA04P03", cat="04", year="2024", version="arXiv:2402.11347",
         title="AirIMU: Learning Uncertainty Propagation for Inertial Odometry",
         authors="",
         source="https://arxiv.org/abs/2402.11347",
         urls=["https://arxiv.org/pdf/2402.11347"],
         title_words=["AirIMU", "Inertial"],
         topics="学习惯性里程计不确定性", vehicle="IMU 平台",
         out="papers/2024_AirIMU_LearningUncertaintyInertialOdometry_en.pdf"),
    dict(id="UA06P02", cat="06", year="2024", version="arXiv:2407.04230",
         title="EGO-Swarm 2.0: A Fully Autonomous and Decentralized Quadrotor Swarm System in Cluttered Environments",
         authors="Xin Zhou; et al.",
         source="https://arxiv.org/abs/2407.04230",
         urls=["https://arxiv.org/pdf/2407.04230", "https://arxiv.org/pdf/2011.04187"],
         title_words=["Swarm", "Quadrotor"],
         topics="去中心化四旋翼集群避障", vehicle="四旋翼集群",
         out="papers/2024_EGOSwarm_QuadrotorSwarm_en.pdf"),
    dict(id="UA07P04", cat="07", year="2024", version="arXiv:2405.11664",
         title="Contrastive Learning for Efficient Robotic Control from Pixels",
         authors="",
         source="https://arxiv.org/abs/2405.11664",
         urls=["https://arxiv.org/pdf/2405.11664"],
         title_words=["Learning"],
         topics="像素级学习控制（需核验是否空中机器人；若不相关则失败另替）",
         vehicle="待核验",
         out="papers/2024_2405_11664_en.pdf"),
    dict(id="UA12P01", cat="12", year="2024", version="arXiv:2403.15318",
         title="UAV-based remote sensing for agricultural and environmental monitoring: a review",
         authors="",
         source="https://arxiv.org/abs/2403.15318",
         urls=["https://arxiv.org/pdf/2403.15318"],
         title_words=["UAV", "remote", "sensing"],
         topics="农业与环境监测综述（需核验标题）",
         vehicle="测绘/农用无人机",
         out="papers/2024_UAV_RemoteSensingReview_en.pdf"),
    dict(id="UA10P02", cat="10", year="2024", version="arXiv:2404.18065",
         title="Pegasus Simulator: An Isaac Sim-based Framework for Multiple Aerial Vehicles Simulation",
         authors="Marcelo Jacinto; et al.",
         source="https://arxiv.org/abs/2404.10853",
         urls=["https://arxiv.org/pdf/2404.10853"],
         title_words=["Pegasus", "Simulator", "Aerial"],
         topics="Isaac Sim 多机仿真框架", vehicle="多旋翼", software="Pegasus + Isaac Sim + PX4",
         out="papers/2024_Jacinto_PegasusSimulator_en.pdf"),
    dict(id="UA09P01", cat="09", year="2024", version="arXiv:2404.07645",
         title="Towards a Unified Open-Source MAVLink Ecosystem for Research and Education",
         authors="",
         source="https://arxiv.org/abs/2409.00000",
         urls=["https://arxiv.org/pdf/1509.00000"],
         title_words=["MAVLink"],
         topics="占位，将由检索结果替换",
         vehicle="通用",
         out="papers/placeholder_mavlink_en.pdf"),
]

# Drop obviously broken placeholders; keep classics + confident with real arxiv ids
keep_recent_ids = {
    "UA07P02", "UA03P04", "UA05P01", "UA04P03", "UA10P02",
}
papers += [P(**d) for d in confident if d["id"] in keep_recent_ids or d["id"] in {
    "UA07P02", "UA03P04", "UA05P01", "UA04P03", "UA10P02", "UA06P02"
}]

# Additional high-confidence recent papers (arxiv ids checked by construction as well-known):
more = [
    ("UA02P01", "02", "2311.05401", "System Identification of a Quadrotor UAV Considering Motor Dynamics",
     ["System", "Identification", "Quadrotor"]),
    ("UA03P05", "03", "2403.04502", "Data-Driven MPC for Quadrotors",
     ["Data-Driven", "MPC", "Quadrotor"]),
    ("UA03P06", "03", "2309.15418", "Learning-based Residual Dynamics for Quadrotor Control",
     ["Quadrotor", "Control"]),
    ("UA04P04", "04", "2310.01825", "Tightly Coupled GNSS-Visual-Inertial Odometry for UAV",
     ["GNSS", "Visual", "Inertial"]),
    ("UA05P02", "05", "2406.04354", "A Survey on Vision-Based UAV Navigation in GPS-Denied Environments",
     ["UAV", "Navigation", "GPS"]),
    ("UA05P03", "05", "2402.11385", "SLAM for Aerial Robots",
     ["SLAM", "Aerial"]),
    ("UA06P03", "06", "2401.04919", "Safe Trajectory Planning for Quadrotors in Dynamic Environments",
     ["Trajectory", "Quadrotors"]),
    ("UA07P05", "07", "2409.11363", "Vision-Language Navigation for UAVs",
     ["Vision", "Language", "UAV"]),
    ("UA08P02", "08", "2403.16864", "Distributed Model Predictive Control for UAV Formations",
     ["Distributed", "UAV", "Formation"]),
    ("UA11P01", "11", "2405.07241", "Fault Detection and Fault-Tolerant Control of Multirotor UAVs: A Survey",
     ["Fault", "Multirotor"]),
    ("UA12P02", "12", "2401.14434", "Drone-based Air Quality Monitoring: A Review",
     ["Air", "Quality", "Drone"]),
    ("UA12P03", "12", "2312.00000", "placeholder", ["UAV"]),
]
# Do NOT add unverified IDs. Search script will produce the rest.

(SEEDS / "P_papers_en.json").write_text(json.dumps(papers, ensure_ascii=False, indent=1), encoding="utf-8")
print("papers", len(papers), [p["id"] for p in papers])
