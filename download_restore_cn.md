# 下载与解压恢复说明（无人机与空中机器人文献库，2026-10-29）

本资料库按“轻量 Git 分支 + Release 全文附件”的方式发布：

- **Git 分支 `release-lite-20261029`**：只包含总目录 `catalog_cn.csv`、进度、学习路线、工具对照、实践索引、检索记录、最终报告、脚本、断点状态（`state/items/`）和本说明，不含 PDF 全文、课程讲义包、官方文档镜像和参考项目。仓库原有的 `main` 分支没有改动。
- **Release `uav-full-20261029`**：3 个独立的不压缩 `.tar` 包，合起来就是完整的资料库，包括 12 个子方向目录下的全部教材、课程、工具文档、参考项目，以及 `papers/` 中的全部论文。

Release 页面：https://github.com/feng199506/uav_aerial_robotics_literature/releases/tag/uav-full-20261029

## 1. 包列表

| 包文件名 | 内容范围（按路径顺序） |
|---|---|
| `uav_aerial_robotics_20261029_batch001_cn_en.tar` | 顶层目录与报告、`scripts/`、`state/`、`01_foundations/` 至 `08_multi_uav/` 全部内容、`09_flight_software_communications/practice/`，以及各子方向的空占位目录 |
| `uav_aerial_robotics_20261029_batch002_cn_en.tar` | `09_flight_software_communications/tools/`、`10_simulation_testing/`、`12_civil_applications/books/`、`papers/` 前 45 篇 |
| `uav_aerial_robotics_20261029_batch003_cn_en.tar` | `papers/` 其余 11 篇 |

每个文件属于哪个包，见 `archive_index_cn.csv`（UTF-8 带 BOM，可直接用 Excel 打开；545 行，其中 527 个文件、18 个空目录）。表中列出包文件名、批次、相对路径、类型和字节数。

- 每个包都可以**单独解压**，不需要拼接。只要某几类资料时，可以只下载对应的包。
- 各包之间**没有重复文件**，解压到同一目录时不会互相覆盖。
- 包未压缩，解压很快，所需磁盘空间约等于包的大小。全部解压约需 **3.0 GiB**。如果还要展开里面的文档镜像和参考项目（见第 4 节），建议预留 6 GiB。

## 2. Windows：浏览器下载

1. 打开上面的 Release 页面，展开 **Assets**。
2. 依次点击 3 个 `.tar` 文件，以及 `archive_index_cn.csv`、`windows_rename_map_cn.csv`、`download_restore_cn.md`、`upload_report_cn.md`，全部保存到**同一个下载文件夹**，例如 `D:\下载\uav\`。
3. 单个包最大约 1.5 GB。浏览器提示“是否保留”时选择保留。下载中断可在浏览器下载列表里点“恢复”或重新下载。
4. 对照 `upload_report_cn.md` 中的字节数，在文件属性里核对每个包的大小（属性窗口里看“大小”的字节数，不要看“占用空间”）。

## 3. Windows：WinRAR 解压（全部解压到同一个目标目录）

请使用 **WinRAR 6 或更新版本**，目标目录用短路径，例如 `D:\uav\`。

**方法 A：一次批量解压（推荐）**

1. 在下载文件夹中，按住 Ctrl 选中全部 3 个 `.tar` 文件。
2. 右键 → **WinRAR → 解压文件…**（Extract files…）。
3. “目标路径”填 `D:\uav\`。
4. **不要**勾选“解压到单独的文件夹 / 在子文件夹中解压”（Extract archives to subfolders）。
5. 确定。所有包会解压到同一个 `D:\uav\` 下，恢复出完整的目录结构：

```
D:\uav\
├─ README_cn.md、catalog_cn.csv、learning_path_cn.md、final_report_cn.md、tools_map_cn.md …
├─ 01_foundations\ … 12_civil_applications\
├─ papers\
├─ scripts\
└─ state\
```

**方法 B：逐个解压**

对每个 `.tar` 文件：右键 → WinRAR → **解压文件…** → 目标路径都填同一个 `D:\uav\` → 确定。

注意：不要用“解压到 uav_aerial_robotics_20261029_batch00X_cn_en\”这个菜单项，它会给每个包各建一个子文件夹，目录结构就被拆散了。

### Windows 文件名兼容

发布包里的全部文件名都已检查并处理，Windows 下解压不会因文件名报错。最长相对路径 151 个字符。具体处理如下，逐条明细见 `windows_rename_map_cn.csv`。资料库的本地原件没有改动。

- **Tedrake《Underactuated Robotics》网页版**（`03_flight_control/books/Tedrake_UnderactuatedRobotics_Notes_html_en/`）：4 个文件名里带 `?`（例如 `cubic_bistable.html?height=240px.html`），已把 `?` 改成 `_`。引用这些文件的 6 个网页里，对应链接也已同步改写，离线打开时仍能正常显示。
- **3 个官方文档离线镜像**：ArduPilot Wiki、Mission Planner、Gazebo Harmonic 这 3 个内层 `.tar` 里，有 72 个网页样式、脚本和字体文件的名字带 `?v=…`。发布包里的这 3 个内层 `.tar` 已重新打包：文件名里的 `?` 改成 `_`，网页里对应的链接同步改写，其余内容不变。所以它们与资料库原件的字节数不同，这是正常的。
- 其余 32 个内层 `.tar`、6 个 `.zip`，以及全部普通文件，名字里都没有 Windows 不允许的字符，也没有只差大小写的文件，没有改动。

## 4. 内层归档（.zip / .tar）

资料库本身就有一部分资料是整包保存的，解压发布包之后它们仍然是单个文件。需要时再单独解开：

- **6 个 `.zip`**：MIT OCW 课程包，在 `01_foundations/courses/`、`03_flight_control/courses/`、`04_state_estimation/courses/`、`05_perception_localization_mapping/courses/` 下。
- **35 个 `.tar`**：分两类。一类是官方工具文档，在 `09_.../tools/` 和 `10_.../tools/` 下，有 HTML 离线镜像和 git 文档源两种。另一类是参考项目的源码快照，在各子方向的 `practice/` 下；BYU 小型无人机课程的讲义也在 `02_modeling_dynamics/courses/` 的一个 `.tar` 里。

解开方法：右键该文件 → WinRAR → **解压到 “文件名\”**。HTML 镜像解开后，用浏览器打开其中的 `index.html`。

## 5. Linux / macOS

```bash
mkdir -p ~/uav
for f in uav_aerial_robotics_20261029_batch*_cn_en.tar; do tar -xf "$f" -C ~/uav || echo "FAILED: $f"; done
```

（macOS 自带 bsdtar，同样支持此格式。）

## 6. 资料状态说明（来自资料库自身的目录，与打包无关）

- **只计已核验条目**：全库去重 117 条（教材 16、大学课程 11、论文 56、官方工具文档 19 份文件，约 11 套不重复工具、参考项目 15）。下载失败的 18 条记录在 `download_failures_cn.csv`，不计入，也没有对应文件。
- **完整性为“部分”的 13 条**：`catalog_cn.csv` 的“完整性”列里，有 13 条标为“部分”，其中大多是官方文档的 HTML 离线镜像，另有 1 条 MIT VNAV 2023 讲义。PX4 和 ArduPilot 的 HTML 镜像抓取时达到页数上限，只保存了部分页面；需要完整内容时，看同目录下的 git 文档源（`*_src_en.tar`）。每条的具体情况以 `catalog_cn.csv` 和 `final_report_cn.md` 为准。
- 美国 FAA Part 107 学习指南只适用于美国，不能当作欧盟或中国的运行规定。
- 本次按 2026-10-29 20:25（中欧时间）的资料库内容打包。打包前先把整个资料库复制成一份快照，打包用的就是这份快照。之后资料库再有改动，不会进入这次发布。

## 7. 完整性说明

- 本次发布只登记了上传状态（以 GitHub API 显示附件为 `uploaded`、远端大小等于本地大小为准），**没有**做下载回验和哈希校验。
- 资料库本身没有整库的 SHA-256 清单。
- 资料库中的资料文件都已打包，没有遗漏。只排除了 3 类不属于资料的内容：本地 `.git/`、`scripts/__pycache__/`（1 个 `.pyc`），以及 `state/` 下 6 个空的 `.lock` 锁文件。
