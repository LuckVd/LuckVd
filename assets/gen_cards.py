#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""自绘 GitHub 风格卡片（440x160，浅色/深色）：项目卡 + 博客卡 + 语言占比卡。
与 oss-contrib 柱状图同一设计语言。数据来源见各 CARD / LANGS 定义。"""
import math
import os

W, H, PAD = 440, 160, 16
INNER = W - PAD * 2
FONT = "-apple-system, 'Segoe UI', 'Noto Sans', 'PingFang SC', 'Microsoft YaHei', 'WenQuanYi Micro Hei', sans-serif"

LANG_COLOR = {
    "TypeScript": "#3178c6", "JavaScript": "#f1e05a", "Python": "#3572A5", "Hexo": "#62E4B5",
}

THEMES = {
    "light": dict(bg="#ffffff", border="#d0d7de", title="#0969da", text="#57606a",
                  muted="#8c959f", star="#57606a", track="#eaeef2"),
    "dark":  dict(bg="#0d1117", border="#30363d", title="#4493f8", text="#8b949e",
                  muted="#6e7681", star="#8b949e", track="#21262d"),
}

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;")

def units(s):
    return sum(1.0 if ord(c) > 0x2E80 else 0.55 for c in s)

def wrap(s, maxu=32.5, lines=2):
    out, cur, cu = [], "", 0.0
    for ch in s:
        w = 1.0 if ord(ch) > 0x2E80 else 0.55
        if cu + w > maxu and cur:
            out.append(cur)
            cur, cu = "", 0.0
        cur += ch
        cu += w
        if len(out) == lines:
            break
    out.append(cur)
    if len(out) > lines:
        out = out[:lines]
        last = out[-1]
        while units(last) > maxu - 1.5:
            last = last[:-1]
        out[-1] = last + "…"
    return out[:lines]

REPO_ICON = ("M2 2.5A2.5 2.5 0 0 1 4.5 0h8.75a.75.75 0 0 1 .75.75v12.5a.75.75 0 0 1-.75.75h-2.5"
             "a.75.75 0 0 1 0-1.5h1.75v-2h-8a1 1 0 0 0-.714 1.7.75.75 0 1 1-1.072 1.05A2.495 2.495 0 0 1 2 11.5Z"
             "m10.5-1h-8a1 1 0 0 0-1 1v6.708A2.486 2.486 0 0 1 4.5 9h8Z")

def lang_dot_x(lang):
    return W - PAD - (units(lang) * 6.2 + 22)

def star_icon(x, y, c, r=5):
    pts = []
    for i in range(10):
        a = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.45
        pts.append(f"{x + rr * math.cos(a):.1f},{y + rr * math.sin(a):.1f}")
    return f'<polygon points="{" ".join(pts)}" fill="{c}"/>'

CARDS = [
    dict(slug="blog", link="https://luckvd.github.io",
         title="个人博客 · LuckVd.github.io", lang="Hexo",
         desc="Hexo 驱动的个人博客：技术笔记、项目展示与折腾记录。",
         stars=0, updated="2026-10"),
    dict(slug="dsh-taskflow", link="https://github.com/LuckVd/dsh-taskflow",
         title="dsh-taskflow", lang="TypeScript",
         desc="AI 合同式任务看板 · DeepSeek Harness Web 插件：AI 拆解/实现/举证，人工验收、打回迭代、状态留痕。",
         stars=0, updated="2026-10"),
    dict(slug="dsh-btw", link="https://github.com/LuckVd/dsh-btw",
         title="dsh-btw", lang="JavaScript",
         desc="DeepSeek Harness Web 插件 · BTW 侧问面板：随手弹窗追问，独立一次性会话，不污染主对话上下文。",
         stars=2, updated="2026-09"),
    dict(slug="DeepVuln", link="https://github.com/LuckVd/DeepVuln",
         title="DeepVuln", lang="Python",
         desc="AI 驱动的多层智能漏洞挖掘系统：情报层 + 分析层 + 扫描流水线 + Web 管理平台。",
         stars=0, updated="2026-09"),
    dict(slug="CSRFscanver", link="https://github.com/LuckVd/CSRFscanver",
         title="CSRFscanver", lang="Python",
         desc="CSRF 漏洞扫描器（Python）。",
         stars=0, updated="2022-10"),
]

def gen_card(c, t):
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="{FONT}">']
    s.append(f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="8" fill="{t["bg"]}" stroke="{t["border"]}"/>')
    s.append(f'<svg x="{PAD}" y="21" width="15" height="15" viewBox="0 0 16 16">'
             f'<path fill="{t["muted"]}" d="{REPO_ICON}"/></svg>')
    s.append(f'<text x="{PAD+21}" y="33.5" font-size="14.5" font-weight="600" fill="{t["title"]}">{esc(c["title"])}</text>')
    dot = LANG_COLOR.get(c["lang"], "#8b949e")
    s.append(f'<circle cx="{lang_dot_x(c["lang"]):.0f}" cy="29" r="4.5" fill="{dot}"/>')
    s.append(f'<text x="{W-PAD}" y="33.5" font-size="11" fill="{t["muted"]}" text-anchor="end">{esc(c["lang"])}</text>')
    for i, line in enumerate(wrap(c["desc"])):
        s.append(f'<text x="{PAD}" y="{64 + i * 20}" font-size="12.5" fill="{t["text"]}">{esc(line)}</text>')
    if c["stars"]:
        s.append(star_icon(PAD + 5, 137, t["star"]))
        s.append(f'<text x="{PAD+16}" y="141" font-size="11" fill="{t["star"]}">{c["stars"]}</text>')
    s.append(f'<text x="{W-PAD}" y="141" font-size="10.5" fill="{t["muted"]}" text-anchor="end">Updated {c["updated"]}</text>')
    s.append('</svg>')
    return "".join(s)

LANGS = [("Python", 60.9), ("TypeScript", 16.4), ("HTML", 11.8),
         ("JavaScript", 7.0), ("Vue", 2.4), ("CSS", 1.5)]
LANG_BAR = {"Python": "#3572A5", "TypeScript": "#3178c6", "HTML": "#e34c26",
            "JavaScript": "#f1e05a", "Vue": "#41b883", "CSS": "#563d7c"}

def gen_langs(t):
    uid = t["bg"][1:]
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="{FONT}">']
    s.append(f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="8" fill="{t["bg"]}" stroke="{t["border"]}"/>')
    for i, bh in enumerate((6, 10, 14)):
        s.append(f'<rect x="{PAD + i*4.5}" y="{29 - bh/2}" width="3" height="{bh}" rx="1.5" fill="{t["muted"]}"/>')
    s.append(f'<text x="{PAD+22}" y="33.5" font-size="14.5" font-weight="600" fill="{t["title"]}">Most Used Languages</text>')
    s.append(f'<defs><clipPath id="langclip-{uid}"><rect x="{PAD}" y="50" width="{INNER}" height="12" rx="6"/></clipPath></defs>')
    s.append(f'<g clip-path="url(#langclip-{uid})">')
    x = PAD
    for lname, pct in LANGS:
        seg = INNER * pct / 100.0
        s.append(f'<rect x="{x:.1f}" y="50" width="{seg+0.5:.1f}" height="12" fill="{LANG_BAR[lname]}"/>')
        x += seg
    if x < PAD + INNER:
        s.append(f'<rect x="{x:.1f}" y="50" width="{PAD+INNER-x+1:.1f}" height="12" fill="{t["track"]}"/>')
    s.append('</g>')
    for i, (lname, pct) in enumerate(LANGS):
        col, row = divmod(i, 3)
        lx = PAD + col * 204
        ly = 90 + row * 24
        s.append(f'<circle cx="{lx+4}" cy="{ly-4}" r="4.5" fill="{LANG_BAR[lname]}"/>')
        s.append(f'<text x="{lx+16}" y="{ly}" font-size="12" fill="{t["text"]}">{esc(lname)}</text>')
        s.append(f'<text x="{lx+188}" y="{ly}" font-size="12" fill="{t["muted"]}" text-anchor="end">{pct}%</text>')
    s.append('</svg>')
    return "".join(s)

if __name__ == "__main__":
    here = os.path.dirname(__file__)
    for name, t in THEMES.items():
        for c in CARDS:
            with open(os.path.join(here, f"card-{c['slug']}-{name}.svg"), "w") as f:
                f.write(gen_card(c, t))
        with open(os.path.join(here, f"card-langs-{name}.svg"), "w") as f:
            f.write(gen_langs(t))
        print("wrote cards for", name)
