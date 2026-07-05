# Git Directory Reorganization Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Reorganize the repository directory structure by renaming `docs` to `sources`, moving book chapters and outputs into a new `docs/` directory, and updating build scripts and documentation.

**Architecture:** Use git native command line moves to preserve file history, update paths in python build script, and modify markdown documents to point to new directories.

**Tech Stack:** Git, Python, Shell.

## Global Constraints
* Always use `git mv` instead of standard `mv` to preserve git history.
* Ensure all links in updated documentation are correct.
* Use `conda activate AITalkInvest` before running python commands.

---

### Task 1: Rename and Move Files in Git

**Files:**
- Modify: directory layout in git

- [ ] **Step 1: Rename docs to sources**
  Run:
  ```bash
  git mv docs sources
  ```
  Expected: Git tracks the rename from `docs` to `sources`.

- [ ] **Step 2: Create new docs folder**
  Run:
  ```bash
  mkdir docs
  ```
  Expected: A new empty directory `docs/` is created at the root.

- [ ] **Step 3: Move chapter files and compiled book files to new docs folder**
  Run:
  ```bash
  git mv 00_序言.md 01_第一回.md 02_第二回.md 03_第三回.md 04_第四回.md 05_第五回.md 06_第六回.md 07_第七回.md 08_第八回.md 09_结语.md 韭韭归一：老亢给小白的投基兵法.md 韭韭归一：老亢给小白的投基兵法.html docs/
  ```
  Expected: Files are moved into `docs/`.

- [ ] **Step 4: Verify git status**
  Run:
  ```bash
  git status
  ```
  Expected: Shows renamed `docs` files to `sources` files, and moved chapter files as renamed to `docs/`.

- [ ] **Step 5: Commit intermediate progress**
  Run:
  ```bash
  git commit -m "refactor: rename docs to sources and move chapter markdown files to docs/"
  ```

---

### Task 2: Update Build Script (`scripts/build_book.py`)

**Files:**
- Modify: `scripts/build_book.py`

- [ ] **Step 1: Modify build script path config**
  Modify [scripts/build_book.py](file:///opt/brainzhang/AITalkInvest/scripts/build_book.py) to read chapters from `docs/` and write outputs to `docs/`.
  Find lines:
  ```python
  MD_OUTPUT = f"{BOOK_TITLE}.md"
  HTML_OUTPUT = f"{BOOK_TITLE}.html"
  ```
  Replace with:
  ```python
  MD_OUTPUT = os.path.join("docs", f"{BOOK_TITLE}.md")
  HTML_OUTPUT = os.path.join("docs", f"{BOOK_TITLE}.html")
  ```

  Find lines:
  ```python
      for chapter in CHAPTERS:
          with open(chapter, "r", encoding="utf-8") as f:
  ```
  Replace with:
  ```python
      for chapter in CHAPTERS:
          with open(os.path.join("docs", chapter), "r", encoding="utf-8") as f:
  ```

  Find lines:
  ```python
          for chapter in CHAPTERS:
              with open(chapter, "r", encoding="utf-8") as c:
  ```
  Replace with:
  ```python
          for chapter in CHAPTERS:
              with open(os.path.join("docs", chapter), "r", encoding="utf-8") as c:
  ```

  Find lines:
  ```python
      for i, chapter in enumerate(CHAPTERS):
          with open(chapter, "r", encoding="utf-8") as f:
  ```
  Replace with:
  ```python
      for i, chapter in enumerate(CHAPTERS):
          with open(os.path.join("docs", chapter), "r", encoding="utf-8") as f:
  ```

- [ ] **Step 2: Run verification test**
  Run:
  ```bash
  python scripts/build_book.py
  ```
  Expected: Output `Build successful: - docs/韭韭归一：老亢给小白的投基兵法.md - docs/韭韭归一：老亢给小白的投基兵法.html`. No python errors.

- [ ] **Step 3: Commit changes**
  Run:
  ```bash
  git add scripts/build_book.py
  git commit -m "refactor: update build_book.py path references to docs/"
  ```

---

### Task 3: Update Documentation and Gitignore

**Files:**
- Modify: `README.md`
- Modify: `README_EXPORT.md`
- Modify: `.gitignore`

- [ ] **Step 1: Modify README.md**
  Modify [README.md](file:///opt/brainzhang/AITalkInvest/README.md) lines 28-31:
  ```markdown
  - `00_序言.md` - `09_结语.md`：全书十章回源码。
  - `韭韭归一：老亢给小白的投基兵法.html`：精排网页版（推荐阅读，支持公式、图片与分页）。
  - `韭韭归一：老亢给小白的投基兵法.md`：全书 Markdown 合集。
  - `docs/`：包含原始投资规则（rules.md）及相关素材。
  ```
  Replace with:
  ```markdown
  - `docs/`：包含全书十章回源码、全书 Markdown 合集、精排网页版等相关素材。
  - `sources/`：包含原始投资规则（rules.md）及其他参考资料。
  ```

- [ ] **Step 2: Modify README_EXPORT.md**
  Modify [README_EXPORT.md](file:///opt/brainzhang/AITalkInvest/README_EXPORT.md):
  Replace occurrences of `韭韭归一：老亢给小白的投基兵法.html` and `韭韭归一：老亢给小白的投基兵法.md` with `docs/韭韭归一：老亢给小白的投基兵法.html` and `docs/韭韭归一：老亢给小白的投基兵法.md`.

- [ ] **Step 3: Modify .gitignore**
  Modify [.gitignore](file:///opt/brainzhang/AITalkInvest/.gitignore):
  Replace `docs/superpowers` with `sources/superpowers`.

- [ ] **Step 4: Verify everything builds and looks correct**
  Run:
  ```bash
  git status
  ```
  Expected: Clean status or only tracked changes.

- [ ] **Step 5: Commit changes**
  Run:
  ```bash
  git add README.md README_EXPORT.md .gitignore
  git commit -m "docs: update directory references in docs and config"
  ```
