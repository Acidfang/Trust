# Jekyll Wiki Deployment Guide

## Quick Start (GitHub Pages)

### Step 1: Push to GitHub

```bash
# Initialize git repository
cd wiki
git init

# Add all files
git add .

# Commit
git commit -m "Initial wiki deployment: The Cold Hard Truth, The Path To Perfection"

# Create GitHub repository (via GitHub web interface first)
# Then:
git remote add origin https://github.com/YOUR_USERNAME/cold-hard-truth.git
git branch -M main
git push -u origin main
```

### Step 2: Enable GitHub Pages

1. Go to your repository on GitHub
2. Settings → Pages
3. Source: Deploy from branch → main
4. Folder: / (root)
5. Save

**Your site will be live at**: `https://YOUR_USERNAME.github.io/cold-hard-truth`

---

## Local Development

### Prerequisites
- Ruby 2.7+
- Bundler

### Setup
```bash
cd wiki
bundle install
bundle exec jekyll serve
```

Visit `http://localhost:4000` in your browser.

### Making Changes
1. Edit files in `docs/`, `_layouts/`, or `assets/`
2. Jekyll auto-reloads on file changes
3. Refresh browser to see updates
4. Test thoroughly before pushing

---

## Directory Structure

```
wiki/
├── _config.yml              # Jekyll configuration
├── _layouts/
│   └── default.html        # Main layout template
├── _includes/
│   ├── navigation.html     # Sidebar navigation
│   └── search-index.html   # Search functionality
├── assets/
│   ├── css/
│   │   └── style.css       # Main stylesheet (dark mode included)
│   └── js/
│       ├── theme.js        # Dark mode toggle
│       ├── toc.js          # Table of contents generation
│       └── search.js       # Search functionality
├── docs/
│   ├── 01_internal_coherence.md
│   ├── 02_help_systems.md
│   ├── 03_diagnostic_method.md
│   ├── 04_universal_foundation.md
│   ├── 05_gate_discovery.md
│   ├── 06_implementation.md
│   ├── 07_future.md
│   └── 08_complete_document.md
├── index.md                # Landing page
├── README.md               # GitHub README
├── Gemfile                 # Ruby dependencies
└── .gitignore             # Git ignore rules
```

---

## Customization

### Color Scheme

Edit `assets/css/style.css`:

```css
:root {
  --color-bg: #ffffff;
  --color-text: #1a1a1a;
  --color-accent: #2c3e50;
  /* ... etc */
}

body.dark-mode {
  --color-bg: #1a1a1a;
  --color-text: #e0e0e0;
  /* ... etc */
}
```

### Site Title & Metadata

Edit `_config.yml`:

```yaml
title: Your Title
description: Your description
author: Your Name
```

### Navigation Menu

Edit `_includes/navigation.html` to add/remove sections.

### Layout

Edit `_layouts/default.html` to change page structure.

---

## SEO & Metadata

Jekyll automatically generates:
- `sitemap.xml` - Search engine sitemap
- `feed.xml` - RSS feed
- Meta tags for social sharing

---

## Performance Tips

1. **Images**: Compress before uploading
2. **CSS**: Already optimized and minified
3. **Search**: Limited to 10 results for speed
4. **TOC**: Generated dynamically on page load

---

## Troubleshooting

### Site not building
```bash
# Clear Jekyll cache
rm -rf _site .jekyll-cache

# Rebuild
bundle exec jekyll build
```

### Search not working
- Check `_includes/search-index.html` is present
- Verify `assets/js/search.js` is loading
- Check browser console for errors

### Dark mode not working
- Check `assets/js/theme.js` is loading
- Verify CSS variables in `assets/css/style.css`
- Check localStorage quota

### Navigation broken
- Verify all markdown files have `permalink:` in front matter
- Check `_includes/navigation.html` links match permalinks

---

## Deployment Checklist

- [ ] All markdown files created
- [ ] _config.yml configured with your details
- [ ] GitHub repository created
- [ ] GitHub Pages enabled
- [ ] Site accessible at `https://YOUR_USERNAME.github.io/cold-hard-truth`
- [ ] Navigation menu links work
- [ ] Search functionality working
- [ ] Dark mode toggle working
- [ ] Print-to-PDF works correctly
- [ ] Mobile responsive tested

---

## Maintenance

### Regular Updates
- Keep Jekyll updated: `bundle update`
- Update Ruby if needed
- Monitor GitHub notifications for security issues

### Backup
- Push regularly to GitHub
- Consider automated backups of `_site/` directory

### Analytics (Optional)
Add Google Analytics to `_config.yml`:
```yaml
google_analytics: "UA-XXXXXXXXX-X"
```

---

## Advanced: Custom Domain

To use your own domain:

1. GitHub Settings → Pages → Custom domain
2. Enter your domain: `wiki.yourdomain.com`
3. Update DNS records (see GitHub instructions)
4. Add CNAME file to root:

```
echo "wiki.yourdomain.com" > CNAME
git add CNAME
git commit -m "Add custom domain"
git push
```

---

## Support

For Jekyll help: https://jekyllrb.com/docs/
For GitHub Pages: https://docs.github.com/en/pages

---

**You now have a complete, production-ready wiki!**

Next: Push to GitHub and share the link.
