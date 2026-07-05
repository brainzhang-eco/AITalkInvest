# Design Spec: Fix Math Formula Rendering in Zensical and HTML Book

## Goal
Enable LaTeX-style math formula rendering (both inline `$ ... $` and block `$$ ... $$`) on both the Zensical static site and the compiled standalone HTML book (`docs/韭韭归一：老亢给小白的投基兵法.html`) using MathJax.

---

## Detailed Plan

### 1. Configure Zensical Website for Math Rendering
1. Modify [zensical.toml](file:///opt/brainzhang/AITalkInvest/zensical.toml) to enable `pymdownx.arithmatex` and load MathJax JavaScript:
   ```toml
   [project.markdown_extensions.pymdownx.arithmatex]
   generic = true

   [project]
   # ... existing config ...
   extra_javascript = [
       "javascripts/mathjax.js",
       "https://unpkg.com/mathjax@3/es5/tex-mml-chtml.js"
   ]
   ```
2. Create `docs/javascripts/mathjax.js` with the MathJax configuration:
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

### 2. Configure Standalone HTML Book for Math Rendering
1. Modify [scripts/build_book.py](file:///opt/brainzhang/AITalkInvest/scripts/build_book.py):
   * Add MathJax loading script to `HTML_TEMPLATE` inside `<head>`:
     ```html
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
     ```
   * Remove conversion of `$` and `$$` from `simple_md_to_html` function:
     Remove or comment out:
     ```python
     # html = re.sub(r'\$(.*?)\$', r'<code>\1</code>', html)
     # html = re.sub(r'\$\$(.*?)\$\$', r'<pre>\1</pre>', html, flags=re.S)
     ```

---

## Verification Plan

### Local Verification
1. Run `python scripts/build_book.py` to generate the HTML book. Check `docs/韭韭归一：老亢给小白的投基兵法.html` file content to verify `<script>` tags are present and the math delimiters `$`/`$$` are preserved without being converted to code/pre tags.
2. Run `zensical build` to compile the static site. Verify `site/index.html` and other generated HTML pages have the `extra_javascript` references and load correctly.
