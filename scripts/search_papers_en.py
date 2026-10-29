#!/usr/bin/env python3
"""arXiv discovery helper for UAV / aerial robotics papers.

Usage:
  python3 -I scripts/search_papers_en.py arxiv QUERY [-n 40] [--all-dates]
  python3 -I scripts/search_papers_en.py batch
"""
import argparse
import sys
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from common_en import WINDOW_START, WINDOW_END, wait, UA_ALT  # noqa: E402

NS = {"a": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/arxiv"}
WIN_FROM = WINDOW_START.replace("-", "")
WIN_TO = WINDOW_END.replace("-", "")


def get(url):
    err = ""
    for attempt in range(4):
        wait("arxiv.org", 4.0)
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA_ALT, "Accept": "application/atom+xml"})
            with urllib.request.urlopen(req, timeout=90) as r:
                return r.read()
        except Exception as e:
            err = repr(e)
            time.sleep(8 * (attempt + 1))
    raise SystemExit(f"arxiv request failed: {err}")


def parse(body):
    out = []
    root = ET.fromstring(body)
    for e in root.findall("a:entry", NS):
        vid = e.findtext("a:id", "", NS).rsplit("/abs/", 1)[-1]
        if "api/errors" in vid:
            continue
        pc = e.find("arxiv:primary_category", NS)
        out.append({
            "id": vid,
            "v1": e.findtext("a:published", "", NS)[:10],
            "upd": e.findtext("a:updated", "", NS)[:10],
            "cat": pc.get("term") if pc is not None else "",
            "title": " ".join(e.findtext("a:title", "", NS).split()),
            "authors": [a.findtext("a:name", "", NS) for a in e.findall("a:author", NS)][:8],
            "abs": " ".join(e.findtext("a:summary", "", NS).split())[:400],
        })
    return out


def search(q, n=30, all_dates=False):
    if not all_dates:
        q = f"({q}) AND submittedDate:[{WIN_FROM}0000 TO {WIN_TO}2359]"
    url = ("https://export.arxiv.org/api/query?search_query="
           + urllib.parse.quote(q) + f"&start=0&max_results={n}&sortBy=submittedDate&sortOrder=descending")
    return parse(get(url))


def show(rows):
    for r in rows:
        au = r["authors"][0].split()[-1] if r["authors"] else "?"
        print(f"{r['v1']}  {r['id']:<22} {r['cat']:<10} {au:12} {r['title'][:110]}")


QUERIES = [
    ('ti:"aerial robotics" OR ti:"aerial robot" OR ti:quadrotor OR ti:quadcopter OR ti:multirotor', 40),
    ('ti:UAV AND (ti:control OR ti:navigation OR ti:slam OR ti:planning OR ti:inspection)', 35),
    ('ti:"visual-inertial" AND (UAV OR quadrotor OR aerial)', 20),
    ('ti:VTOL AND (control OR modeling OR transition)', 15),
    ('(ti:"drone racing" OR ti:"learning to fly" OR ti:"aerial navigation") AND (cat:cs.RO OR cat:cs.LG)', 20),
    ('ti:swarm AND (UAV OR quadrotor OR aerial) AND (cat:cs.RO OR cat:eess.SY)', 20),
    ('(ti:"flight control" OR ti:MPC) AND (quadrotor OR UAV OR "aerial robot")', 20),
    ('(ti:survey OR ti:review OR ti:tutorial) AND (quadrotor OR "aerial robot" OR "unmanned aerial")', 25),
    ('ti:Gazebo OR ti:SITL OR ti:AirSim OR ti:JSBSim OR ti:"hardware in the loop" AND (UAV OR PX4 OR quadrotor)', 15),
    ('(ti:inspection OR ti:photogrammetry OR ti:agriculture OR ti:"air quality" OR ti:disaster) AND (UAV OR drone OR unmanned)', 25),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["arxiv", "batch"])
    ap.add_argument("query", nargs="?")
    ap.add_argument("-n", type=int, default=25)
    ap.add_argument("--all-dates", action="store_true")
    a = ap.parse_args()
    if a.cmd == "arxiv":
        show(search(a.query, a.n, a.all_dates))
        return
    seen = set()
    for q, n in QUERIES:
        print("\n===", q, "===")
        try:
            rows = search(q, n)
        except SystemExit as e:
            print("FAIL", e)
            continue
        for r in rows:
            if r["id"] in seen:
                continue
            seen.add(r["id"])
            show([r])


if __name__ == "__main__":
    main()
