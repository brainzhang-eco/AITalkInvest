# Zensical Static Site Setup and Deployment Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Configure and compile the repository as a static website using Zensical, and deploy it to GitHub Pages with the custom domain `invest.brainz.fun` using GitHub Actions.

**Architecture:** Create a `zensical.toml` configuration, add a `docs/index.md` home page, verify local builds, and deploy using a GitHub Actions workflow with `peaceiris/actions-gh-pages`.

**Tech Stack:** Python 3.12, Zensical, GitHub Actions, Git.

## Global Constraints
* Always use `conda activate AITalkInvest` before running python/pip commands.
* Ensure all links in navigation and generated index are correct.
* Make sure `site/` folder is not committed to the repo (add to gitignore).

---

### Task 1: Install Zensical and Create Configuration

**Files:**
- Create: `zensical.toml`
- Modify: `.gitignore`

- [ ] **Step 1: Install Zensical package**
  Run:
  ```bash
  conda run -n AITalkInvest pip install zensical
  ```
  Expected: Installation finishes successfully.

- [ ] **Step 2: Create Zensical configuration**
  Create [zensical.toml](file:///opt/brainzhang/AITalkInvest/zensical.toml):
  ```toml
  [project]
  site_name = "韭韭归一：老亢给小白的投基兵法"
  site_url = "https://invest.brainz.fun/"
  docs_dir = "docs"

  [[project.nav]]
  "简介" = "index.md"
  "序言" = "00_序言.md"
  "第一回" = "01_第一回.md"
  "第二回" = "02_第二回.md"
  "第三回" = "03_第三回.md"
  "第四回" = "04_第四回.md"
  "第五回" = "05_第五回.md"
  "第六回" = "06_第六回.md"
  "第七回" = "07_第七回.md"
  "第八回" = "08_第八回.md"
  "结语" = "09_结语.md"
  ```

- [ ] **Step 3: Ignore build directory in gitignore**
  Modify [.gitignore](file:///opt/brainzhang/AITalkInvest/.gitignore) to add `/site/` to prevent committing the generated site.
  Add at the bottom:
  ```
  # Zensical build output
  /site/
  ```

- [ ] **Step 4: Verify Zensical command**
  Run:
  ```bash
  conda run -n AITalkInvest zensical --help
  ```
  Expected: Zensical help menu is displayed.

- [ ] **Step 5: Commit changes**
  Run:
  ```bash
  git add zensical.toml .gitignore
  git commit -m "chore: install and configure Zensical static site generator"
  ```

---

### Task 2: Create Landing Page and Build Locally

**Files:**
- Create: `docs/index.md`

- [ ] **Step 1: Create docs/index.md landing page**
  Create [docs/index.md](file:///opt/brainzhang/AITalkInvest/docs/index.md) by copying [README.md](file:///opt/brainzhang/AITalkInvest/README.md) contents, but remove developer-focused sections ("项目结构", "PDF下载", "导出建议") to keep it polished for web readers.

- [ ] **Step 2: Build the site locally**
  Run:
  ```bash
  conda run -n AITalkInvest zensical build --clean
  ```
  Expected: Success output showing site built in `site/` folder.

- [ ] **Step 3: Verify build output**
  Run:
  ```bash
  ls -la site/index.html
  ```
  Expected: The file exists and contains the HTML compiled from `docs/index.md`.

- [ ] **Step 4: Commit changes**
  Run:
  ```bash
  git add docs/index.md
  git commit -m "docs: add index page for website"
  ```

---

### Task 3: Set up GitHub Actions CI/CD

**Files:**
- Create: `.github/workflows/deploy.yml`

- [ ] **Step 1: Create deploy workflow**
  Create [.github/workflows/deploy.yml](file:///opt/brainzhang/AITalkInvest/.github/workflows/deploy.yml):
  ```yaml
  name: Deploy Zensical Site to GitHub Pages

  on:
    push:
      branches:
        - main

  permissions:
    contents: write

  jobs:
    deploy:
      runs-on: ubuntu-latest
      steps:
        - name: Checkout repository
          uses: actions/checkout@v4

        - name: Set up Python
          uses: actions/setup-python@v5
          with:
            python-version: '3.12'

        - name: Install dependencies
          run: |
            python -m pip install --upgrade pip
            pip install zensical

        - name: Build static site
          run: |
            zensical build --clean

        - name: Deploy to GitHub Pages
          uses: peaceiris/actions-gh-pages@v3
          with:
            github_token: ${{ secrets.GITHUB_TOKEN }}
            publish_dir: ./site
            cname: invest.brainz.fun
  ```

- [ ] **Step 2: Commit deployment configuration**
  Run:
  ```bash
  git add .github/workflows/deploy.yml
  git commit -m "ci: add GitHub Actions workflow for Pages deployment"
  ```
