#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
嵩口项目可视化看板 · 自动更新脚本
===================================
自动扫描 images/ videos/ audio/ 目录下的素材文件，
重新生成「嵩口项目可视化看板.html」。

用法：
    python3 scripts/update_dashboard.py              # 生成看板
    python3 scripts/update_dashboard.py --watch      # 监控模式，文件变化自动更新
    python3 scripts/update_dashboard.py --output xx  # 指定输出路径

依赖：Python 3.8+，无需第三方库。
"""

import os
import sys
import time
import json
import hashlib
import urllib.parse
from pathlib import Path
from datetime import datetime

# ─── 配置 ───────────────────────────────────────────────────────────

REPO_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_FILE = REPO_ROOT / "songkou-dashboard.html"

# GitHub 信息（用于生成 jsDelivr CDN 链接）
GITHUB_USER = "easyeye163"
GITHUB_REPO = "h3-video-coding"
GITHUB_BRANCH = "main"

# 项目总览配置
PROJECT_TITLE = "嵩口宣传项目"
PROJECT_SUBTITLE = "永泰嵩口古镇 20 集 AI 文化宣传短剧 · 素材与进度看板"
TOTAL_EPISODES = 20
SEGMENTS_PER_EP = 4

# 分集标题（按 EP1-EP20 顺序）
EPISODE_TITLES = [
    "初见嵩口", "阿公的故事", "鹤形之谜", "用坦厝的秘密", "导演来了",
    "小糯米的疑问", "龙口祖厝的传说", "宁远庄往事", "万安堡探秘", "巷弄时光",
    "木雕匠心", "四水归堂", "神秘旅人", "节日准备", "月光下的古镇",
    "新旧碰撞", "传承之路", "镜头背后", "告别与承诺", "千年回响",
]

# 素材分类配置
# 每个分类：目录路径（相对 repo 根）、显示标题、卡片说明、文件扩展名
ASSET_CATEGORIES = {
    "characters": {
        "dir": "images/songkou_characters",
        "title": "角色定妆图（三视图）",
        "dot": "d-green",
        "hint": "角色三视图定妆图（真人写实 + 电影滤镜）。",
        "extensions": {".png", ".jpg", ".jpeg", ".webp"},
        # 文件名 → 显示名称 映射
        "name_map": {
            "lin_xiaoxi_three_view.png": "林小溪 · 主角 24 岁返乡青年",
            "chen_agong_three_view.png": "陈阿公 · 72 岁智慧长者",
            "zhang_director_three_view.png": "张导演 · 35 岁纪录片导演",
            "mysterious_traveler_three_view.png": "神秘旅人 · 哲学思考者",
            "xiao_nuomi_three_view.png": "小糯米 · 8 岁天真孩童",
            "songkou_panorama_firstframe.png": "嵩口全景 · 成片首帧",
            "张导演_three_view.png": "张导演 · 35 岁纪录片导演（中文名版）",
            "王婶_three_view.png": "王婶 · 嵩口古镇热心长辈",
        },
    },
    "scenes": {
        "dir": "images/嵩口真实场景图",
        "title": "嵩口真实场景图",
        "dot": "d-gold",
        "hint": "",
        "extensions": {".png", ".jpg", ".jpeg", ".webp"},
        "name_map": {
            "嵩口全景.png": "嵩口全景 · 大樟溪穿镇而过",
            "德星楼.jpeg": "德星楼 · 三层木阁楼",
            "古码头.png": "古码头 · 千年古榕渡口",
            "龙口祖厝.png": "龙口祖厝 · 183 间大厝群",
            "鹤形路.png": "鹤形路 · 150 米仙鹤巷道",
            "宁远庄.png": "宁远庄 · 四井拱梁大寨堡",
            "万安堡.png": "万安堡 · 三层防御寨堡",
            "古城墙.webp": "古城墙 · 防御体系遗存",
            "夯土墙.jpeg": "夯土墙 · 闽式生土夯筑",
            "现代改造新建筑.png": "现代改造 · 嵩口模式活化",
            "用坦厝.jpeg": "用坦厝 · 原图参考",
            "用坦厝_krea.png": "用坦厝 · KREA 风格化",
            "用坦厝_zimage.png": "用坦厝 · Z-image 文生图",
        },
    },
    "videos_drama": {
        "dir": "videos/songkou_drama",
        "title": "视频成片 · 嵩口短剧",
        "dot": "d-red",
        "hint": "点击视频右下角播放按钮即可预览；较大文件建议 WiFi 下播放。",
        "extensions": {".mp4", ".mov", ".webm"},
        "prefix": "🎬 ",
    },
    "videos_misc": {
        "dir": "videos",
        "title": "视频素材 · 其他",
        "dot": "d-red",
        "hint": "",
        "extensions": {".mp4", ".mov", ".webm"},
        "exclude_subdirs": {"songkou_drama"},
        "prefix": "素材 · ",
    },
    "audio_voices": {
        "dir": "audio/voices",
        "title": "角色音色（专属）",
        "dot": "d-blue",
        "hint": "",
        "extensions": {".flac", ".mp3", ".wav", ".m4a"},
        "name_map": {
            "songkou_girl_main.flac": "🎙 林小溪 · 温柔活泼女声（专属）",
            "songkou_elder.flac": "🎙 陈阿公 · 沧桑长者男声（专属）",
            "songkou_traveler.flac": "🎙 神秘旅人 · 清冷男声（专属）",
            "张导演_voice.flac": "🎙 张导演 · 纪录片导演男声（专属）",
            "王婶_voice.flac": "🎙 王婶 · 热心长辈女声（专属）",
        },
    },
    "audio_misc": {
        "dir": "audio",
        "title": "备选音色库",
        "dot": "d-blue",
        "hint": "",
        "extensions": {".flac", ".mp3", ".wav", ".m4a"},
        "exclude_subdirs": {"voices"},
        "name_map": {
            "01_温暖治愈男生.flac": "🎙 张导演 · 活泼男生（复用）",
            "03_活泼女生.flac": "🎙 小糯米 · 活泼女生（复用）",
            "20岁女生.flac": "🎙 20 岁女生 · 备选音色",
            "20岁女生_清冷.flac": "🎙 20 岁女生 · 清冷版（备选）",
            "02_温暖治愈男生_v2.flac": "🎙 温暖治愈男生 v2（备选）",
        },
    },
}


# ─── 工具函数 ───────────────────────────────────────────────────────

def jsdelivr_url(rel_path: str) -> str:
    """生成 jsDelivr CDN 链接，自动 URL 编码中文路径"""
    encoded = urllib.parse.quote(rel_path)
    return f"https://cdn.jsdelivr.net/gh/{GITHUB_USER}/{GITHUB_REPO}@{GITHUB_BRANCH}/{encoded}"


def pages_url(rel_path: str) -> str:
    """GitHub Pages URL — 正确返回 video/mp4 content-type，适合视频文件"""
    encoded = urllib.parse.quote(rel_path)
    return f"https://{GITHUB_USER}.github.io/{GITHUB_REPO}/{encoded}"


VIDEO_EXTENSIONS = {".mp4", ".mov", ".webm", ".avi"}


def scan_files(category_key: str, config: dict) -> list:
    """扫描指定目录下的素材文件，返回 [{name, path, url, size}] 列表"""
    base_dir = REPO_ROOT / config["dir"]
    if not base_dir.exists():
        return []

    name_map = config.get("name_map", {})
    prefix = config.get("prefix", "")
    extensions = config["extensions"]
    exclude_subdirs = config.get("exclude_subdirs", set())

    files = []
    for f in sorted(base_dir.rglob("*")):
        if not f.is_file():
            continue
        if f.suffix.lower() not in extensions:
            continue
        # 排除子目录
        rel = f.relative_to(base_dir)
        if len(rel.parts) > 1 and rel.parts[0] in exclude_subdirs:
            continue

        rel_path = str(Path(config["dir"]) / rel)
        filename = f.name
        display_name = name_map.get(filename, prefix + f.stem)

        files.append({
            "name": display_name,
            "filename": filename,
            "rel_path": rel_path,
            "url": pages_url(rel_path) if Path(rel_path).suffix.lower() in VIDEO_EXTENSIONS else jsdelivr_url(rel_path),
            "size": f.stat().st_size,
        })

    return files


def parse_episode_progress(video_files: list) -> dict:
    """从视频文件名解析分集进度
    文件名格式：EP{num}段{seg}_{desc}.mp4
    返回：{ep_num: {segments: {1,2,3,4}, complete: bool}}
    """
    import re
    episodes = {}

    for vf in video_files:
        m = re.match(r"EP(\d+)段(\d+)", vf["filename"])
        if not m:
            continue
        ep_num = int(m.group(1))
        seg_num = int(m.group(2))

        if ep_num not in episodes:
            episodes[ep_num] = {"segments": set(), "complete": False}
        episodes[ep_num]["segments"].add(seg_num)

    for ep_num, info in episodes.items():
        info["complete"] = len(info["segments"]) >= SEGMENTS_PER_EP

    return episodes


def dir_snapshot(dir_path: Path, extensions: set = None) -> str:
    """生成目录快照 hash，用于检测文件变化"""
    h = hashlib.md5()
    if not dir_path.exists():
        return "empty"

    for f in sorted(dir_path.rglob("*")):
        if not f.is_file():
            continue
        if extensions and f.suffix.lower() not in extensions:
            continue
        rel = f.relative_to(dir_path)
        stat = f.stat()
        h.update(f"{rel}|{stat.st_size}|{stat.st_mtime}".encode())

    return h.hexdigest()


# ─── HTML 生成 ──────────────────────────────────────────────────────

def generate_html() -> str:
    """生成完整的看板 HTML"""
    today = datetime.now().strftime("%Y-%m-%d")

    # 扫描所有素材
    characters = scan_files("characters", ASSET_CATEGORIES["characters"])
    scenes = scan_files("scenes", ASSET_CATEGORIES["scenes"])
    videos_drama = scan_files("videos_drama", ASSET_CATEGORIES["videos_drama"])
    videos_misc = scan_files("videos_misc", ASSET_CATEGORIES["videos_misc"])
    audio_voices = scan_files("audio_voices", ASSET_CATEGORIES["audio_voices"])
    audio_misc = scan_files("audio_misc", ASSET_CATEGORIES["audio_misc"])

    # 计算进度
    ep_progress = parse_episode_progress(videos_drama)
    completed_eps = sum(1 for info in ep_progress.values() if info["complete"])
    completed_segs = sum(len(info["segments"]) for info in ep_progress.values())
    total_segs = TOTAL_EPISODES * SEGMENTS_PER_EP

    char_count = len(characters)
    voice_count = len(audio_voices)
    scene_count = len(scenes)

    # 分集矩阵
    eps_html = ""
    for i in range(TOTAL_EPISODES):
        ep_num = i + 1
        title = EPISODE_TITLES[i] if i < len(EPISODE_TITLES) else f"第{ep_num}集"
        info = ep_progress.get(ep_num, {"segments": set(), "complete": False})

        if info["complete"]:
            status_cls = "done"
            status_text = "成片完成"
        elif len(info["segments"]) > 0:
            status_cls = "ready"
            status_text = f"{len(info['segments'])}/{SEGMENTS_PER_EP} 段"
        else:
            status_cls = "wait"
            status_text = "未开始"

        eps_html += f'      <div class="ep"><span class="no">EP{ep_num}</span><span class="nm">{title}</span><span class="st {status_cls}">{status_text}</span></div>\n'

    # 角色定妆图
    chars_html = ""
    for item in characters:
        chars_html += f'      <div class="img"><img src="{item["url"]}" alt="{item["name"]}" loading="lazy"><div class="cap">{item["name"]}</div></div>\n'

    # 场景图
    scenes_html = ""
    for item in scenes:
        scenes_html += f'      <div class="img"><img src="{item["url"]}" alt="{item["name"]}" loading="lazy"><div class="cap">{item["name"]}</div></div>\n'

    # 短剧视频
    drama_html = ""
    for item in videos_drama:
        drama_html += f'      <div class="video"><div class="tt">{item["name"]}</div>\n        <video src="{item["url"]}" type="video/mp4" controls preload="metadata" playsinline></video></div>\n'

    # 其他视频
    misc_videos_html = ""
    for item in videos_misc:
        misc_videos_html += f'      <div class="video"><div class="tt">{item["name"]}</div>\n        <video src="{item["url"]}" type="video/mp4" controls preload="metadata" playsinline></video></div>\n'

    # 角色音色
    voices_html = ""
    for item in audio_voices:
        ext = item["filename"].split(".")[-1].lower()
        mime_type = f"audio/{ext}" if ext != "flac" else "audio/flac"
        voices_html += f'      <div class="audio"><div class="tt">{item["name"]}</div>\n        <audio src="{item["url"]}" type="{mime_type}" controls preload="metadata"></audio></div>\n'

    # 备选音色
    misc_audio_html = ""
    for item in audio_misc:
        ext = item["filename"].split(".")[-1].lower()
        mime_type = f"audio/{ext}" if ext != "flac" else "audio/flac"
        misc_audio_html += f'      <div class="audio"><div class="tt">{item["name"]}</div>\n        <audio src="{item["url"]}" type="{mime_type}" controls preload="metadata"></audio></div>\n'

    # 进度百分比
    ep_pct = int(completed_eps / TOTAL_EPISODES * 100)
    seg_pct = int(completed_segs / total_segs * 100)
    char_pct = min(int(char_count / 5 * 100), 100)
    voice_pct = min(int(voice_count / 5 * 100), 100)
    scene_pct = min(int(scene_count / 8 * 100), 100)

    # 进度描述
    progress_hint = f"剧本与提示词层已 100% 就绪；成片层 {seg_pct}%（{completed_segs}/{total_segs} 段，{completed_eps}/{TOTAL_EPISODES} 集完成）。"

    # 里程碑（自动生成）
    milestone_items = []
    if completed_eps > 0:
        milestone_items.append(
            f'<div class="mil"><span class="tag rec">已完成</span><span>剧本规划（{TOTAL_EPISODES} 集）/ 镜头脚本（{total_segs} 段提示词）/ {char_count} 个角色定妆图 / {voice_count} 个角色音色 / {completed_eps} 集成片</span></div>'
        )
    milestone_items.append(
        f'<div class="mil"><span class="tag ing">进行中</span><span>视频成片批量制作中，当前已完成 {completed_segs} / {total_segs} 个镜头段</span></div>'
    )
    next_ep = completed_eps + 1
    if next_ep <= TOTAL_EPISODES:
        next_title = EPISODE_TITLES[next_ep - 1] if next_ep - 1 < len(EPISODE_TITLES) else f"第{next_ep}集"
        milestone_items.append(
            f'<div class="mil"><span class="tag warn">下一里程碑</span><span>EP{next_ep}《{next_title}》成片制作</span></div>'
        )
    milestones_html = "\n".join(milestone_items)

    # 资产缺口（自动生成）
    gap_items = []
    target_chars = ["林小溪", "陈阿公", "张导演", "神秘旅人", "小糯米"]
    char_names = [c["name"].split(" · ")[0] for c in characters]
    missing_chars = [c for c in target_chars if not any(c in n for n in char_names)]
    for c in missing_chars[:3]:
        gap_items.append(f'<tr><td class="pri">🔴 P0</td><td>{c}定妆图</td><td>相关集次</td><td>待生成</td></tr>')

    if scene_count < 8:
        gap_items.append(f'<tr><td class="pri">🟡 P1</td><td>{8 - scene_count} 个场景图</td><td>全集次场景</td><td>待补充</td></tr>')

    if voice_count < 5:
        gap_items.append(f'<tr><td class="pri">🟡 P1</td><td>{5 - voice_count} 个角色音色</td><td>相关集次</td><td>待录制/生成</td></tr>')

    if not gap_items:
        gap_items.append('<tr><td class="pri">🟢</td><td>暂无缺口</td><td>-</td><td>资产齐全</td></tr>')

    gaps_html = "\n".join(gap_items)

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>{PROJECT_TITLE} · 素材与进度看板</title>
<style>
  :root{{
    --bg:#f4f5f7;--card:#fff;--ink:#1c2333;--sub:#6b7280;--line:#eceef2;
    --accent:#b8551f;--green:#0e7a5f;--gold:#c9962e;--blue:#2f6fed;--red:#e11d48;
    --radius:14px;--shadow:0 2px 10px rgba(20,30,60,.06);
  }}
  *{{box-sizing:border-box;margin:0;padding:0;-webkit-tap-highlight-color:transparent}}
  html,body{{background:var(--bg);color:var(--ink);font-family:-apple-system,BlinkMacSystemFont,"PingFang SC","HarmonyOS Sans SC","Microsoft YaHei",sans-serif;line-height:1.6}}
  body{{padding:18px 14px 40px}}
  .wrap{{max-width:760px;margin:0 auto}}
  header{{display:flex;align-items:center;justify-content:space-between;gap:10px;padding:6px 2px 14px}}
  header h1{{font-size:20px;font-weight:800}}
  header h1 small{{display:block;font-size:12px;font-weight:500;color:var(--sub);margin-top:2px}}
  .badge{{background:linear-gradient(135deg,var(--accent),#e07b3f);color:#fff;font-size:12px;font-weight:600;padding:6px 12px;border-radius:999px;white-space:nowrap}}
  section{{background:var(--card);border-radius:var(--radius);box-shadow:var(--shadow);padding:16px 14px;margin-bottom:16px}}
  .s-title{{display:flex;align-items:center;gap:8px;font-size:16px;font-weight:700;margin-bottom:12px}}
  .s-title .dot{{width:8px;height:8px;border-radius:50%;flex:none}}
  .d-orange{{background:var(--accent)}}.d-green{{background:var(--green)}}.d-gold{{background:var(--gold)}}.d-blue{{background:var(--blue)}}.d-red{{background:var(--red)}}
  .hint{{font-size:12px;color:var(--sub);margin-top:8px}}

  /* 进度总览 */
  .overview{{display:grid;grid-template-columns:repeat(2,1fr);gap:10px}}
  .ov{{background:#f8f9fb;border-radius:10px;padding:12px}}
  .ov .k{{font-size:12px;color:var(--sub)}}
  .ov .v{{font-size:20px;font-weight:800;margin:2px 0 6px}}
  .bar{{height:6px;background:#e6e8ee;border-radius:99px;overflow:hidden}}
  .bar i{{display:block;height:100%;border-radius:99px;background:linear-gradient(90deg,var(--accent),#e07b3f)}}
  .bar.green i{{background:linear-gradient(90deg,var(--green),#22a580)}}
  .bar.blue i{{background:linear-gradient(90deg,var(--blue),#5b8def)}}
  .bar.gold i{{background:linear-gradient(90deg,var(--gold),#e0b555)}}
  .bar.red i{{background:linear-gradient(90deg,var(--red),#f25c7e)}}

  /* 分集矩阵 */
  .eps{{display:grid;grid-template-columns:repeat(2,1fr);gap:8px}}
  .ep{{display:flex;align-items:center;gap:8px;background:#f8f9fb;border:1px solid var(--line);border-radius:10px;padding:9px 10px;font-size:12.5px}}
  .ep .no{{font-weight:800;color:var(--sub);flex:none}}
  .ep .nm{{flex:1;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
  .ep .st{{font-size:11px;font-weight:600;padding:2px 8px;border-radius:999px;flex:none}}
  .st.done{{background:#e3f5ee;color:var(--green)}}
  .st.ready{{background:#fff3e0;color:var(--gold)}}
  .st.wait{{background:#eef0f4;color:#9aa1ad}}
  .legend{{display:flex;gap:12px;flex-wrap:wrap;margin-top:10px;font-size:12px;color:var(--sub)}}

  /* 图片网格 */
  .imgs{{display:grid;grid-template-columns:repeat(3,1fr);gap:8px}}
  .img{{position:relative;border-radius:10px;overflow:hidden;background:#f1f2f5;aspect-ratio:1/1.1}}
  .img img{{width:100%;height:100%;object-fit:cover;display:block}}
  .img .cap{{position:absolute;left:0;right:0;bottom:0;background:linear-gradient(transparent,rgba(0,0,0,.72));color:#fff;font-size:10.5px;padding:14px 6px 5px;line-height:1.3}}
  @media(min-width:560px){{.imgs{{grid-template-columns:repeat(4,1fr)}}}}

  /* 视频 */
  .videos{{display:flex;flex-direction:column;gap:10px}}
  .video{{background:#f8f9fb;border:1px solid var(--line);border-radius:10px;overflow:hidden}}
  .video .tt{{font-size:13px;font-weight:600;padding:8px 10px 0}}
  .video video{{width:100%;display:block;aspect-ratio:16/9;background:#000}}

  /* 音频 */
  .audios{{display:flex;flex-direction:column;gap:8px}}
  .audio{{background:#f8f9fb;border:1px solid var(--line);border-radius:10px;padding:8px 10px}}
  .audio .tt{{font-size:12.5px;font-weight:600;margin-bottom:4px}}
  .audio audio{{width:100%;height:34px}}

  /* 里程碑 / 缺口 */
  .list2{{display:flex;flex-direction:column;gap:8px}}
  .mil{{display:flex;gap:10px;font-size:13px;background:#f8f9fb;border-radius:10px;padding:10px}}
  .mil .tag{{flex:none;font-size:11px;font-weight:600;padding:2px 8px;border-radius:999px;height:fit-content;margin-top:2px}}
  .tag.rec{{background:#e3f5ee;color:var(--green)}}
  .tag.ing{{background:#fff3e0;color:var(--gold)}}
  .tag.warn{{background:#ffecef;color:var(--red)}}
  table{{width:100%;border-collapse:collapse;font-size:12.5px}}
  th,td{{text-align:left;padding:7px 6px;border-bottom:1px solid var(--line)}}
  th{{color:var(--sub);font-weight:600;font-size:11.5px;white-space:nowrap}}
  td.pri{{font-weight:700;white-space:nowrap}}
  footer{{text-align:center;font-size:11px;color:#aab0bc;margin-top:20px}}
</style>
</head>
<body>
<div class="wrap">

  <header>
    <h1>{PROJECT_TITLE}
      <small>{PROJECT_SUBTITLE}</small>
    </h1>
    <div class="badge">数据截至 {today}</div>
  </header>

  <!-- 进度总览 -->
  <section>
    <div class="s-title"><span class="dot d-orange"></span>项目整体完成度</div>
    <div class="overview">
      <div class="ov"><div class="k">剧集完成</div><div class="v">{completed_eps} / {TOTAL_EPISODES}</div><div class="bar"><i style="width:{ep_pct}%"></i></div></div>
      <div class="ov"><div class="k">镜头段完成</div><div class="v">{completed_segs} / {total_segs}</div><div class="bar blue"><i style="width:{seg_pct}%"></i></div></div>
      <div class="ov"><div class="k">角色定妆图</div><div class="v">{char_count} / 5</div><div class="bar red"><i style="width:{char_pct}%"></i></div></div>
      <div class="ov"><div class="k">角色音色</div><div class="v">{voice_count} / 5</div><div class="bar green"><i style="width:{voice_pct}%"></i></div></div>
      <div class="ov"><div class="k">场景图</div><div class="v">{scene_count} / 8</div><div class="bar gold"><i style="width:{scene_pct}%"></i></div></div>
      <div class="ov"><div class="k">剧本 + 提示词</div><div class="v">100%</div><div class="bar green"><i style="width:100%"></i></div></div>
    </div>
    <div class="hint">{progress_hint}</div>
  </section>

  <!-- 分集矩阵 -->
  <section>
    <div class="s-title"><span class="dot d-blue"></span>分集实施矩阵（{TOTAL_EPISODES} 集）</div>
    <div class="eps">
{eps_html.rstrip()}
    </div>
    <div class="legend"><span>🟢 成片完成</span><span>🟡 部分段完成</span><span>⚪ 未开始</span></div>
  </section>

  <!-- 角色定妆图 -->
  <section>
    <div class="s-title"><span class="dot d-green"></span>{ASSET_CATEGORIES['characters']['title']}</div>
    <div class="imgs">
{chars_html.rstrip()}
    </div>
    <div class="hint">{ASSET_CATEGORIES['characters']['hint']}</div>
  </section>

  <!-- 嵩口真实场景图 -->
  <section>
    <div class="s-title"><span class="dot d-gold"></span>{ASSET_CATEGORIES['scenes']['title']}</div>
    <div class="imgs">
{scenes_html.rstrip()}
    </div>
  </section>

  <!-- 视频成片 -->
  <section>
    <div class="s-title"><span class="dot d-red"></span>{ASSET_CATEGORIES['videos_drama']['title']}</div>
    <div class="videos">
{drama_html.rstrip()}
    </div>
    <div class="hint">{ASSET_CATEGORIES['videos_drama']['hint']}</div>
  </section>

  <!-- 其他视频素材 -->
  <section>
    <div class="s-title"><span class="dot d-red"></span>{ASSET_CATEGORIES['videos_misc']['title']}</div>
    <div class="videos">
{misc_videos_html.rstrip()}
    </div>
  </section>

  <!-- 角色音色 -->
  <section>
    <div class="s-title"><span class="dot d-blue"></span>{ASSET_CATEGORIES['audio_voices']['title']}</div>
    <div class="audios">
{voices_html.rstrip()}
    </div>
  </section>

  <!-- 备选音色 -->
  <section>
    <div class="s-title"><span class="dot d-blue"></span>{ASSET_CATEGORIES['audio_misc']['title']}</div>
    <div class="audios">
{misc_audio_html.rstrip()}
    </div>
  </section>

  <!-- 里程碑与下一步 -->
  <section>
    <div class="s-title"><span class="dot d-green"></span>关键节点与下一步</div>
    <div class="list2">
{milestones_html}
    </div>
  </section>

  <!-- 资产缺口 -->
  <section>
    <div class="s-title"><span class="dot d-red"></span>资产缺口清单</div>
    <table>
      <tr><th>优先级</th><th>资产</th><th>影响集次</th><th>状态</th></tr>
{gaps_html}
    </table>
  </section>

  <footer>{PROJECT_TITLE}看板 · 由 update_dashboard.py 自动生成 · 数据截至 {today}</footer>
</div>
</body>
</html>
"""


# ─── 主逻辑 ─────────────────────────────────────────────────────────

def main():
    import argparse
    parser = argparse.ArgumentParser(description="嵩口项目可视化看板自动更新脚本")
    parser.add_argument("--output", "-o", help="输出 HTML 文件路径", default=str(OUTPUT_FILE))
    parser.add_argument("--watch", "-w", action="store_true", help="监控模式：检测到文件变化自动更新")
    parser.add_argument("--interval", "-i", type=int, default=3, help="监控模式下的检查间隔（秒）")
    args = parser.parse_args()

    output_path = Path(args.output)

    if args.watch:
        print(f"👀 监控模式启动，检查间隔 {args.interval} 秒")
        print(f"📁 监控目录：{REPO_ROOT / 'images'}, {REPO_ROOT / 'videos'}, {REPO_ROOT / 'audio'}")
        print(f"📄 输出文件：{output_path}")
        print("按 Ctrl+C 退出\n")

        last_hash = ""
        while True:
            # 计算所有素材目录的快照
            all_exts = {".png", ".jpg", ".jpeg", ".webp", ".mp4", ".mov", ".webm", ".flac", ".mp3", ".wav", ".m4a"}
            current_hash = ""
            for d in ["images", "videos", "audio"]:
                current_hash += dir_snapshot(REPO_ROOT / d, all_exts)

            if current_hash != last_hash:
                html = generate_html()
                output_path.write_text(html, encoding="utf-8")
                now = datetime.now().strftime("%H:%M:%S")
                print(f"✅ [{now}] 检测到素材变化，看板已更新 → {output_path.name}")
                last_hash = current_hash

            time.sleep(args.interval)
    else:
        # 单次生成
        html = generate_html()
        output_path.write_text(html, encoding="utf-8")
        print(f"✅ 看板已生成：{output_path}")

        # 统计信息
        characters = scan_files("characters", ASSET_CATEGORIES["characters"])
        scenes = scan_files("scenes", ASSET_CATEGORIES["scenes"])
        videos_drama = scan_files("videos_drama", ASSET_CATEGORIES["videos_drama"])
        videos_misc = scan_files("videos_misc", ASSET_CATEGORIES["videos_misc"])
        audio_voices = scan_files("audio_voices", ASSET_CATEGORIES["audio_voices"])
        audio_misc = scan_files("audio_misc", ASSET_CATEGORIES["audio_misc"])

        print(f"   角色定妆图：{len(characters)} 张")
        print(f"   场景图：{len(scenes)} 张")
        print(f"   短剧视频：{len(videos_drama)} 个")
        print(f"   其他视频：{len(videos_misc)} 个")
        print(f"   专属音色：{len(audio_voices)} 个")
        print(f"   备选音色：{len(audio_misc)} 个")


if __name__ == "__main__":
    main()
