#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""拉取真实数据并写入 data.json，供 gen_cards.py / gen_chart.py 消费。
本地跑（gh 已登录）或 Actions 里跑（GH_TOKEN）皆可。"""
import collections
import json
import os
import subprocess

OWNER = "LuckVd"
HERE = os.path.dirname(os.path.abspath(__file__))

# 柱状图行标签美化 + dsh 生态聚合
LABELS = {
    "alipay/ant-application-security-testing-benchmark": "alipay/xAST 基准",
}
DSH_ECOSYSTEM = {
    "xbzbing/dsh-auth-gateway",
    "omdsh-dev/DSH-better-sidebar",
    "awesome-dsh-plugin/awesome-dsh-plugin",
}
FEATURED = ["LuckVd.github.io", "dsh-taskflow", "dsh-btw", "DeepVuln", "CSRFscanver"]


def gh(path):
    out = subprocess.run(["gh", "api", path], capture_output=True, text=True, check=True)
    return json.loads(out.stdout)


def merged_pr_groups():
    data = gh(f"search/issues?q=type:pr+author:{OWNER}+is:merged&per_page=100")
    counts = collections.Counter(
        i["repository_url"].split("/repos/")[-1] for i in data.get("items", [])
    )
    rows, dsh_n, dsh_repos = [], 0, 0
    for repo, n in counts.items():
        if repo.startswith(OWNER + "/"):
            continue  # 自己仓库的 PR 不算"开源贡献"
        if repo in DSH_ECOSYSTEM:
            dsh_n += n
            dsh_repos += 1
            continue
        rows.append([LABELS.get(repo, repo), n, 1])
    if dsh_n:
        rows.append(["dsh 生态插件", dsh_n, dsh_repos])
    rows.sort(key=lambda r: -r[1])
    total_pr = sum(n for _, n, _ in rows)
    total_projects = sum(p for _, _, p in rows)
    return {"rows": [[l, n] for l, n, _ in rows], "total_pr": total_pr, "total_projects": total_projects}


def featured_repos():
    repos = {}
    for name in FEATURED:
        r = gh(f"repos/{OWNER}/{name}")
        repos[name] = {
            "desc": r.get("description") or "",
            "stars": r.get("stargazers_count", 0),
            "updated": (r.get("pushed_at") or "")[:7],
            "lang": r.get("language") or "",
        }
    return repos


def language_share():
    repos = gh(f"users/{OWNER}/repos?per_page=100")
    langs = collections.Counter()
    for r in repos:
        if r.get("fork"):
            continue  # fork 不算自己的语言
        try:
            for k, v in gh(f"repos/{r['full_name']}/languages").items():
                langs[k] += v
        except Exception:
            continue
    total = sum(langs.values()) or 1
    top = [[k, round(v * 100.0 / total, 1)] for k, v in langs.most_common(6)]
    if top:
        drift = round(100.0 - sum(p for _, p in top), 1)
        top[0][1] = round(top[0][1] + drift, 1)  # 补齐到 100%
    return top


def main():
    data = {
        "chart": merged_pr_groups(),
        "repos": featured_repos(),
        "langs": language_share(),
        "generated_at": __import__("datetime").datetime.utcnow().strftime("%Y-%m-%d"),
    }
    with open(os.path.join(HERE, "data.json"), "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    print("data.json written:",
          f"{data['chart']['total_pr']} PRs / {data['chart']['total_projects']} projects,",
          f"{len(data['langs'])} langs")


if __name__ == "__main__":
    main()
