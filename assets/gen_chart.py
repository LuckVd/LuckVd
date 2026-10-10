#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成开源贡献柱状图（GitHub 原生配色，浅色/深色两版）。数据: merged PRs by repo, 2026-10 查询。"""
import os

DATA = [
    ("Tencent/WeKnora", 12),
    ("dsh 生态插件", 3),
    ("manaflow-ai/cmux", 2),
    ("alipay/xAST 基准", 1),
    ("agentGroup", 1),
 ("修仙世界模拟器", 1),
]

W, PAD = 880, 16
LABEL_X, TRACK_X, TRACK_W = 16, 238, 594
BAR_H, PITCH = 16, 40
HEAD_H = 40
H = HEAD_H + PITCH * len(DATA) + PAD

THEMES = {
    "light": dict(track="#eaeef2", bar="#2da44e", label="#57606a", value="#24292f", head="#6e7781"),
    "dark":  dict(track="#21262d", bar="#3fb950", label="#8b949e", value="#e6edf3", head="#7d8590"),
}

FONT = "-apple-system, 'Segoe UI', 'Noto Sans', 'PingFang SC', 'Microsoft YaHei', 'WenQuanYi Micro Hei', sans-serif"
total = sum(n for _, n in DATA)
vmax = max(n for _, n in DATA)

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;")

for name, t in THEMES.items():
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="{FONT}">']
    s.append(f'<text x="{LABEL_X}" y="24" font-size="11" letter-spacing="2" fill="{t["head"]}">OPEN SOURCE · MERGED PULL REQUESTS</text>')
    s.append(f'<text x="{W-PAD}" y="24" font-size="11" fill="{t["head"]}" text-anchor="end">{total} merged · {len(DATA)} repos</text>')
    for i, (label, n) in enumerate(DATA):
        cy = HEAD_H + i * PITCH + BAR_H / 2
        bw = TRACK_W * n / vmax
        s.append(f'<text x="{LABEL_X}" y="{cy + 4.5:.0f}" font-size="13" fill="{t["label"]}">{esc(label)}</text>')
        s.append(f'<rect x="{TRACK_X}" y="{HEAD_H + i * PITCH}" width="{TRACK_W}" height="{BAR_H}" rx="8" fill="{t["track"]}"/>')
        s.append(f'<rect x="{TRACK_X}" y="{HEAD_H + i * PITCH}" width="{bw:.0f}" height="{BAR_H}" rx="8" fill="{t["bar"]}"/>')
        s.append(f'<text x="{W-PAD}" y="{cy + 4.5:.0f}" font-size="13" font-weight="600" fill="{t["value"]}" text-anchor="end">{n}</text>')
    s.append('</svg>')
    out = os.path.join(os.path.dirname(__file__), f"oss-contrib-{name}.svg")
    with open(out, "w") as f:
        f.write("".join(s))
    print("wrote", out, f"{W}x{H}")
