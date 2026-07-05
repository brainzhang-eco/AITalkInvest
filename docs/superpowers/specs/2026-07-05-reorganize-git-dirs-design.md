# Design Spec: Reorganize Git Directory Structure

## Goal
Reorganize the repository directory structure to:
1. Rename the current `docs/` directory to `sources/`.
2. Move the chapter markdown files (`00_序言.md` through `09_结语.md`) and compiled book markdown (`韭韭归一：老亢给小白的投基兵法.md`) and HTML (`韭韭归一：老亢给小白的投基兵法.html`) files from the root directory into a new `docs/` directory.
3. Update all script paths, documentation, and configuration references to match the new structure.

---

## Detailed Plan

### 1. File & Directory Renames (Git-tracked)
* Move the current `docs/` directory to `sources/`:
  `git mv docs sources`
* Create a new `docs/` directory:
  `mkdir docs`
* Move root-level book files into `docs/`:
  `git mv 00_序言.md 01_第一回.md 02_第二回.md 03_第三回.md 04_第四回.md 05_第五回.md 06_第六回.md 07_第七回.md 08_第八回.md 09_结语.md 韭韭归一：老亢给小白的投基兵法.md 韭韭归一：老亢给小白的投基兵法.html docs/`

### 2. Script Updates (`scripts/build_book.py`)
Update references to markdown files and build targets:
* Path for chapters (`CHAPTERS` list items) should be read from the `docs/` directory.
* Path for outputs (`MD_OUTPUT` and `HTML_OUTPUT`) should be written to the `docs/` directory.
* Adjust path joins accordingly:
  ```python
  MD_OUTPUT = os.path.join("docs", f"{BOOK_TITLE}.md")
  HTML_OUTPUT = os.path.join("docs", f"{BOOK_TITLE}.html")
  ```
  And prefix input files with `docs/` when reading them:
  ```python
  os.path.join("docs", chapter)
  ```

### 3. Documentation Updates
* **`README.md`**:
  * Update description of chapter files, HTML version, and Markdown collection to reference the `docs/` directory.
  * Update description of rules/materials from `docs/` to `sources/`.
* **`README_EXPORT.md`**:
  * Update path references for HTML and MD compiled books to target the `docs/` directory.

### 4. Configuration & Other Updates
* **`.gitignore`**:
  * Update `docs/superpowers` ignore rule to `sources/superpowers`.

---

## Verification Plan

### Manual Verification
1. Run build script to generate book formats:
   ```bash
   conda activate AITalkInvest
   python scripts/build_book.py
   ```
2. Verify that `docs/韭韭归一：老亢给小白的投基兵法.md` and `docs/韭韭归一：老亢给小白的投基兵法.html` are correctly compiled and match original contents.
3. Run `git status` and `git diff` to verify only the expected changes are present.
