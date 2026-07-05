# Design Spec: Compile Static Site with Zensical and Deploy to GitHub Pages

## Goal
Configure and compile the repository as a static documentation website using Zensical. Deploy the compiled website to GitHub Pages under the custom domain `invest.brainz.fun` using GitHub Actions.

---

## Detailed Plan

### 1. Zensical Configuration (`zensical.toml`)
Create a configuration file `zensical.toml` at the project root:
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

### 2. Website Landing Page (`docs/index.md`)
Create `docs/index.md` based on `README.md` to serve as the homepage of the website. Clean up irrelevant root layout sections (such as "项目结构" or "导出建议") to keep the web landing page concise and focused.

### 3. GitHub Actions CI/CD (`.github/workflows/deploy.yml`)
Create a workflow `.github/workflows/deploy.yml` that runs on push to `main`:
* Checks out code.
* Installs Python 3.12 and Zensical.
* Runs `zensical build --clean`.
* Uses `peaceiris/actions-gh-pages@v3` to publish the `./site` directory to `gh-pages` branch, configured with the CNAME `invest.brainz.fun`.

### 4. Local Installation and Verification
1. Install Zensical in the local Python/Conda environment:
   ```bash
   conda activate AITalkInvest
   pip install zensical
   ```
2. Build the site locally:
   ```bash
   zensical build
   ```
3. Check the output files in `site/` to make sure HTML structure is correct.

---

## Verification Plan

### Manual Verification
1. Run local build: `zensical build`.
2. Check that `site/index.html` exists and is formatted correctly.
3. Check that `site/CNAME` contains `invest.brainz.fun`.
4. Run `git status` to ensure all new configuration files are tracked.
