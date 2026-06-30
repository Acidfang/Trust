#!/usr/bin/env python3
"""
Jekyll-like markdown renderer preview server
Converts .md files to HTML with proper styling
"""

import os
import re
from pathlib import Path
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import unquote
import markdown
import yaml

os.chdir(Path(__file__).parent)

class MarkdownRenderHandler(SimpleHTTPRequestHandler):
    """Renders markdown files as HTML"""
    
    def do_GET(self):
        # Normalize path
        path = unquote(self.path).lstrip('/')
        
        # Handle root
        if path == '' or path == '/':
            self.send_docs_index()
            return
        
        # Handle requests for .md files
        if path.endswith('.md'):
            full_path = Path(path)
            if full_path.exists() and full_path.is_file():
                self.render_markdown(full_path)
                return
        
        # For directory paths ending in /, show index
        if path.endswith('/'):
            dir_path = Path(path.rstrip('/'))
            if dir_path.exists() and dir_path.is_dir():
                # Check for index.md
                index_file = dir_path / 'index.md'
                if index_file.exists():
                    self.render_markdown(index_file)
                    return
                # Otherwise list directory
                self.list_directory_html(dir_path)
                return
        
        # Default: serve static files
        super().do_GET()
    
    def send_docs_index(self):
        """Send home page with link to /docs/"""
        html = """<!DOCTYPE html>
<html>
<head>
    <title>Wiki Preview</title>
    <style>
        body { 
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial; 
            margin: 40px; 
            max-width: 600px;
        }
        h1 { color: #0366d6; }
        a { color: #0366d6; text-decoration: none; }
        a:hover { text-decoration: underline; }
        .server-status { 
            background: #28a745; 
            color: white; 
            padding: 12px; 
            border-radius: 4px;
            margin-bottom: 20px;
        }
    </style>
</head>
<body>
    <div class="server-status">✓ Markdown Preview Server Running</div>
    <h1>📚 Wiki Documentation Preview</h1>
    <p><a href="/wiki/docs/">Browse documentation →</a></p>
</body>
</html>"""
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Content-Length', len(html.encode()))
        self.end_headers()
        self.wfile.write(html.encode())
    
    def list_directory_html(self, directory):
        """List contents of a directory"""
        try:
            files = sorted(directory.iterdir())
        except PermissionError:
            self.send_error(403, "Permission denied")
            return
        
        # Build HTML
        rel_path = str(directory).lstrip('.')
        html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Directory: {rel_path}</title>
    <style>
        body {{ 
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial; 
            margin: 40px; 
            max-width: 800px;
        }}
        h1 {{ color: #0366d6; }}
        a {{ color: #0366d6; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
        ul {{ list-style: none; padding: 0; }}
        li {{ padding: 8px 0; border-bottom: 1px solid #eee; }}
        .dir {{ font-weight: bold; }}
        .back {{ margin-bottom: 20px; }}
    </style>
</head>
<body>
    <div class="back"><a href="/wiki/docs/">← Back to docs</a></div>
    <h1>📁 {rel_path}</h1>
    <ul>
"""
        for item in files:
            if item.name.startswith('.'):
                continue
            
            if item.is_dir():
                html += f'<li class="dir">📂 <a href="{item.name}/">{item.name}/</a></li>\n'
            else:
                display_name = item.name
                if item.suffix == '.md':
                    display_name = f"📄 {item.name}"
                html += f'<li><a href="{item.name}">{display_name}</a></li>\n'
        
        html += """    </ul>
</body>
</html>"""
        
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Content-Length', len(html.encode()))
        self.end_headers()
        self.wfile.write(html.encode())
    
    def render_markdown(self, file_path):
        """Render a markdown file as HTML"""
        try:
            content = file_path.read_text(encoding='utf-8')
        except Exception as e:
            self.send_error(500, f"Error reading file: {e}")
            return
        
        # Parse YAML frontmatter
        frontmatter = {}
        markdown_content = content
        
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                try:
                    frontmatter = yaml.safe_load(parts[1]) or {}
                    markdown_content = parts[2].lstrip('\n')
                except:
                    pass
        
        # Convert markdown to HTML
        # Markdown will pass through raw HTML by default
        try:
            html_body = markdown.markdown(
                markdown_content,
                extensions=['extra', 'codehilite', 'toc']
            )
        except Exception as e:
            html_body = f"<p><strong>Markdown Error:</strong> {e}</p>"
        
        # Get metadata
        title = frontmatter.get('title', file_path.stem.replace('-', ' ').title())
        description = frontmatter.get('description', '')
        layout = frontmatter.get('layout', 'page')
        
        # Wrap in full HTML with Jekyll-like styling
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Helvetica Neue", Helvetica, Arial, sans-serif;
            line-height: 1.6;
            color: #24292e;
            background: #fff;
        }}
        
        .page-container {{
            max-width: 960px;
            margin: 0 auto;
            padding: 40px 20px;
        }}
        
        .page-header {{
            margin-bottom: 40px;
            padding-bottom: 20px;
            border-bottom: 1px solid #eaecef;
        }}
        
        .page-header h1 {{
            font-size: 2em;
            color: #0366d6;
            margin-bottom: 10px;
        }}
        
        .page-header p {{
            color: #6a737d;
            font-size: 0.95em;
        }}
        
        .page-content {{
            color: #24292e;
        }}
        
        .page-content h2 {{
            font-size: 1.5em;
            margin: 24px 0 16px 0;
            padding-top: 24px;
            border-top: 1px solid #eaecef;
            font-weight: 600;
        }}
        
        .page-content h3 {{
            font-size: 1.25em;
            margin: 16px 0 8px 0;
            font-weight: 600;
        }}
        
        .page-content p {{
            margin-bottom: 16px;
        }}
        
        .page-content code {{
            background: #f6f8fa;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: SFMono-Regular, Consolas, "Liberation Mono", Menlo, monospace;
            font-size: 0.85em;
        }}
        
        .page-content pre {{
            background: #f6f8fa;
            padding: 16px;
            border-radius: 6px;
            overflow-x: auto;
            margin-bottom: 16px;
            border: 1px solid #eaecef;
        }}
        
        .page-content pre code {{
            background: none;
            padding: 0;
            font-size: 0.9em;
        }}
        
        .page-content blockquote {{
            padding: 0 1em;
            color: #6a737d;
            border-left: 0.25em solid #dfe2e5;
            margin: 0 0 16px 0;
        }}
        
        .page-content a {{
            color: #0366d6;
            text-decoration: none;
        }}
        
        .page-content a:hover {{
            text-decoration: underline;
        }}
        
        .page-content ul, .page-content ol {{
            margin-left: 2em;
            margin-bottom: 16px;
        }}
        
        .page-content li {{
            margin-bottom: 8px;
        }}
        
        .page-content table {{
            border-collapse: collapse;
            width: 100%;
            margin-bottom: 16px;
        }}
        
        .page-content table th,
        .page-content table td {{
            padding: 6px 13px;
            border: 1px solid #dfe2e5;
            text-align: left;
        }}
        
        .page-content table th {{
            background: #f6f8fa;
            font-weight: 600;
        }}
        
        .back-link {{
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #eaecef;
        }}
        
        .back-link a {{
            color: #0366d6;
        }}
        
        /* Allow interactive elements to overflow if needed */
        .page-content canvas, 
        .page-content svg {{
            max-width: 100%;
            height: auto;
        }}
    </style>
</head>
<body>
    <div class="page-container">
        <div class="page-header">
            <h1>{title}</h1>
            {'<p>' + description + '</p>' if description else ''}
        </div>
        <div class="page-content">
            {html_body}
        </div>
        <div class="back-link">
            <a href="/wiki/docs/">&larr; Back to docs</a>
        </div>
    </div>
</body>
</html>"""
        
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Content-Length', len(html.encode()))
        self.end_headers()
        self.wfile.write(html.encode())

if __name__ == '__main__':
    port = 4000
    server = HTTPServer(('127.0.0.1', port), MarkdownRenderHandler)
    print(f"🔄 Markdown Renderer running at http://localhost:{port}")
    print(f"   Browse: http://localhost:{port}/wiki/docs/")
    print(f"\nPress Ctrl+C to stop")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n✓ Server stopped")
