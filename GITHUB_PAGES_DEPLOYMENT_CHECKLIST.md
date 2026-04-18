# GitHub Pages Wiki - Deployment Checklist

## ✅ Configuration Complete

All systems are configured for automatic GitHub Pages deployment. **The wiki will build and deploy automatically when you push to master.**

---

## GitHub Pages Setup Checklist

### Server Configuration
- ✅ **Jekyll build workflow**: `.github/workflows/build-wiki.yml`
  - Triggers on: Push to `master` branch
  - Builds from: `/wiki` directory  
  - Publishes to: `gh-pages` branch
  - Deploy action: `peaceiris/actions-gh-pages`

- ✅ **Jekyll configuration**: `wiki/_config.yml`
  - Theme: `minima` (GitHub Pages default)
  - Baseurl: `/Trust` (matches repo name)
  - URL: `https://acidfang.github.io`
  - Safe mode: `true` (GitHub Pages compatible)
  - All plugins: GitHub Pages compatible

- ✅ **Dependencies**: `wiki/Gemfile`
  - jekyll ~> 4.3
  - jekyll-feed
  - jekyll-seo-tag
  - jekyll-sitemap
  - minima ~> 2.5

### Markdown Files
- ✅ **Front matter**: All critical pages have proper YAML headers
  - `the-root-cause-goal-blindness.md` ✓
  - `the-mirror-not-the-same.md` ✓
  - `the-undeniable-pattern.md` ✓
  - `evidence-why-undeniables-are-real.md` ✓
  - `how-reality-works-blocking-mechanisms.md` ✓
  - `how-reality-works-quick-ref.md` ✓
  - `how-reality-works-applied-analysis.md` ✓
  - `frameworks-comparison.md` ✓
  - `learning-pathways.md` ✓
  - `index.md` ✓

- ✅ **Layouts**: `wiki/_layouts/default.html` exists
- ✅ **Data**: `wiki/_data/frameworks.yml` properly formatted

### Publishing Ready
- ✅ **Repository**: `Acidfang/Trust` on GitHub
- ✅ **Remote**: `git remote -v` shows `origin` pointing to GitHub
- ✅ **Commits**: All changes committed to master branch

---

## What to do Now

### Step 1: Enable GitHub Pages
Go to: **https://github.com/Acidfang/Trust/settings/pages**

1. Click **Settings** → **Pages**
2. Under "Source", select:
   - **Branch**: `gh-pages` (created by workflow)
   - **Folder**: `/ (root)`
3. Click "Save"

GitHub Pages will show: "Your site is published at **https://acidfang.github.io/Trust**"

### Step 2: Push to Trigger Build
```powershell
cd c:\Determined
git push origin master
```

The workflow will automatically:
1. Build Jekyll from `/wiki`
2. Generate HTML in `wiki/_site/`
3. Deploy to `gh-pages` branch
4. Update live site at: https://acidfang.github.io/Trust

### Step 3: Monitor Build
1. Go to: **https://github.com/Acidfang/Trust/actions**
2. Watch "Build and Deploy Wiki" workflow running
3. Check for ✅ (success) or ❌ (failure)

---

## What Gets Published

### Entry Point
- **https://acidfang.github.io/Trust** → `wiki/docs/index.md`

### Framework Pages (START HERE)
- https://acidfang.github.io/Trust/the-root-cause-goal-blindness/
- https://acidfang.github.io/Trust/evidence-why-undeniables-are-real/
- https://acidfang.github.io/Trust/the-undeniable-pattern/
- https://acidfang.github.io/Trust/the-mirror-not-the-same/

### How Reality Works
- https://acidfang.github.io/Trust/how-reality-works-blocking-mechanisms/
- https://acidfang.github.io/Trust/how-reality-works-quick-ref/
- https://acidfang.github.io/Trust/how-reality-works-applied-analysis/

### Navigation & Learning
- https://acidfang.github.io/Trust/frameworks-comparison/
- https://acidfang.github.io/Trust/pathways/
- Plus all other documented pages

---

## Troubleshooting

### Build Fails (Red ❌ in Actions)
1. Click the failed workflow in Actions tab
2. Check logs for error message
3. Common issues:
   - **Ruby version mismatch**: Check `ruby/setup-ruby@v1` version
   - **Missing gems**: Verify `wiki/Gemfile` has all dependencies
   - **Markdown syntax error**: Check YAML front matter format

### Site Shows "Page not found" (404)
1. Verify GitHub Pages is enabled (Settings → Pages)
2. Check workflow completed successfully (Actions tab)
3. Wait 1-2 minutes for GitHub Pages to update
4. Try accessing https://acidfang.github.io/Trust (not /wiki)

### Changes Not Appearing
1. Did you push to `master` branch?
2. Check Actions tab for "Build and Deploy Wiki" workflow
3. If workflow didn't run, check the file paths in `build-wiki.yml` trigger

---

## Summary

| Component | Status | Location |
|-----------|--------|----------|
| Workflow | ✅ Ready | `.github/workflows/build-wiki.yml` |
| Jekyll Config | ✅ Ready | `wiki/_config.yml` |
| Gemfile | ✅ Ready | `wiki/Gemfile` |
| Front Matter | ✅ Complete | All `wiki/docs/*.md` files |
| Layouts | ✅ Ready | `wiki/_layouts/` |
| GitHub Pages | ⏳ Pending | Settings → Pages (enable now) |
| Live Site | ⏳ Pending | https://acidfang.github.io/Trust |

**Next Step**: Enable GitHub Pages in repository Settings (use link above)

After that, just push to master and the wiki will auto-deploy!

---

## Files Modified/Created

```
Commits for GitHub Pages automation:
- 221b912: Configure GitHub Pages automation
  - workflow/build-wiki.yml (UPDATED)
  - wiki/_config.yml (UPDATED)
  - GITHUB_PAGES_SETUP.md (CREATED)

- f245e5f: Add Jekyll front matter
  - All critical wiki/*.md files (UPDATED with front matter)
```

---

## Git Commands Reference

```powershell
# View current remote
git remote -v

# View branch
git branch -a

# Check workflow status
git log --oneline -5

# Push to trigger build
git push origin master -v

# Check git status
git status
```

All set! 🚀
