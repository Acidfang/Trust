# GitHub Pages Setup for Wiki

## What's Been Configured

✅ **GitHub Workflow**: `.github/workflows/build-wiki.yml`
- Automatically builds the wiki when changes are pushed to master
- Builds from the `/wiki` directory
- Publishes to GitHub Pages using `peaceiris/actions-gh-pages`

✅ **Jekyll Configuration**: `wiki/_config.yml`
- Theme: minima (GitHub Pages compatible)
- Baseurl: `/Trust` (matches repository name)
- URL: `https://acidfang.github.io`
- All plugins are GitHub Pages compatible

✅ **Gemfile**: `wiki/Gemfile`
- Uses only GitHub Pages compatible gems
- Includes jekyll-feed, jekyll-seo-tag, jekyll-sitemap

## Steps to Enable GitHub Pages

You need to configure GitHub Pages settings on the repository:

1. **Go to GitHub Repository Settings**
   - Navigate to: https://github.com/Acidfang/Trust
   - Go to **Settings** → **Pages**

2. **Configure Source**
   - **Source Branch**: `gh-pages` (this will be created by the workflow)
   - **Root Folder**: `/` (default)

3. **Verify Workflow**
   - Go to **Actions** tab
   - Watch for "Build and Deploy Wiki" workflow
   - First push to master will trigger the build

## How It Works

1. **You push to master** in the `/wiki` folder
2. **GitHub Actions runs** `.github/workflows/build-wiki.yml`
3. **Jekyll builds** the site from `wiki/` → `wiki/_site/`
4. **Workflow deploys** to `gh-pages` branch
5. **GitHub Pages serves** the site at: **https://acidfang.github.io/Trust**

## Testing Locally (Before Pushing)

### Option 1: Python Simple Server
```powershell
cd c:\Determined\wiki\docs
python -m http.server 8000
# Visit http://localhost:8000
```

### Option 2: Jekyll Local Build
```powershell
cd c:\Determined\wiki
bundle install
bundle exec jekyll serve --baseurl "/Trust"
# Visit http://localhost:4000/Trust
```

## File Structure

```
Acidfang/Trust (GitHub repo)
├── .github/workflows/
│   └── build-wiki.yml          ← Workflow that deploys site
├── wiki/                        ← Source of the wiki
│   ├── _config.yml              ← Jekyll config (UPDATED)
│   ├── _layouts/
│   ├── _data/
│   ├── _includes/
│   ├── Gemfile                  ← Dependencies
│   └── docs/
│       ├── index.md             ← Entry point
│       ├── the-root-cause-goal-blindness.md
│       ├── frameworks-comparison.md
│       ├── learning-pathways.md
│       └── [all other pages]
├── docs/                        ← Built site output (created by workflow)
│   └── [generated HTML files]
└── gh-pages/                    ← GitHub Pages branch (created by workflow)
    └── [static site content]
```

## Key URLs

- **Repository**: https://github.com/Acidfang/Trust
- **Wiki Live**: https://acidfang.github.io/Trust (after Pages is enabled)
- **Pages Settings**: https://github.com/Acidfang/Trust/settings/pages
- **Actions**: https://github.com/Acidfang/Trust/actions

## Troubleshooting

### Build Fails
Check the Actions tab for error logs:
- Missing dependencies? → Check `wiki/Gemfile`
- Layout missing? → Check `wiki/_layouts/` directory
- Bad YAML in front matter? → Check markdown file headers

### Site Doesn't Update
- Did you push to `master` branch? (workflow only runs on master)
- Did the workflow complete successfully? → Check Actions tab
- Is Pages properly configured? → Check Settings → Pages

### Pages Says "No commits yet"
This is normal. The `gh-pages` branch is created by the workflow on first successful build.

## What's Live

Once GitHub Pages is enabled and the workflow completes:

### Entry Point
- https://acidfang.github.io/Trust → `wiki/docs/index.md`

### Root-Cause Framework (START HERE)
- https://acidfang.github.io/Trust/the-root-cause-goal-blindness/
- https://acidfang.github.io/Trust/evidence-why-undeniables-are-real/
- https://acidfang.github.io/Trust/the-undeniable-pattern/
- https://acidfang.github.io/Trust/the-mirror-not-the-same/

### How Reality Works
- https://acidfang.github.io/Trust/how-reality-works-blocking-mechanisms/
- https://acidfang.github.io/Trust/how-reality-works-quick-ref/
- https://acidfang.github.io/Trust/how-reality-works-applied-analysis/

### Learning & Navigation
- https://acidfang.github.io/Trust/frameworks-comparison/
- https://acidfang.github.io/Trust/learning-pathways/
- https://acidfang.github.io/Trust/case-studies/

## Summary

The wiki is now configured for GitHub Pages automation:
- ✅ Workflow handles Jekyll build
- ✅ Jekyll config is GitHub Pages compatible
- ✅ All required files are in place
- ✅ Baseurl and URL are correctly set

**Next step**: Enable GitHub Pages in repository Settings (Pages section) to point to `gh-pages` branch.
