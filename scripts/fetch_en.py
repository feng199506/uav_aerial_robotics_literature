"""Download + verify library items described in scripts/seeds/*.json (resumable).

Usage:
  python3 -I scripts/fetch_en.py run  [--cat 05] [--ids ID,ID] [--type docs] [--redo] [--retry-failed]
  python3 -I scripts/fetch_en.py verify [--ids ...]      # re-run verification on existing output
  python3 -I scripts/fetch_en.py status

Kinds (seed["get"]["kind"]):
  pdf      urls:[..] (alternatives, first that verifies wins)
  pdfset   urls:[..] or index+pattern; saved as a directory of the original chapter PDFs
  file     url -> stored as-is (official zip / tar / pdf / txt); verify by archive listing
  hfdoc    lib, ver -> official built docs zip from the hf-doc-build dataset
  git      repo, ref, paths(optional sparse), keep upstream tree inside <out>.tar
  mirror   start, accept_prefix(es), domains -> wget offline mirror packed into <out>.tar

Nothing downloaded is executed or imported. One runner at a time (flock state/fetch.lock).
"""
import argparse
import fcntl
import hashlib
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tarfile
import time
import urllib.parse
import zipfile
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common_en import (ACCESS_DATE, ITEMS, ROOT, STAGING, SCRIPTS, STATE, http, item_state, norm_words,  # noqa: E402
                       save_item_state, use_pypdf)

SEEDS = SCRIPTS / "seeds"
GIT_ENV = {"GIT_TERMINAL_PROMPT": "0", "GIT_LFS_SKIP_SMUDGE": "1", "PATH": "/usr/bin:/bin", "HOME": str(STAGING),
           "GIT_CONFIG_NOSYSTEM": "1"}
BIG_EXT = re.compile(r"\.(pt|pth|ckpt|safetensors|bin|onnx|h5|hdf5|pb|tflite|gguf|npz|npy|mp4|mov|avi|mkv|webm|"
                     r"zip|tar|gz|tgz|xz|bz2|7z|parquet|arrow|whl|so|dll|dylib|exe|iso|dmg)$", re.I)
SMALL_LIMIT = 25 * 1024 * 1024       # any single file above this is dropped from source packs
BIG_EXT_LIMIT = 5 * 1024 * 1024      # weight/data/binary-like files above this are dropped


def load_seeds():
    seeds = []
    for f in sorted(SEEDS.glob("*.json")):
        for s in json.loads(f.read_text(encoding="utf-8")):
            s["_seedfile"] = f.name
            seeds.append(s)
    ids = [s["id"] for s in seeds]
    dup = {i for i in ids if ids.count(i) > 1}
    if dup:
        raise SystemExit(f"duplicate ids: {sorted(dup)}")
    return seeds


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def run(cmd, cwd=None, timeout=3600):
    r = subprocess.run(cmd, cwd=cwd, env=GIT_ENV, capture_output=True, text=True, timeout=timeout)
    if r.returncode != 0:
        raise RuntimeError(f"{' '.join(cmd[:4])}... rc={r.returncode}: {r.stderr.strip()[-400:]}")
    return r.stdout


# ---------------------------------------------------------------- PDF
def pdf_check(path, expect):
    pypdf = use_pypdf()
    with open(path, "rb") as f:
        if f.read(5) != b"%PDF-":
            return False, "不是 PDF 文件头", {}
    try:
        rd = pypdf.PdfReader(str(path))
        n = len(rd.pages)
        text = ""
        for i in range(min(n, int(expect.get("title_pages", 6)))):
            try:
                text += " " + (rd.pages[i].extract_text() or "")
            except Exception:
                pass
        # sample body pages for extractable text
        body_chars = 0
        sample = sorted({n // 4, n // 2, (3 * n) // 4, max(n - 2, 0)})
        for i in sample:
            try:
                body_chars += len(rd.pages[i].extract_text() or "")
            except Exception:
                pass
        meta_title = ""
        try:
            meta_title = (rd.metadata or {}).get("/Title", "") or ""
        except Exception:
            pass
    except Exception as e:
        return False, f"pypdf 解析失败: {type(e).__name__}: {str(e)[:120]}", {}
    info = {"pages": n, "meta_title": str(meta_title)[:200], "body_sample_chars": body_chars}
    minp = int(expect.get("min_pages", 1))
    if n < minp:
        return False, f"页数 {n} < 期望 {minp}", info
    words = norm_words(" ".join(expect.get("title_words", [])))
    if words:
        hay = set(norm_words(text + " " + str(meta_title)))
        ratio = sum(w in hay for w in words) / len(words)
        info["title_match"] = round(ratio, 2)
        if ratio < float(expect.get("min_ratio", 0.6)):
            return False, f"标题词匹配率 {ratio:.2f} 过低", info
    if body_chars < 200 and not expect.get("allow_scan"):
        return False, "正文抽样无可提取文本（疑似扫描/残缺）", info
    return True, f"通过：pypdf 可解析 {n} 页；标题词匹配 {info.get('title_match', '-')}", info


def get_pdf(seed, st):
    g = seed["get"]
    out = ROOT / seed["out"]
    out.parent.mkdir(parents=True, exist_ok=True)
    errs = []
    for url in g["urls"]:
        tmp = STAGING / (seed["id"] + ".pdf")
        r = http(url, dest=tmp, max_bytes=int(g.get("max_mb", 400)) * 1024 * 1024, timeout=300)
        if r["status"] != 200:
            errs.append(f"{url}: {r['status']} {r['err']}")
            continue
        ok, msg, info = pdf_check(tmp, seed.get("expect", {}))
        if ok:
            shutil.move(tmp, out)
            st.update(download_url=url, final_url=r["url"], http_last_modified=r.get("last_modified", ""),
                      verify=msg, info=info, bytes=out.stat().st_size, sha256=sha256(out))
            return True
        errs.append(f"{url}: {msg}")
        tmp.unlink(missing_ok=True)
    st["error"] = " | ".join(errs)[-1500:]
    return False


def get_pdfset(seed, st):
    g = seed["get"]
    outdir = ROOT / seed["out"]
    urls = list(g.get("urls", []))
    if g.get("index"):
        r = http(g["index"])
        if r["status"] != 200:
            st["error"] = f"index {r['status']} {r['err']}"
            return False
        html = r["body"].decode("utf-8", "replace")
        found = []
        for m in HREF_ANY.finditer(html):
            href = next(x for x in m.groups() if x)
            u = urllib.parse.urljoin(r["url"], href)
            if re.search(g["pattern"], u) and u not in found:
                found.append(u)
        urls += found
    if len(urls) < int(g.get("min_files", 1)):
        st["error"] = f"只找到 {len(urls)} 个章节链接 < {g.get('min_files')}"
        return False
    tmpdir = STAGING / (seed["id"] + "_set")
    shutil.rmtree(tmpdir, ignore_errors=True)
    tmpdir.mkdir(parents=True)
    bad, pages, names = [], 0, []
    for u in urls:
        name = urllib.parse.unquote(u.rstrip("/").split("/")[-1]) or "index.pdf"
        name = re.sub(r"[^A-Za-z0-9._-]", "_", name)
        if name in names:
            name = f"{len(names):03d}_{name}"
        dest = tmpdir / name
        r = http(u, dest=dest, timeout=300)
        if r["status"] != 200:
            bad.append(f"{u}: {r['status']}")
            continue
        if name.lower().endswith(".txt"):
            body = dest.read_bytes()
            ok = len(body) > 5000 and b"Request for Comments" in body[:20000]
            info, msg = {"pages": 0}, "" if ok else "文本过短或非 RFC 文本"
        else:
            ok, msg, info = pdf_check(dest, {"min_pages": 1, "allow_scan": True})
        if not ok:
            bad.append(f"{name}: {msg}")
            continue
        names.append(name)
        pages += info.get("pages", 0)
    if bad:
        st["error"] = f"{len(bad)} 个章节失败: " + "; ".join(bad)[:1200]
        return False
    (tmpdir / "_chapter_order_en.txt").write_text("\n".join(f"{n}\t{u}" for n, u in zip(names, urls)) + "\n")
    shutil.rmtree(outdir, ignore_errors=True)
    outdir.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(tmpdir, outdir)
    st.update(download_url=g.get("index") or urls[0], verify=f"通过：{len(names)} 个文件均可解析（PDF 共 {pages} 页）",
              info={"chapters": len(names), "pages": pages}, bytes=sum(p.stat().st_size for p in outdir.iterdir()))
    return True


# ---------------------------------------------------------------- archives
def list_archive(path):
    p = str(path)
    if p.endswith(".zip"):
        with zipfile.ZipFile(p) as z:
            return [i.filename for i in z.infolist() if not i.is_dir()], z
    with tarfile.open(p) as t:
        return [m.name for m in t.getmembers() if m.isfile()], t


def read_member(path, name):
    p = str(path)
    if p.endswith(".zip"):
        with zipfile.ZipFile(p) as z:
            return z.read(name)
    with tarfile.open(p) as t:
        f = t.extractfile(name)
        return f.read() if f else b""


HREF_ANY = re.compile(r"""href\s*=\s*(?:"([^"]+)"|'([^']+)'|([^\s>"']+))""", re.I)
HREF = re.compile(r'(?:href|src)=["\']([^"\'#?]+)', re.I)


def check_tree(names, path, expect, kind_hint=""):
    """names: member list. Checks counts, entry, license, and local link integrity of a sample."""
    raw_names = list(names)
    names = [n[2:] if n.startswith("./") else n for n in names]
    raw_of = dict(zip(names, raw_names))
    ext = {}
    for n in names:
        e = n.rsplit(".", 1)[-1].lower() if "." in n.split("/")[-1] else ""
        ext[e] = ext.get(e, 0) + 1
    html = ext.get("html", 0) + ext.get("htm", 0)
    docs = html + ext.get("md", 0) + ext.get("mdx", 0) + ext.get("rst", 0) + ext.get("ipynb", 0) + ext.get("txt", 0) \
        + ext.get("adoc", 0) + ext.get("tex", 0) + ext.get("xml", 0) * bool(expect.get("count_xml"))
    info = {"files": len(names), "html": html, "md_rst_ipynb": docs - html,
            "top_ext": sorted(ext.items(), key=lambda kv: -kv[1])[:8]}
    nset = set(names)
    entry = expect.get("entry")
    if entry:
        hits = [n for n in names if n == entry or n.endswith("/" + entry)]
        info["entry"] = hits[0] if hits else ""
        if not hits:
            return False, f"入口文件 {entry} 不存在", info
    lic = [n for n in names if re.search(r"(^|/)(LICENSE|LICENCE|COPYING|COPYRIGHT|NOTICE)[^/]*$", n, re.I)]
    info["license_files"] = lic[:5]
    if expect.get("need_license") and not lic:
        return False, "未找到许可证文件", info
    mind = int(expect.get("min_docs", 1))
    if docs < mind:
        return False, f"文档文件数 {docs} < 期望 {mind}", info
    for req in expect.get("must_have", []):
        if not any(re.search(req, n) for n in names):
            return False, f"缺少必需内容 /{req}/", info
    # local link check on a sample of html pages
    if html and expect.get("link_check", True):
        pages = [n for n in names if n.lower().endswith((".html", ".htm"))]
        step = max(1, len(pages) // 120)
        total = broken = 0
        missing = []
        arc = zipfile.ZipFile(str(path)) if str(path).endswith(".zip") else tarfile.open(str(path))
        for n in pages[::step][:120]:
            try:
                if isinstance(arc, zipfile.ZipFile):
                    body = arc.read(raw_of[n]).decode("utf-8", "replace")
                else:
                    body = arc.extractfile(raw_of[n]).read().decode("utf-8", "replace")
            except Exception:
                continue
            base = n.rsplit("/", 1)[0] if "/" in n else ""
            for m in HREF.finditer(body):
                u = m.group(1)
                if re.match(r"^[a-z][a-z0-9+.-]*:", u, re.I) or u.startswith("//") or u.startswith("/"):
                    continue
                tgt = os.path.normpath(os.path.join(base, urllib.parse.unquote(u)))
                total += 1
                if tgt not in nset and tgt.rstrip("/") + "/index.html" not in nset:
                    broken += 1
                    if len(missing) < 5:
                        missing.append(tgt)
        arc.close()
        info["link_sample"] = {"links": total, "broken": broken, "examples": missing}
        if total and broken / total > float(expect.get("max_broken", 0.05)):
            return False, f"本地链接抽样断链率 {broken}/{total} 过高", info
    return True, f"通过：{len(names)} 个文件（HTML {html}，文档源 {docs - html}）", info


def get_file(seed, st):
    g = seed["get"]
    out = ROOT / seed["out"]
    out.parent.mkdir(parents=True, exist_ok=True)
    errs = []
    for url in g.get("urls", [g.get("url")]):
        tmp = STAGING / (seed["id"] + "_" + url.rstrip("/").split("/")[-1][-40:])
        r = http(url, dest=tmp, max_bytes=int(g.get("max_mb", 800)) * 1024 * 1024, timeout=900)
        if r["status"] != 200:
            errs.append(f"{url}: {r['status']} {r['err']}")
            continue
        if seed["out"].endswith(".pdf"):
            ok, msg, info = pdf_check(tmp, seed.get("expect", {}))
        elif seed["out"].endswith((".txt", ".md", ".html")):
            body = tmp.read_bytes()
            ok = len(body) > int(seed.get("expect", {}).get("min_bytes", 1000))
            info = {"bytes": len(body)}
            msg = f"通过：{len(body)} 字节文本" if ok else "文本过短"
        else:
            try:
                names, _ = list_archive(tmp)
                ok, msg, info = check_tree(names, tmp, seed.get("expect", {}))
            except Exception as e:
                ok, msg, info = False, f"归档无法读取: {e}", {}
        if ok:
            shutil.move(tmp, out)
            st.update(download_url=url, final_url=r["url"][:300], http_last_modified=r.get("last_modified", ""),
                      verify=msg, info=info, bytes=out.stat().st_size, sha256=sha256(out))
            return True
        errs.append(f"{url}: {msg}")
        tmp.unlink(missing_ok=True)
    st["error"] = " | ".join(errs)[-1500:]
    return False


def get_hfdoc(seed, st):
    g = seed["get"]
    seed = dict(seed)
    seed["get"] = {"urls": [f"https://huggingface.co/datasets/hf-doc-build/doc-build/resolve/main/{g['lib']}/{g['ver']}.zip"],
                   "max_mb": 300}
    seed.setdefault("expect", {}).setdefault("link_check", False)
    return get_file(seed, st)


# ---------------------------------------------------------------- git
def pack_dir(src, out, prefix, st):
    """tar src (upstream tree) into out, dropping .git, oversized and weight/data-like files."""
    dropped = []

    def flt(ti):
        rel = ti.name
        if "/.git/" in rel + "/" or rel.endswith("/.git"):
            return None
        if ti.isfile():
            if ti.size > SMALL_LIMIT or (BIG_EXT.search(rel) and ti.size > BIG_EXT_LIMIT):
                dropped.append(f"{rel} ({ti.size // 1024} KiB)")
                return None
        if ti.issym() or ti.islnk():
            tgt = ti.linkname
            if tgt.startswith("/") or ".." in tgt.split("/"):
                return None
        ti.uid = ti.gid = 0
        ti.uname = ti.gname = "root"
        return ti
    tmp = Path(str(out) + ".part")
    with tarfile.open(tmp, "w:gz" if str(out).endswith(".tar.gz") else "w") as t:
        t.add(src, arcname=prefix, filter=flt)
    os.replace(tmp, out)
    st["dropped_large_files"] = dropped[:200]
    st["dropped_count"] = len(dropped)


def get_git(seed, st):
    g = seed["get"]
    out = ROOT / seed["out"]
    out.parent.mkdir(parents=True, exist_ok=True)
    work = STAGING / (seed["id"] + "_git")
    shutil.rmtree(work, ignore_errors=True)
    repo = g["repo"]
    paths = g.get("paths")
    cmd = ["git", "-c", "core.hooksPath=/dev/null", "-c", "advice.detachedHead=false", "clone", "-q", "--depth", "1",
           "--no-tags", "--single-branch"]
    if g.get("ref"):
        cmd += ["--branch", g["ref"]]
    if paths:
        cmd += ["--filter=blob:none", "--sparse", "--no-checkout"]
    cmd += [repo, str(work)]
    try:
        run(cmd, timeout=int(g.get("timeout", 3600)))
        if paths:
            run(["git", "-C", str(work), "sparse-checkout", "set", "--no-cone"] + ["/*.md", "/*.txt", "/*.rst",
                "/LICENSE*", "/COPYING*", "/NOTICE*", "/LICENCE*", "/CITATION*", "/pyproject.toml", "/setup.py",
                "/package.json"] + [p if p.startswith("/") else "/" + p for p in paths], timeout=600)
            run(["git", "-C", str(work), "-c", "core.hooksPath=/dev/null", "checkout", "-q"],
                timeout=int(g.get("timeout", 3600)))
        commit = run(["git", "-C", str(work), "rev-parse", "HEAD"]).strip()
        cdate = run(["git", "-C", str(work), "log", "-1", "--format=%cI"]).strip()
    except Exception as e:
        st["error"] = str(e)[-800:]
        shutil.rmtree(work, ignore_errors=True)
        return False
    shutil.rmtree(work / ".git", ignore_errors=True)
    prefix = out.name.rsplit(".tar", 1)[0]
    pack_dir(work, out, prefix, st)
    shutil.rmtree(work, ignore_errors=True)
    names, _ = list_archive(out)
    exp = dict(seed.get("expect", {}))
    exp.setdefault("need_license", not g.get("license_from_project"))
    exp.setdefault("link_check", bool(g.get("built_html")))
    ok, msg, info = check_tree(names, out, exp)
    st.update(download_url=repo, ref=g.get("ref") or "(默认分支)", commit=commit, commit_date=cdate,
              sparse_paths=paths or ["(整个仓库)"], verify=msg, info=info, bytes=out.stat().st_size, sha256=sha256(out))
    if not ok:
        st["error"] = msg
    return ok


# ---------------------------------------------------------------- wget mirror
def get_mirror(seed, st):
    g = seed["get"]
    out = ROOT / seed["out"]
    out.parent.mkdir(parents=True, exist_ok=True)
    work = STAGING / (seed["id"] + "_m")
    shutil.rmtree(work, ignore_errors=True)
    work.mkdir(parents=True)
    starts = g["start"] if isinstance(g["start"], list) else [g["start"]]
    host = urllib.parse.urlparse(starts[0]).netloc
    incl = g.get("include", [])  # path prefixes allowed for recursion (wget -I)
    cmd = ["wget", "-q", "-e", "robots=on", "--recursive", "--level", str(g.get("level", "inf")), "--no-parent",
           "--page-requisites", "--convert-links", "--adjust-extension", "--no-host-directories", "--timeout", "60",
           "--tries", "2", "--wait", str(g.get("wait", 0.3)), "--random-wait", "--user-agent",
           "Mozilla/5.0 (compatible; uav_aerial_robotics_literature/1.0; offline docs copy)",
           "--quota", f"{int(g.get('quota_mb', 600))}m", "--reject", "*.mp4,*.webm,*.mov,*.zip,*.tar.gz,*.whl,*.ipynb.zip",
           "--domains", ",".join(g.get("domains", [host])), "-P", str(work)]
    if g.get("span"):
        cmd += ["--span-hosts"]
    if incl:
        cmd += ["--include-directories", ",".join(incl)]
    if g.get("exclude"):
        cmd += ["--exclude-directories", ",".join(g["exclude"])]
    if g.get("reject_regex"):
        cmd += ["--reject-regex", g["reject_regex"]]
    r = subprocess.run(cmd + starts, capture_output=True, text=True, timeout=int(g.get("timeout", 5400)))
    st["wget_rc"] = r.returncode  # 8 = some 404s, normal for large sites
    prefix = out.name.rsplit(".tar", 1)[0]
    files = [p for p in work.rglob("*") if p.is_file()]
    st["quota_hit"] = sum(p.stat().st_size for p in files) >= int(g.get("quota_mb", 600)) * 1024 * 1024 * 0.98
    if not files:
        st["error"] = f"wget 无输出 rc={r.returncode} {r.stderr[-300:]}"
        return False
    pack_dir(work, out, prefix, st)
    shutil.rmtree(work, ignore_errors=True)
    names, _ = list_archive(out)
    ok, msg, info = check_tree(names, out, seed.get("expect", {}))
    if st["quota_hit"]:
        ok, msg = False, "镜像达到配额上限，可能不完整：" + msg
    st.update(download_url=starts[0], mirror_scope={"start": starts, "include": incl, "level": g.get("level", "inf")},
              verify=msg, info=info, bytes=out.stat().st_size, sha256=sha256(out))
    if not ok:
        st["error"] = msg
    return ok


def get_multi_git(seed, st):
    """Several complete repos (e.g. a course's assignment repos) -> <out>/<repo>_<commit7>_en.tar each."""
    outdir = ROOT / seed["out"]
    outdir.mkdir(parents=True, exist_ok=True)
    parts, errs = [], []
    for repo in seed["get"]["repos"]:
        name = repo.rstrip("/").split("/")[-1]
        sub = {"id": f"{seed['id']}_{name}", "out": str((outdir / f"{name}_en.tar").relative_to(ROOT)),
               "get": {"kind": "git", "repo": repo}, "expect": {"need_license": False, "min_docs": 1}}
        sst = {}
        if get_git(sub, sst):
            final = outdir / f"{name}_{sst['commit'][:7]}_en.tar"
            os.replace(ROOT / sub["out"], final)
            lic = sst["info"].get("license_files")
            parts.append({"repo": repo, "commit": sst["commit"], "commit_date": sst["commit_date"], "file": final.name,
                          "files": sst["info"]["files"], "license_files": lic, "dropped": sst.get("dropped_count", 0)})
        else:
            errs.append(f"{repo}: {sst.get('error', '')[:200]}")
    st["parts"] = parts
    st["download_url"] = seed["get"]["repos"][0]
    st["bytes"] = sum(p.stat().st_size for p in outdir.iterdir())
    if errs:
        st["error"] = " | ".join(errs)
        return False
    nolic = [p["repo"] for p in parts if not p["license_files"]]
    st["verify"] = f"通过：{len(parts)} 个仓库完整归档" + (f"；无许可证文件：{len(nolic)} 个（见 parts）" if nolic else "")
    return True


KINDS = {"multi_git": get_multi_git, "pdf": get_pdf, "pdfset": get_pdfset, "file": get_file, "hfdoc": get_hfdoc, "git": get_git,
         "mirror": get_mirror}


def select(seeds, a):
    out = seeds
    if a.cat:
        cats = a.cat.split(",")
        out = [s for s in out if s["cat"] in cats]
    if a.type:
        out = [s for s in out if s["type"] in a.type.split(",")]
    if a.ids:
        ids = set(a.ids.split(","))
        out = [s for s in out if s["id"] in ids]
    if a.tool:
        out = [s for s in out if s.get("tool")]
    if a.seedfile:
        out = [s for s in out if s["_seedfile"].startswith(a.seedfile)]
    if a.kind:
        kinds = a.kind.split(",")
        out = [s for s in out if s["get"]["kind"] in kinds or (s.get("reuse") and "reuse" in kinds)]
    return out


def do_item(seed, redo=False, retry=False):
    st = item_state(seed["id"])
    if seed.get("reuse"):
        return do_reuse(seed, st)
    if st.get("status") == "ok" and not redo:
        return st
    if st.get("status") in ("failed", "partial") and not (redo or retry):
        return st
    st = {"id": seed["id"], "started": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    kind = seed["get"]["kind"]
    STAGING.mkdir(parents=True, exist_ok=True)
    try:
        ok = KINDS[kind](seed, st)
    except Exception as e:
        ok = False
        st["error"] = f"{type(e).__name__}: {e}"[:800]
    st["status"] = "ok" if ok else "failed"
    st["access_date"] = ACCESS_DATE
    st["finished"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    save_item_state(seed["id"], st)
    return st


def do_reuse(seed, st):
    """Copy a verified file from a sibling library (never move/delete the original)."""
    if st.get("status") == "ok":
        return st
    src = Path(seed["reuse"]["path"])
    out = ROOT / seed["out"]
    st = {"id": seed["id"], "reused_from": str(src)}
    if not src.exists():
        st.update(status="failed", error="复用源不存在")
    else:
        out.parent.mkdir(parents=True, exist_ok=True)
        if src.is_dir():
            shutil.copytree(src, out, dirs_exist_ok=True)
            st.update(status="ok", verify="复用目录已复制（源库已核验）", bytes=sum(p.stat().st_size for p in out.rglob("*") if p.is_file()))
        else:
            shutil.copy2(src, out)
            if str(out).endswith(".pdf"):
                ok, msg, info = pdf_check(out, seed.get("expect", {}))
            else:
                ok, msg, info = True, "复用文件已复制", {}
            st.update(status="ok" if ok else "failed", verify=msg, info=info, bytes=out.stat().st_size,
                      sha256=sha256(out), error="" if ok else msg)
    st["access_date"] = ACCESS_DATE
    save_item_state(seed["id"], st)
    return st


def reverify(seed):
    """Re-run checks on an existing output (after a seed's expect/entry was corrected)."""
    st = item_state(seed["id"])
    out = ROOT / seed["out"]
    if not st or not out.exists() or seed.get("reuse"):
        return
    kind = seed["get"]["kind"]
    if out.is_dir() or kind == "pdf" or str(out).endswith(".pdf"):
        return
    exp = dict(seed.get("expect", {}))
    if kind == "git":
        exp.setdefault("need_license", not seed["get"].get("license_from_project"))
        exp.setdefault("link_check", bool(seed["get"].get("built_html")))
    if kind == "hfdoc":
        exp.setdefault("link_check", False)
    names, _ = list_archive(out)
    ok, msg, info = check_tree(names, out, exp)
    st.update(status="ok" if ok else "failed", verify=msg, info=info, error="" if ok else msg,
              reverified=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
    save_item_state(seed["id"], st)
    print(f"{seed['id']:<14} {st['status']:<7} {msg[:150]}", flush=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["run", "status", "verify"])
    ap.add_argument("--cat")
    ap.add_argument("--ids")
    ap.add_argument("--type")
    ap.add_argument("--tool", action="store_true")
    ap.add_argument("--seedfile", help="prefix of seed file name, e.g. C_ or T_")
    ap.add_argument("--kind", help="comma list of get.kind; also selects the lock lane")
    ap.add_argument("--redo", action="store_true")
    ap.add_argument("--retry-failed", action="store_true")
    a = ap.parse_args()
    seeds = select(load_seeds(), a)
    if a.cmd == "status":
        cnt = {}
        for s in seeds:
            k = item_state(s["id"]).get("status", "todo")
            cnt[k] = cnt.get(k, 0) + 1
            if k == "failed":
                print(s["id"], item_state(s["id"]).get("error", "")[:200])
        print(cnt)
        return
    STATE.mkdir(exist_ok=True)
    lane = (a.seedfile or "") + re.sub(r"[^a-z,]", "", a.kind or "all").replace(",", "_")
    lockf = open(STATE / f"fetch_{lane}.lock", "w")
    try:
        fcntl.flock(lockf, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        raise SystemExit(f"another fetch_en.py is running in lane {lane}")
    for s in seeds:
        if a.cmd == "verify":
            reverify(s)
            continue
        st = do_item(s, redo=a.redo, retry=a.retry_failed)
        mb = (st.get("bytes") or 0) / 1e6
        print(f"{s['id']:<14} {st.get('status'):<7} {mb:8.1f}MB  {(st.get('verify') or st.get('error') or '')[:150]}",
              flush=True)


if __name__ == "__main__":
    main()
