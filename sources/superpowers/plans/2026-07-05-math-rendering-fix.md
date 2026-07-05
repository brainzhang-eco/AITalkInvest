# Math Rendering Fix Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Enable LaTeX-style math rendering (both inline and display block formulas) on the Zensical static site and the compiled HTML book using MathJax.

**Architecture:** Configure Zensical arithmatex markdown extension and MathJax script, and update the Python build script to load MathJax in the output HTML template.

**Tech Stack:** Python, Zensical, HTML, JavaScript.

## Global Constraints
* Always use `conda activate AITalkInvest` before running python commands.
* Ensure all links and math tags are syntax-valid.

---

### Task 1: Set up Zensical Math Rendering Config

**Files:**
- Create: `docs/javascripts/mathjax.js`
- Modify: `zensical.toml`

- [ ] **Step 1: Create docs/javascripts/mathjax.js**
  Create the folder `docs/javascripts` and the file [docs/javascripts/mathjax.js](file:///opt/brainzhang/AITalkInvest/docs/javascripts/mathjax.js):
  ```javascript
  window.MathJax = {
    tex: {
      inlineMath: [["$", "$"], ["\\(", "\\)"]],
      displayMath: [["$$", "$$"], ["\\[", "\\]"]],
      processEscapes: true,
      processEnvironments: true
    },
    options: {
      ignoreHtmlClass: ".*",
      processHtmlClass: "arithmatex"
    }
  };
  ```

- [ ] **Step 2: Modify zensical.toml**
  Modify [zensical.toml](file:///opt/brainzhang/AITalkInvest/zensical.toml) to enable the arithmatex markdown extension and load the custom and CDN JavaScript:
  At the bottom of `[project]` add:
  ```toml
  extra_javascript = [
      "javascripts/mathjax.js",
      "https://unpkg.com/mathjax@3/es5/tex-mml-chtml.js"
  ]

  [project.markdown_extensions.pymdownx.arithmatex]
  generic = true
  ```

- [ ] **Step 3: Run Zensical build verification**
  Run:
  ```bash
  conda run -n AITalkInvest zensical build --clean
  ```
  Expected: Successful build without errors.

- [ ] **Step 4: Commit changes**
  Run:
  ```bash
  git add docs/javascripts/mathjax.js zensical.toml
  git commit -m "chore: enable math rendering in Zensical static site configuration"
  ```

---

### Task 2: Update Build Script and HTML Template

**Files:**
- Modify: `scripts/build_book.py`

- [ ] **Step 1: Update HTML Template inside scripts/build_book.py**
  Modify [scripts/build_book.py](file:///opt/brainzhang/AITalkInvest/scripts/build_book.py).
  Find lines in `HTML_TEMPLATE`:
  ```html
  </style>
  </head>
  ```
  Replace with:
  ```html
  </style>
  <script>
  window.MathJax = {
      tex: {
          inlineMath: [['$', '$'], ['\\(', '\\)']],
          displayMath: [['$$', '$$'], ['\\[', '\\]']],
          processEscapes: true,
          processEnvironments: true
      }
  };
  </script>
  <script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js" id="MathJax-script" async></script>
  </head>
  ```

- [ ] **Step 2: Update simple_md_to_html function**
  Modify [scripts/build_book.py](file:///opt/brainzhang/AITalkInvest/scripts/build_book.py).
  Find lines in `simple_md_to_html`:
  ```python
      html = re.sub(r'\$(.*?)\$', r'<code>\1</code>', html)
      html = re.sub(r'\$\$(.*?)\$\$', r'<pre>\1</pre>', html, flags=re.S)
  ```
  Replace with (remove or comment out these replacements so MathJax handles them):
  ```python
      # MathJax handles $ and $$ delimiters, do not replace them with code/pre tags
  ```

- [ ] **Step 3: Run build_book script verification**
  Run:
  ```bash
  conda run -n AITalkInvest python scripts/build_book.py
  ```
  Expected: Successful compile and output generated at `docs/韭韭归一：老亢给小白的投基兵法.html`.

- [ ] **Step 4: Verify output contents**
  Run:
  ```bash
  grep -i "MathJax" docs/韭韭归一：老亢给小白的投基兵法.html
  ```
  Expected: Matches for MathJax script load. Also check that `docs/韭韭归一：老亢给小白的投基兵法.html` contains the raw equations with `$$` (e.g. `$$E = 100 \times ...$$`).

- [ ] **Step 5: Commit changes**
  Run:
  ```bash
  git add scripts/build_book.py docs/韭韭归一：老亢给小白的投基兵法.html docs/韭韭归一：老亢给小白的投基兵法.md
  git commit -m "refactor: integrate MathJax rendering inside standalone HTML book template"
  ```
