#!/usr/bin/env python3
"""
Complete Jekyll site generator in pure Python
Builds a complete static site from markdown, templates, and configuration
"""

import os
import sys
import yaml
import markdown
import re
import shutil
from pathlib import Path
from datetime import datetime
from urllib.parse import quote

class JekyllGenerator:
    def __init__(self, wiki_dir):
        self.wiki_dir = Path(wiki_dir)
        self.docs_dir = self.wiki_dir / 'docs'
        self.layouts_dir = self.wiki_dir / '_layouts'
        self.includes_dir = self.wiki_dir / '_includes'
        self.output_dir = self.wiki_dir / '_site'
        self.config = {}
        self.pages = []
        
    def load_config(self):
        """Load Jekyll configuration from _config.yml"""
        config_file = self.wiki_dir / '_config.yml'
        if config_file.exists():
            with open(config_file, 'r', encoding='utf-8') as f:
                self.config = yaml.safe_load(f) or {}
        print(f"✓ Loaded config: {self.config.get('title', 'Untitled')}")
        return self.config
    
    def load_layout(self, layout_name='default'):
        """Load HTML layout template"""
        layout_file = self.layouts_dir / f'{layout_name}.html'
        if layout_file.exists():
            with open(layout_file, 'r', encoding='utf-8') as f:
                return f.read()
        # Fallback to default layout if specified layout doesn't exist
        if layout_name != 'default':
            default_file = self.layouts_dir / 'default.html'
            if default_file.exists():
                with open(default_file, 'r', encoding='utf-8') as f:
                    return f.read()
        return None
    
    def process_liquid(self, template, context):
        """Process Liquid template syntax with context"""
        # Replace {{ site.baseurl }} with empty string (local site has no baseurl)
        template = re.sub(r"{{\s*site\.baseurl\s*}}", '', template)
        
        # Replace {{ variables }}
        for key, value in context.items():
            # Escape the replacement value to prevent regex issues
            escaped_value = str(value).replace('\\', '\\\\')
            # Handle simple variables with various spacing
            template = re.sub(r"{{\s*" + re.escape(key) + r"\s*}}", escaped_value, template, flags=re.IGNORECASE)
        
        # Process relative_url filter: {{ '/path' | relative_url }} → /path
        template = re.sub(r"{{\s*'([^']+)'\s*\|\s*relative_url\s*}}", r"\1", template)
        
        # Process if/endif blocks (simplified - just remove the markers)
        template = re.sub(r'{%\s*if\s+[^%]*%\}.*?{%\s*endif\s*%\}', '', template, flags=re.DOTALL)
        
        # Remove unparseable liquid
        template = re.sub(r'{%[^%]*%\}', '', template)
        
        return template
    
    def process_liquid_content(self, content):
        """Process Liquid tags in markdown content"""
        # Replace {{ site.baseurl }} with empty string
        content = re.sub(r"{{\s*site\.baseurl\s*}}", '', content)
        
        # Process relative_url filter: {{ '/path' | relative_url }} → /path
        content = re.sub(r"{{\s*'([^']+)'\s*\|\s*relative_url\s*}}", r"\1", content)
        
        # Remove other unparseable Liquid tags
        content = re.sub(r"{{\s*[^}]+\s*}}", '', content)
        
        return content
    
    def load_include(self, include_name):
        """Load and process an include file"""
        include_file = self.includes_dir / f'{include_name}.html'
        if include_file.exists():
            with open(include_file, 'r', encoding='utf-8') as f:
                content = f.read()
            # Process navigation - simplified rendering
            return self.process_navigation_html(content)
        return ''
    
    def process_navigation_html(self, nav_html):
        """Process navigation HTML and convert Liquid loops to actual HTML"""
        # For now, just return the HTML as-is (it's already static in navigation-unified.html)
        # Remove Liquid syntax that might break HTML rendering
        nav_html = re.sub(r'{%\s*if[^%]*%\}', '', nav_html)
        nav_html = re.sub(r'{%\s*endif\s*%\}', '', nav_html)
        nav_html = re.sub(r'{%\s*include[^%]*%\}', '', nav_html)
        
        # Process variable replacements
        nav_html = nav_html.replace("{{ site.title }}", self.config.get('title', ''))
        nav_html = nav_html.replace("{{ site.description }}", self.config.get('description', ''))
        nav_html = nav_html.replace("{{ '/' | relative_url }}", "/")
        
        # Simple relative_url filter replacement
        nav_html = re.sub(r"{{\s*'([^']+)'\s*\|\s*relative_url\s*}}", r"\1", nav_html)
        
        return nav_html
    
    def parse_frontmatter(self, content):
        """Extract YAML frontmatter from markdown"""
        if not content.startswith('---'):
            return {}, content
        
        parts = content.split('---', 2)
        if len(parts) < 3:
            return {}, content
        
        try:
            frontmatter = yaml.safe_load(parts[1])
            body = parts[2].strip()
            return frontmatter or {}, body
        except:
            return {}, content
    
    def markdown_to_html(self, content):
        """Convert markdown to HTML"""
        md = markdown.Markdown(
            extensions=['extra', 'codehilite', 'toc'],
            extension_configs={
                'toc': {
                    'title': 'Table of Contents',
                    'toc_depth': '2-3',
                }
            }
        )
        return md.convert(content)
    
    def scan_docs(self):
        """Scan docs directory for markdown files"""
        if not self.docs_dir.exists():
            print("! Docs directory not found")
            return []
        
        pages = []
        for md_file in self.docs_dir.glob('*.md'):
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            frontmatter, body = self.parse_frontmatter(content)
            
            # Default values
            page = {
                'filename': md_file.stem,
                'filepath': md_file,
                'url': '/' + md_file.stem + '/',
                'title': frontmatter.get('title', md_file.stem.replace('-', ' ').title()),
                'layout': frontmatter.get('layout', 'default'),
                'frontmatter': frontmatter,
                'body': body,
            }
            
            # Override URL if specified
            if 'permalink' in frontmatter:
                page['url'] = frontmatter['permalink']
            
            pages.append(page)
        
        print(f"✓ Found {len(pages)} markdown files")
        return pages
    
    def render_page(self, page):
        """Render a single page with layout"""
        # Convert markdown to HTML
        content_html = self.markdown_to_html(page['body'])
        
        # Process Liquid tags in content FIRST (markdown may have Liquid syntax)
        content_html = self.process_liquid_content(content_html)
        
        # Load layout
        layout_name = page.get('layout', 'default')
        layout = self.load_layout(layout_name)
        
        if not layout:
            return content_html
        
        # Load navigation include FIRST, before processing liquid
        nav_html = self.load_include('navigation-unified')
        
        # Replace include tags with actual content
        layout = re.sub(r'{%\s*include\s+["\']?navigation-unified\.html["\']?\s*%\}', nav_html, layout, flags=re.IGNORECASE)
        
        # Build context for template rendering
        context = {
            'site.title': self.config.get('title', ''),
            'site.description': self.config.get('description', ''),
            'page.title': page['title'],
            'page.url': page['url'],
            'content': content_html,
            'now': datetime.now().strftime('%Y-%m-%d'),
        }
        
        # Process layout with Liquid (this removes remaining liquid tags)
        rendered = self.process_liquid(layout, context)
        
        # Replace content placeholder
        rendered = rendered.replace('{{ content }}', content_html)
        
        # Replace navigation include
        rendered = rendered.replace('{% include navigation-unified.html %}', nav_html)
        
        return rendered
    
    def generate_site(self):
        """Generate complete site"""
        print("\n" + "="*70)
        print("JEKYLL SITE GENERATOR")
        print("="*70)
        
        # Load configuration
        self.load_config()
        
        # Clear and create output directory
        if self.output_dir.exists():
            shutil.rmtree(self.output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Copy assets
        assets_src = self.wiki_dir / 'assets'
        if assets_src.exists():
            shutil.copytree(assets_src, self.output_dir / 'assets')
            print(f"✓ Copied assets")
        
        # Scan and render pages
        self.pages = self.scan_docs()
        
        generated_count = 0
        for page in self.pages:
            # Render page
            html = self.render_page(page)
            
            # Determine output path - create directory/index.html structure
            url_path = page['url'].strip('/')
            if not url_path:
                url_path = 'index'
                output_file = self.output_dir / 'index.html'
            else:
                # Create directory/index.html for proper URL routing
                output_file = self.output_dir / url_path / 'index.html'
            
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            # Write file
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(html)
            
            print(f"  ✓ {page['filename']}.md → {url_path}/")
            generated_count += 1
        
        print("\n" + "="*70)
        print(f"✅ SITE GENERATED: {generated_count} pages")
        print(f"📁 Output: {self.output_dir}")
        print("="*70 + "\n")
        
        return self.output_dir

if __name__ == '__main__':
    wiki_path = Path(__file__).parent
    generator = JekyllGenerator(wiki_path)
    generator.generate_site()
