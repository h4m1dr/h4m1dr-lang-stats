# 🧬 h4m1dr – Top Languages Dashboard

This repository automatically generates an SVG chart showing my **top programming languages**
based on all my public GitHub repositories.

The SVG is updated regularly using **GitHub Actions** and the GitHub API.

---


## PR0DUC71V17Y 4N4LY71C5
Powered by WakaTime + GitHub Actions (auto-updated daily)

<!--START_SECTION:waka-->
<!-- WakaTime block will be injected here by GitHub Actions -->
<!--END_SECTION:waka-->

---

## 📈 W33KLY G17HUB 4C71V17Y
Real GitHub contributions for the last 7 days (commits, PRs, issues, etc.)

```text
Weekly GitHub Activity (contributions)
Thu 7  | ██████████████████████████████
Fri 0  | ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
Sat 0  | ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
Sun 0  | ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
Mon 2  | ████████░░░░░░░░░░░░░░░░░░░░░░
Tue 6  | █████████████████████████░░░░░
Wed 5  | █████████████████████░░░░░░░░░
````

## 📉 M0N7HLY G17HUB 4C71V17Y (L457 12 M0N7H5)

Real GitHub contributions aggregated monthly.

```text
Monthly GitHub Activity (last 12 months)
Jan 2025 | ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 0
Feb 2025 | █████████░░░░░░░░░░░░░░░░░░░░░ 4
Mar 2025 | ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 0
Apr 2025 | ████░░░░░░░░░░░░░░░░░░░░░░░░░░ 2
May 2025 | ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 0
Jun 2025 | ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 0
Jul 2025 | ████░░░░░░░░░░░░░░░░░░░░░░░░░░ 2
Aug 2025 | ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 0
Sep 2025 | ████░░░░░░░░░░░░░░░░░░░░░░░░░░ 2
Oct 2025 | ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 0
Nov 2025 | ████████████████░░░░░░░░░░░░░░ 7
Dec 2025 | ██████████████████████████████ 13
```


---

## 📊 Top Languages (by bytes)

> Data is aggregated from all non-fork public repositories under **@h4m1dr**.

![Top Languages](https://raw.githubusercontent.com/h4m1dr/h4m1dr-lang-stats/main/assets/top_langs.svg)

---

## ⚙️ How it works

- `scripts/generate_top_langs_svg.py`  
  Fetches all repositories for `@h4m1dr`, calls the `/languages` API for each,
  aggregates the byte counts per language, and generates a clean SVG bar chart.

- `.github/workflows/update_langs.yml`  
  Runs on a schedule (cron) or manually via the **Actions** tab, regenerates the SVG,
  and commits it back to this repository.

---

## 🔗 Usage in other READMEs

In any other README (for example, in your main profile repo `h4m1dr/h4m1dr`),  
you can embed this chart with:

```md
![Top Languages](https://raw.githubusercontent.com/h4m1dr/h4m1dr-lang-stats/main/assets/top_langs.svg)
````

---

## 🛠 Roadmap

* [ ] Add per-repository breakdown
* [ ] Add support for grouping similar languages (e.g. TS/JS)
* [ ] Add alternative themes (dark / light)
* [ ] Add donut-style chart option
