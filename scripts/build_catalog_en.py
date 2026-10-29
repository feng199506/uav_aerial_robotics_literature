#!/usr/bin/env python3
"""Build catalog_cn.csv, progress, failures, and fill README progress from item state."""
import csv
import json
import time
from collections import Counter
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from common_en import ACCESS_DATE, CATS, ITEMS, ROOT, SEARCH_DATE, TYPES, WINDOW_START, WINDOW_END, item_state, load_json

SEEDS = ROOT / "scripts" / "seeds"


def load_seeds():
    out = []
    for f in sorted(SEEDS.glob("*.json")):
        out.extend(json.loads(f.read_text(encoding="utf-8")))
    return out


def year_in_window(y):
    try:
        yi = int(str(y)[:4])
    except (TypeError, ValueError):
        return None
    return WINDOW_START[:4] <= str(yi) <= WINDOW_END[:4] and not (
        yi == int(WINDOW_START[:4]) and False)


FIELDS = [
    "资料编号", "主分类", "交叉标签", "类型", "标题", "作者或机构", "学校", "年份", "版本",
    "语言", "难度", "先修要求", "原始来源", "下载地址", "本地路径", "完整性", "许可证",
    "推荐顺序", "飞行器类型", "任务", "传感器", "计算平台与软件", "仿真或实飞",
    "定位条件及环境", "评价指标", "代码与数据", "已验证范围", "作者报告限制", "信息依据",
    "是否复用", "复用来源", "适用地区", "提交号", "工具", "备注",
]


def row(seed, st):
    p = seed.get("paper") or {}
    reuse = seed.get("reuse") or {}
    return {
        "资料编号": seed["id"],
        "主分类": f"{seed['cat']}_{CATS.get(seed['cat'], '')}",
        "交叉标签": ";".join(seed.get("cross") or []),
        "类型": TYPES.get(seed["type"], seed["type"]),
        "标题": seed.get("title", ""),
        "作者或机构": seed.get("authors", ""),
        "学校": seed.get("school", ""),
        "年份": seed.get("year", ""),
        "版本": seed.get("version", "") or st.get("ref", "") or st.get("commit", ""),
        "语言": seed.get("lang", "en"),
        "难度": seed.get("level", ""),
        "先修要求": seed.get("prereq", ""),
        "原始来源": seed.get("source", ""),
        "下载地址": st.get("download_url") or st.get("final_url") or seed.get("source", ""),
        "本地路径": seed.get("out", ""),
        "完整性": (
            (seed.get("complete") or "完整") if st.get("status") == "ok"
            else ("失败" if st.get("status") == "failed" else "待核验")
        ),
        "许可证": seed.get("license", ""),
        "推荐顺序": seed.get("order", ""),
        "飞行器类型": seed.get("vehicle") or p.get("vehicle", ""),
        "任务": p.get("task", ""),
        "传感器": seed.get("sensors") or p.get("sensors", ""),
        "计算平台与软件": seed.get("stack") or p.get("software", ""),
        "仿真或实飞": p.get("setting", ""),
        "定位条件及环境": p.get("env", ""),
        "评价指标": p.get("metrics", ""),
        "代码与数据": p.get("code_data", ""),
        "已验证范围": p.get("verified_scope", ""),
        "作者报告限制": p.get("author_limits") or p.get("limits", ""),
        "信息依据": p.get("evidence") or seed.get("evidence", ""),
        "是否复用": "已有复用" if reuse else "新下载",
        "复用来源": reuse.get("path", ""),
        "适用地区": seed.get("region", ""),
        "提交号": st.get("commit", ""),
        "工具": seed.get("tool", ""),
        "备注": (seed.get("note") or "") + ((" | " + st.get("verify", "")) if st.get("verify") else ""),
    }


def main():
    seeds = load_seeds()
    ok, fail, todo = [], [], []
    for s in seeds:
        st = item_state(s["id"]) or {}
        status = st.get("status")
        if status == "ok":
            ok.append((s, st))
        elif status == "failed":
            fail.append((s, st))
        else:
            todo.append((s, st))

    catp = ROOT / "catalog_cn.csv"
    with catp.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        for s, st in ok:
            w.writerow(row(s, st))

    failp = ROOT / "download_failures_cn.csv"
    with failp.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["资料编号", "类型", "标题", "状态", "错误", "来源"])
        w.writeheader()
        for s, st in fail + todo:
            w.writerow({
                "资料编号": s["id"], "类型": s["type"], "标题": s.get("title", ""),
                "状态": st.get("status", "todo"),
                "错误": (st.get("error") or "")[:500],
                "来源": s.get("source", ""),
            })

    by_type = Counter(s["type"] for s, _ in ok)
    papers = [(s, st) for s, st in ok if s["type"] == "paper"]
    classic = [s for s, _ in papers if s.get("classic") or (str(s.get("year", "9999")) < WINDOW_START[:4])]
    # year-based: before 2024 is outside rolling 3y except late 2023
    recent, old = [], []
    for s, st in papers:
        y = str(s.get("year", ""))
        try:
            yi = int(y[:4])
        except ValueError:
            recent.append(s); continue
        if yi >= 2024 or y >= WINDOW_START[:4] and yi >= 2023:
            # 2023 papers need classic flag if before window; treat non-classic 2023 as recent-candidate
            if yi < 2023 or (yi == 2022) or yi <= 2022:
                old.append(s)
            elif yi == 2023:
                if s.get("classic"):
                    old.append(s)
                else:
                    recent.append(s)
            else:
                recent.append(s)
        else:
            old.append(s)

    prog = ROOT / "progress_cn.csv"
    with prog.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["类型", "已核验", "失败", "待办", "目标"])
        w.writerow(["教材/参考书", by_type["book"], sum(1 for s,_ in fail if s["type"]=="book"),
                    sum(1 for s,_ in todo if s["type"]=="book"), "15-25"])
        w.writerow(["大学课程/讲义", by_type["course"], sum(1 for s,_ in fail if s["type"]=="course"),
                    sum(1 for s,_ in todo if s["type"]=="course"), "10-15"])
        w.writerow(["论文/综述/学术教程", by_type["paper"], sum(1 for s,_ in fail if s["type"]=="paper"),
                    sum(1 for s,_ in todo if s["type"]=="paper"), "约50"])
        w.writerow(["官方工具文档", by_type["docs"], sum(1 for s,_ in fail if s["type"]=="docs"),
                    sum(1 for s,_ in todo if s["type"]=="docs"), "8-12"])
        w.writerow(["实验及实践案例", by_type["practice"], sum(1 for s,_ in fail if s["type"]=="practice"),
                    sum(1 for s,_ in todo if s["type"]=="practice"), "10-15"])
        w.writerow(["合计去重", len(ok), len(fail), len(todo), ""])
        n = len(papers)
        w.writerow(["论文近三年", len(recent), "", "", f"{len(recent)}/{n}" if n else "0"])
        w.writerow(["论文经典/窗口外", len(old), "", "", ""])

    print(f"ok={len(ok)} fail={len(fail)} todo={len(todo)} types={dict(by_type)}")
    print(f"papers recent={len(recent)} old={len(old)}")


if __name__ == "__main__":
    main()
