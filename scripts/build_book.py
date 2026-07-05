import os
import re

# Configuration
CHAPTERS = [
    "00_序言.md", "01_第一回.md", "02_第二回.md", "03_第三回.md", 
    "04_第四回.md", "05_第五回.md", "06_第六回.md", "07_第七回.md", 
    "08_第八回.md", "09_结语.md"
]
BOOK_TITLE = "韭韭归一：老亢给小白的投基兵法"
MD_OUTPUT = os.path.join("docs", f"{BOOK_TITLE}.md")
HTML_OUTPUT = os.path.join("docs", f"{BOOK_TITLE}.html")

# HTML Template
HTML_TEMPLATE = """<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>{title}</title>
<style>
    body {{
        font-family: "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", "WenQuanYi Micro Hei", sans-serif;
        line-height: 1.8;
        color: #333;
        max-width: 800px;
        margin: 0 auto;
        padding: 40px;
        background-color: #fdfdfd;
    }}
    h1, h2, h3, h4 {{
        color: #1a1a1a;
        border-bottom: 1px solid #eee;
        padding-bottom: 10px;
        margin-top: 40px;
    }}
    h1 {{ font-size: 2.5em; text-align: center; border-bottom: none; }}
    h4 {{ border-bottom: none; margin-top: 20px; color: #d2691e; }}
    .subtitle {{ text-align: center; font-style: italic; color: #666; margin-top: -20px; margin-bottom: 40px; }}
    blockquote {{
        border-left: 5px solid #d2691e;
        background-color: #fff9f0;
        padding: 15px 20px;
        margin: 20px 0;
        font-style: italic;
    }}
    code {{
        background-color: #f4f4f4;
        padding: 2px 5px;
        border-radius: 3px;
        font-family: Consolas, Monaco, 'Andale Mono', 'Ubuntu Mono', monospace;
    }}
    pre {{
        background-color: #f4f4f4;
        padding: 15px;
        border-radius: 5px;
        overflow-x: auto;
    }}
    table {{
        border-collapse: collapse;
        width: 100%;
        margin: 20px 0;
    }}
    th, td {{
        border: 1px solid #ddd;
        padding: 12px;
        text-align: left;
    }}
    th {{ background-color: #f8f8f8; }}
    .page-break {{ page-break-before: always; }}
    .toc {{ background: #f9f9f9; padding: 20px; border-radius: 5px; }}
    .toc ul {{ list-style: none; padding-left: 0; }}
    .toc li {{ margin-bottom: 8px; }}
    .toc a {{ color: #d2691e; text-decoration: none; }}
    .toc a:hover {{ text-decoration: underline; }}
</style>
<script>
window.MathJax = {{
    tex: {{
        inlineMath: [['$', '$'], ['\\\\(', '\\\\)']],
        displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']],
        processEscapes: true,
        processEnvironments: true
    }}
}};
</script>
<script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js" id="MathJax-script" async></script>
</head>
<body>
<h1>{title}</h1>
<div class="subtitle">老亢给小白的投基兵法</div>
<div class="toc">
    <h2>目录</h2>
    <ul>
{toc_items}
    </ul>
</div>
<div class="page-break"></div>
{body_content}
</body>
</html>
"""

def simple_md_to_html(md_text):
    html = md_text
    # Order matters here
    html = re.sub(r'^# (.*)$', r'<h1>\1</h1>', html, flags=re.M)
    html = re.sub(r'^## (.*)$', r'<h2>\1</h2>', html, flags=re.M)
    html = re.sub(r'^### (.*)$', r'<h3>\1</h3>', html, flags=re.M)
    html = re.sub(r'^#### (.*)$', r'<h4>\1</h4>', html, flags=re.M)
    html = re.sub(r'^> (.*)$', r'<blockquote>\1</blockquote>', html, flags=re.M)
    html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html)
    # MathJax handles $ and $$ delimiters, do not replace them with code/pre tags
    html = re.sub(r'^\* (.*)$', r'<li>\1</li>', html, flags=re.M)
    html = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', html)
    html = html.replace('\n\n', '</p><p>')
    return f'<p>{html}</p>'

def build():
    # 1. Prepare TOC and Titles
    titles = []
    for chapter in CHAPTERS:
        with open(os.path.join("docs", chapter), "r", encoding="utf-8") as f:
            first_line = f.readline()
            titles.append(first_line.replace("# ", "").strip())

    # 2. Generate Combined Markdown
    page_break_md = "\n\n<div style=\"page-break-after: always;\"></div>\n\n"
    with open(MD_OUTPUT, "w", encoding="utf-8") as f:
        f.write(f"# {BOOK_TITLE}\n\n## 目录\n\n")
        for i, title in enumerate(titles):
            f.write(f"{i}. [{title}](#{title.replace('：', '').replace(' ', '-')})\n")
        f.write("\n---\n\n")
        for chapter in CHAPTERS:
            with open(os.path.join("docs", chapter), "r", encoding="utf-8") as c:
                content = c.read()
                f.write(content)
                f.write(page_break_md)
                f.write("\n\n---\n\n")

    # 3. Generate HTML
    toc_items = ""
    for i, title in enumerate(titles):
        toc_items += f'        <li><a href="#ch{i}">{title}</a></li>\n'

    body_content = ""
    for i, chapter in enumerate(CHAPTERS):
        with open(os.path.join("docs", chapter), "r", encoding="utf-8") as f:
            content = f.read()
            body_content += f'<div id="ch{i}" class="page-break">'
            body_content += simple_md_to_html(content)
            body_content += '</div>\n'

    full_html = HTML_TEMPLATE.format(
        title=BOOK_TITLE,
        toc_items=toc_items,
        body_content=body_content
    )
    with open(HTML_OUTPUT, "w", encoding="utf-8") as f:
        f.write(full_html)

    print(f"Build successful: \n- {MD_OUTPUT}\n- {HTML_OUTPUT}")

if __name__ == "__main__":
    build()
